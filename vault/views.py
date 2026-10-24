
import json
import os
from hashlib import sha256

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import SignUpForm, DocumentUploadForm
from .models import Document, DocumentGrant, AuditEvent
from .permissions import can_read_document

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


def record_audit(actor, document, action, outcome, details=None):
    """Record an audit event linked to the previous event's hash."""
    details = details or {}

    with transaction.atomic():
        previous = (
            AuditEvent.objects
            .select_for_update()
            .order_by("-id")
            .first()
        )

        previous_hash = previous.event_hash if previous else "0" * 64
        timestamp = timezone.now()

        payload = {
            "actor_id": actor.id if actor and actor.is_authenticated else None,
            "document_id": document.id if document else None,
            "action": action,
            "outcome": outcome,
            "timestamp": timestamp.isoformat(),
            "details": details,
            "previous_hash": previous_hash,
        }

        event_hash = sha256(
            json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

        AuditEvent.objects.create(
            actor=actor if actor and actor.is_authenticated else None,
            document=document,
            action=action,
            outcome=outcome,
            timestamp=timestamp,
            details=details,
            previous_hash=previous_hash,
            event_hash=event_hash,
        )


def home(request):
    return render(request, "vault/home.html")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "vault/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm(request)

    return render(request, "vault/login.html", {"form": form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    """Display owned and shared documents, with title/category search."""
    query = request.GET.get("q", "").strip()

    documents = Document.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    shared_documents = Document.objects.filter(
        grants__user=request.user
    ).exclude(
        owner=request.user
    ).distinct().order_by("-created_at")

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

        shared_documents = shared_documents.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    grants = DocumentGrant.objects.filter(
        document__owner=request.user
    ).select_related("document", "user")

    return render(
        request,
        "vault/dashboard.html",
        {
            "documents": documents,
            "shared_documents": shared_documents,
            "grants": grants,
            "upload_form": DocumentUploadForm(),
            "query": query,
        },
    )


@login_required
@require_POST
def upload_document(request):
    form = DocumentUploadForm(request.POST, request.FILES)

    if form.is_valid():
        uploaded_file = form.cleaned_data.get("file")

        if uploaded_file is None:
            form.add_error("file", "Please select a file.")
        elif uploaded_file.size > MAX_UPLOAD_SIZE:
            form.add_error("file", "The maximum allowed file size is 10 MB.")
        else:
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

            record_audit(
                request.user,
                document,
                "upload",
                "success",
                {"title": document.title},
            )

            return redirect("dashboard")

    documents = Document.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    shared_documents = Document.objects.filter(
        grants__user=request.user
    ).exclude(
        owner=request.user
    ).distinct().order_by("-created_at")

    grants = DocumentGrant.objects.filter(
        document__owner=request.user
    ).select_related("document", "user")

    return render(
        request,
        "vault/dashboard.html",
        {
            "documents": documents,
            "shared_documents": shared_documents,
            "grants": grants,
            "upload_form": form,
            "query": "",
        },
    )


@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if not can_read_document(request.user, document):
        record_audit(
            request.user,
            document,
            "download",
            "denied",
            {"reason": "Insufficient document permissions"},
        )

        return HttpResponseForbidden(
            "You do not have permission to access this document."
        )

    try:
        file_handle = document.file.open("rb")
    except (FileNotFoundError, ValueError, OSError):
        raise Http404("The document file could not be found.")

    record_audit(
        request.user,
        document,
        "download",
        "success",
        {"title": document.title},
    )

    filename = os.path.basename(document.file.name)

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=filename,
    )


@login_required
def grant_permission(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id,
        owner=request.user,
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        permission = request.POST.get("permission", "").strip()

        if not username:
            error = "Username is required."
        elif permission not in (
            DocumentGrant.READ,
            DocumentGrant.EDIT,
        ):
            error = "Choose a valid permission."
        else:
            target_user = User.objects.filter(
                username=username
            ).first()

            if target_user is None:
                error = "That username does not exist."
            elif target_user.id == request.user.id:
                error = "You already own this document."
            else:
                grant, created = DocumentGrant.objects.update_or_create(
                    document=document,
                    user=target_user,
                    defaults={"permission": permission},
                )

                record_audit(
                    request.user,
                    document,
                    "permission_grant" if created else "permission_update",
                    "success",
                    {
                        "target_username": target_user.username,
                        "permission": permission,
                    },
                )

                return redirect("dashboard")

        return render(
            request,
            "vault/grant_permission.html",
            {
                "document": document,
                "error": error,
            },
        )

    return render(
        request,
        "vault/grant_permission.html",
        {"document": document},
    )


@login_required
@require_POST
def revoke_permission(request, document_id, user_id):
    document = get_object_or_404(
        Document,
        id=document_id,
        owner=request.user,
    )

    grant = get_object_or_404(
        DocumentGrant,
        document=document,
        user_id=user_id,
    )

    target_username = grant.user.username
    previous_permission = grant.permission

    with transaction.atomic():
        record_audit(
            request.user,
            document,
            "permission_revoke",
            "success",
            {
                "target_username": target_username,
                "previous_permission": previous_permission,
            },
        )

        grant.delete()

    return redirect("dashboard")


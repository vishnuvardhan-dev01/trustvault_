from django.contrib import admin

from .models import Document, DocumentGrant, AuditEvent


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "category", "created_at")
    search_fields = ("title", "category", "owner__username")
    list_filter = ("category", "created_at")
    ordering = ("-created_at",)


@admin.register(DocumentGrant)
class DocumentGrantAdmin(admin.ModelAdmin):
    list_display = ("document", "user", "permission", "granted_at")
    search_fields = ("document__title", "user__username")
    list_filter = ("permission", "granted_at")
    autocomplete_fields = ("document", "user")  # optional: requires ModelAdmin.autocomplete_fields setup


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "document",
        "action",
        "outcome",
        "timestamp",
    )
    search_fields = (
        "actor__username",
        "document__title",
        "action",
        "outcome",
    )
    list_filter = ("action", "outcome", "timestamp")
    date_hierarchy = "timestamp"

    # Keep audit records read-only
    readonly_fields = (
        "actor",
        "document",
        "action",
        "outcome",
        "timestamp",
        "details",
        "previous_hash",
        "event_hash",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Returning False here also hides the edit links in the changelist.
        return False

    def has_delete_permission(self, request, obj=None):
        return False
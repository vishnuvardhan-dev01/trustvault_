
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_documents"
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class DocumentGrant(models.Model):
    READ = "read"
    EDIT = "edit"

    PERMISSION_CHOICES = [
        (READ, "Read"),
        (EDIT, "Edit"),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="grants"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="document_grants"
    )
    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "user"],
                name="unique_document_user_grant"
            )
        ]

class AuditEvent(models.Model):
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=50)
    outcome = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    previous_hash = models.CharField(max_length=64, blank=True)
    event_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["-timestamp", "-id"]

from .models import DocumentGrant


def can_read_document(user, document):
    """
    Check whether a user has permission to read a document.

    The document owner can always read their own document.
    Users with READ or EDIT permission can read shared documents.
    Unauthenticated and unauthorized users are denied access.
    """

    if not user.is_authenticated:
        return False

    # Document owners can read their own documents.
    if document.owner_id == user.id:
        return True

    # Users with READ or EDIT permission can read the document.
    return DocumentGrant.objects.filter(
        document=document,
        user=user,
        permission__in=[
            DocumentGrant.READ,
            DocumentGrant.EDIT,
        ],
    ).exists()


def can_edit_document(user, document):
    """
    Check whether a user has permission to edit a document.

    The owner can edit their own document.
    Other users need explicit EDIT permission.
    """

    if not user.is_authenticated:
        return False

    # Document owners can edit their own documents.
    if document.owner_id == user.id:
        return True

    # Other users must have EDIT permission.
    return DocumentGrant.objects.filter(
        document=document,
        user=user,
        permission=DocumentGrant.EDIT,
    ).exists()


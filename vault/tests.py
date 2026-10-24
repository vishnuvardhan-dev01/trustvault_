
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Document, DocumentGrant
from .permissions import can_read_document, can_edit_document


class DocumentPermissionTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="TestPass123!"
        )
        self.reader = User.objects.create_user(
            username="reader",
            password="TestPass123!"
        )
        self.unauthorized = User.objects.create_user(
            username="outsider",
            password="TestPass123!"
        )

        self.document = Document.objects.create(
            owner=self.owner,
            title="Test Document",
            category="Testing",
            file=SimpleUploadedFile(
                "test.txt",
                b"TrustVault test content",
                content_type="text/plain",
            ),
        )

    def test_owner_can_read_and_edit(self):
        self.assertTrue(can_read_document(self.owner, self.document))
        self.assertTrue(can_edit_document(self.owner, self.document))

    def test_reader_can_read_but_not_edit(self):
        DocumentGrant.objects.create(
            document=self.document,
            user=self.reader,
            permission=DocumentGrant.READ,
        )

        self.assertTrue(can_read_document(self.reader, self.document))
        self.assertFalse(can_edit_document(self.reader, self.document))

    def test_unauthorized_user_cannot_read_or_edit(self):
        self.assertFalse(
            can_read_document(self.unauthorized, self.document)
        )
        self.assertFalse(
            can_edit_document(self.unauthorized, self.document)
        )

    def test_reader_can_download(self):
        DocumentGrant.objects.create(
            document=self.document,
            user=self.reader,
            permission=DocumentGrant.READ,
        )

        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "download_document",
                args=[self.document.id],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_cannot_download(self):
        self.client.force_login(self.unauthorized)

        response = self.client.get(
            reverse(
                "download_document",
                args=[self.document.id],
            )
        )

        self.assertEqual(response.status_code, 403)


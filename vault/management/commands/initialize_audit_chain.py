
import hashlib
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from vault.models import AuditEvent


class Command(BaseCommand):
    help = "Rebuild the audit hash chain for existing events"

    def handle(self, *args, **options):
        with transaction.atomic():
            events = list(
                AuditEvent.objects.select_for_update().order_by("id")
            )

            previous_hash = "0" * 64

            for event in events:
                payload = {
                    "actor_id": event.actor_id,
                    "document_id": event.document_id,
                    "action": event.action,
                    "outcome": event.outcome,
                    "timestamp": event.timestamp.isoformat(),
                    "details": event.details,
                    "previous_hash": previous_hash,
                }

                event_hash = hashlib.sha256(
                    json.dumps(
                        payload,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest()

                event.previous_hash = previous_hash
                event.event_hash = event_hash

                event.save(
                    update_fields=["previous_hash", "event_hash"]
                )

                previous_hash = event_hash

        self.stdout.write(
            self.style.SUCCESS(
                f"Rebuilt the audit chain for {len(events)} events."
            )
        )


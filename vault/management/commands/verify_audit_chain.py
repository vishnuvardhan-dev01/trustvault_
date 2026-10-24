
import hashlib
import json

from django.core.management.base import BaseCommand
from vault.models import AuditEvent


class Command(BaseCommand):
    help = "Verify the integrity of the TrustVault audit hash chain"

    def handle(self, *args, **options):
        events = list(AuditEvent.objects.order_by("id"))

        if not events:
            self.stdout.write(self.style.SUCCESS("No audit events to verify."))
            return

        # Legacy records may have been created before hashing was implemented.
        first = events[0]

        if not first.previous_hash and not first.event_hash:
            self.stderr.write(
                self.style.ERROR(
                    f"Audit event {first.id} has no hashes. "
                    "Legacy audit records need a safe migration before verification."
                )
            )
            return

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

            expected_hash = hashlib.sha256(
                json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()

            if event.previous_hash != previous_hash:
                self.stderr.write(
                    self.style.ERROR(
                        f"CHAIN LINK ERROR at event ID {event.id}"
                    )
                )
                return

            if event.event_hash != expected_hash:
                self.stderr.write(
                    self.style.ERROR(
                        f"HASH MISMATCH at event ID {event.id}"
                    )
                )
                return

            previous_hash = event.event_hash

        self.stdout.write(
            self.style.SUCCESS(
                f"Audit chain verified successfully. Events checked: {len(events)}"
            )
        )


import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


LOG_FILE = Path(
    "logs/agent_events.jsonl"
)


class RunTracker:
    """Collect lightweight run telemetry."""

    def __init__(self):
        self.run_id = str(
            uuid.uuid4()
        )

        self.start_time = (
            time.perf_counter()
        )

    def finish(
        self,
        mode: str,
        status: str,
        evidence_count: int,
        provider_error: str | None = None,
    ) -> dict:

        duration = (
            time.perf_counter()
            - self.start_time
        )

        event = {
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "run_id": self.run_id,
            "mode": mode,
            "status": status,
            "duration_seconds": round(
                duration,
                3,
            ),
            "evidence_count": (
                evidence_count
            ),
            "fallback_used": (
                mode
                == "deterministic_fallback"
            ),
            "provider_error": (
                provider_error
            ),
        }

        LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with LOG_FILE.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                )
                + "\n"
            )

        return event
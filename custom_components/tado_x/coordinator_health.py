"""Local, per-home refresh diagnostics; no API access."""
from datetime import datetime, timezone
from time import monotonic


class CoordinatorHealth:
    def __init__(self):
        self.started = monotonic()
        self.last_success = None
        self.last_success_at = None
        self.last_attempt_at = None
        self.attempt_started = None
        self.duration = None
        self.outcome = "initialising"
        self.successes = self.failures = self.consecutive_failures = 0
        self.error = None
        self.optional_errors = {}
        self.command_sequence = 0
        self.command_attempt_sequence = 0
        self.command_requested_at = None
        self.command_completed_at = None
        self.command_outcome = None
        self.command_pending = False

    def request_command_refresh(self):
        self.command_sequence += 1
        self.command_requested_at = datetime.now(timezone.utc).isoformat()
        self.command_completed_at = None
        self.command_outcome = "pending"
        self.command_pending = True
        return self.command_sequence

    def command_request_failed(self, sequence):
        if self.command_pending and sequence == self.command_sequence:
            self.command_pending = False
            self.command_outcome = "error"
            self.command_completed_at = datetime.now(timezone.utc).isoformat()


    def begin(self):
        self.command_attempt_sequence = self.command_sequence
        self.attempt_started = monotonic()
        self.last_attempt_at = datetime.now(timezone.utc).isoformat()

    def finish(self, outcome, error=None):
        self.duration = round(monotonic() - self.attempt_started, 3)
        self.attempt_started = None
        self.outcome = outcome
        self.error = error
        if (self.command_pending and self.command_attempt_sequence == self.command_sequence):
            self.command_pending = False
            self.command_completed_at = datetime.now(timezone.utc).isoformat()
            self.command_outcome = "degraded" if outcome == "success" and self.optional_errors else outcome
        if outcome == "success":
            self.last_success = monotonic()
            self.last_success_at = datetime.now(timezone.utc).isoformat()
            self.successes += 1
            self.consecutive_failures = 0
        elif outcome != "cancelled":
            self.failures += 1
            self.consecutive_failures += 1

    def state(self, interval):
        if self.outcome in ("rate_limited", "authentication_required"):
            return self.outcome
        if monotonic() - (self.last_success if self.last_success is not None else self.started) >= max(90, 3 * interval):
            return "stale"
        if self.outcome == "error":
            return "error"
        if self.last_success is None:
            return "initialising"
        return "degraded" if self.optional_errors else "healthy"

    def attributes(self, interval):
        return {
            "last_successful_refresh": self.last_success_at,
            "last_attempted_refresh": self.last_attempt_at,
            "last_refresh_duration_seconds": self.duration,
            "last_refresh_outcome": self.outcome,
            "consecutive_failures": self.consecutive_failures,
            "successful_refreshes": self.successes,
            "failed_refreshes": self.failures,
            "failed_optional_datasets": dict(self.optional_errors),
            "last_error_type": self.error,
            "polling_interval_seconds": interval,
            "staleness_threshold_seconds": max(90, 3 * interval),
            "last_command_refresh_requested": self.command_requested_at,
            "last_command_refresh_completed": self.command_completed_at,
            "last_command_refresh_outcome": self.command_outcome,
            "command_refresh_pending": self.command_pending,
            "refresh_in_progress": self.attempt_started is not None,
        }

"""Home-scoped holiday state, refresh scheduling and safe activation."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from homeassistant.helpers.event import async_track_point_in_utc_time, async_track_time_interval
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.astimezone(timezone.utc) if result.tzinfo else None
    except ValueError:
        return None


class HolidayModeManager:
    """Maintain a single holiday snapshot per Tado home."""

    def __init__(self, hass, coordinator, interval: int) -> None:
        self.hass = hass
        self.coordinator = coordinator
        self.interval = max(900, int(interval))
        self.data: dict[str, Any] | None = None
        self._unsub_periodic = None
        self._unsub_events = []
        self._lock = asyncio.Lock()

    @property
    def status(self) -> str | None:
        data = self.data
        if not isinstance(data, dict) or not isinstance(data.get("enabled"), bool):
            return None
        if not data["enabled"]:
            return "off"
        now = dt_util.utcnow()
        start, end = parse_time(data.get("startDate")), parse_time(data.get("endDate"))
        if start is None or end is None or end <= start:
            return None
        if start > now:
            return "scheduled"
        if end <= now:
            return "ended"
        # The API active flag can lag a scheduled transition; the known
        # date interval determines the effective status between refreshes.
        return "active"

    async def start(self) -> None:
        try:
            await self.refresh()
        except Exception as err:  # Holiday API may not be available on every account.
            _LOGGER.warning("Holiday mode initial read failed for home %s: %s", self.coordinator.home_id, err)
        self._unsub_periodic = async_track_time_interval(
            self.hass, self._periodic, timedelta(seconds=self.interval)
        )

    async def _periodic(self, now) -> None:
        try:
            await self.refresh()
        except Exception as err:
            _LOGGER.warning("Holiday mode refresh failed for home %s: %s", self.coordinator.home_id, err)

    async def refresh(self) -> None:
        async with self._lock:
            data = await self.coordinator.api.get_holiday_mode()
            if not isinstance(data, dict) or "enabled" not in data:
                raise ValueError("Holiday mode API response is incomplete")
            self.data = data
            self._schedule_events()
            self.coordinator.async_update_listeners()

    def _schedule_events(self) -> None:
        for unsubscribe in self._unsub_events:
            unsubscribe()
        self._unsub_events.clear()
        if not self.data or not self.data.get("enabled"):
            return
        now = dt_util.utcnow()
        for field in ("startDate", "endDate"):
            when = parse_time(self.data.get(field))
            if when and when > now:
                self._unsub_events.append(async_track_point_in_utc_time(self.hass, self._at_boundary, when))

    async def _at_boundary(self, now) -> None:
        # Notify entities promptly, even if the confirming API request fails.
        self.coordinator.async_update_listeners()
        await self._periodic(now)
        await self.coordinator.async_request_refresh()

    async def set_enabled(self, enabled: bool) -> None:
        # Always obtain the latest settings before a read-modify-write.
        current = await self.coordinator.api.get_holiday_mode()
        if not isinstance(current, dict) or not isinstance(current.get("roomSettings"), dict):
            raise ValueError("Cannot safely modify holiday mode without its existing room settings")
        start = end = None
        if enabled:
            stored_start = parse_time(current.get("startDate"))
            stored_end = parse_time(current.get("endDate"))
            now = dt_util.utcnow()
            if not stored_start or not stored_end or stored_end <= now or stored_end <= stored_start:
                start_dt = now.replace(microsecond=0) - timedelta(seconds=1)
                end_dt = start_dt + timedelta(days=7)
                start = start_dt.isoformat(timespec="seconds").replace("+00:00", "Z")
                end = end_dt.isoformat(timespec="seconds").replace("+00:00", "Z")
        await self.coordinator.api.set_holiday_mode(enabled, start, end)
        await self.refresh()
        await self.coordinator.async_request_refresh()

    def stop(self) -> None:
        if self._unsub_periodic:
            self._unsub_periodic()
            self._unsub_periodic = None
        for unsubscribe in self._unsub_events:
            unsubscribe()
        self._unsub_events.clear()

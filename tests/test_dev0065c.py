"""Test request attribution and wrapper with no HA or network."""
import ast
import asyncio
import logging
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
root = Path(__file__).resolve().parents[1] / 'custom_components/tado_x'
exec((root/'coordinator_health.py').read_text())
h = CoordinatorHealth(); other = CoordinatorHealth()
h.begin(); h.request_command_refresh(); h.finish('success')
assert h.command_pending  # already-running cycle cannot confirm later command
h.begin(); h.finish('success'); assert h.command_outcome == 'success' and not h.command_pending
h.request_command_refresh(); h.request_command_refresh(); h.begin(); h.finish('success')
assert h.command_outcome == 'success' and not h.command_pending
for outcome in ('error','rate_limited','authentication_required','cancelled','success'):
    h.request_command_refresh(); h.begin(); h.optional_errors = {'weather':'Error'}
    h.finish(outcome); assert h.command_outcome == ('degraded' if outcome == 'success' else outcome)
    assert not h.command_pending and h.command_completed_at
assert other.command_outcome is None
h.request_command_refresh(); h.begin(); h.request_command_refresh(); h.finish('success'); assert h.command_pending
h.begin(); h.finish('success'); assert not h.command_pending
_LOGGER = logging.getLogger(__name__)
method = next(n for c in ast.parse((root/'coordinator.py').read_text()).body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='async_request_command_refresh')
exec(compile(ast.Module(body=[method],type_ignores=[]),'wrapper','exec'))
async def main():
    c = SimpleNamespace(home_id=1,health=CoordinatorHealth(),async_request_refresh=AsyncMock())
    await async_request_command_refresh(c)
    assert c.health.command_pending and c.async_request_refresh.await_count == 1
    c.health.begin(); c.health.finish('success'); assert not c.health.command_pending
    c.async_request_refresh.side_effect = RuntimeError('test')
    await async_request_command_refresh(c)
    assert c.health.command_outcome == 'error' and not c.health.command_pending
    assert c.async_request_refresh.await_count == 2
asyncio.run(main())
print('DEV-006.5C attribution and wrapper tests passed')

"""Standalone health state tests (no Home Assistant or network)."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('health', Path(__file__).resolve().parents[1] / 'custom_components/tado_x/coordinator_health.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
with patch.object(m, 'monotonic', return_value=100) as clock:
    h = m.CoordinatorHealth(); other = m.CoordinatorHealth()
    assert h.state(30) == 'initialising'
    h.begin(); assert h.attributes(30)['refresh_in_progress']
    clock.return_value = 101; h.finish('success'); assert h.state(30) == 'healthy'
    h.optional_errors['weather'] = 'Error'; assert h.state(30) == 'degraded'
    h.begin(); h.finish('rate_limited'); assert h.state(30) == 'rate_limited' and h.last_success == 101
    h.begin(); h.finish('error'); assert h.state(30) == 'error'
    clock.return_value = 192; assert h.state(30) == 'stale'; assert h.state(60) == 'error'
    h.begin(); h.optional_errors.clear(); h.finish('success'); assert h.state(30) == 'healthy'
    assert h.successes == 2 and h.failures == 2 and h.consecutive_failures == 0
    assert other.successes == 0
    h.begin(); h.finish('authentication_required'); assert h.state(30) == 'authentication_required'
print('Health state checks passed')

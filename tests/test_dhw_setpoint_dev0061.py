"""Standalone DEV-006.1 checks; no Home Assistant or live Tado API required."""
import ast
import asyncio
import math
from pathlib import Path
from types import SimpleNamespace

root = Path(__file__).resolve().parents[1] / 'custom_components' / 'tado_x'

def method(file, cls, name):
    tree = ast.parse((root / file).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls)
    return next(n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)

def isolated_class(name, methods, ns):
    code = ast.fix_missing_locations(ast.Module(body=[ast.ClassDef(name=name, bases=[], keywords=[], body=methods, decorator_list=[])], type_ignores=[]))
    exec(compile(code, '<actual source methods>', 'exec'), ns)
    return ns[name]

class ApiError(Exception): pass
Api = isolated_class('Api', [method('api.py','TadoXApi','set_domestic_hot_water_temperature')], {'TadoXApiError':ApiError,'TADO_HOPS_API_URL':'https://hops.tado.com'})
calls=[]
async def request(*args, **kwargs): calls.append((args,kwargs))
a=Api();a._home_id=101;a._request=request
asyncio.run(a.set_domestic_hot_water_temperature(51))
assert calls==[(('POST','https://hops.tado.com/homes/101/programmer/domesticHotWater/manualControl'),{'json_data':{'setpoint':51}})]
a._home_id=None
try: asyncio.run(a.set_domestic_hot_water_temperature(51));assert False
except ApiError: pass

class HomeAssistantError(Exception): pass
Number=isolated_class('Number',[method('number.py','TadoXDhwSetpoint','async_set_native_value')],{'math':math,'HomeAssistantError':HomeAssistantError})
async def setpoint(v): calls.append(('write',v))
async def refresh(): calls.append(('refresh',))
n=Number();n.coordinator=SimpleNamespace(enable_hot_water=True,data=SimpleNamespace(dhw_setpoint_min=30,dhw_setpoint_max=65),api=SimpleNamespace(set_domestic_hot_water_temperature=setpoint),async_request_command_refresh=refresh)
asyncio.run(n.async_set_native_value(51.0));assert calls[-2:]==[('write',51),('refresh',)]
for invalid in (29,66,50.5,float('nan'),float('inf'),True):
    old=len(calls)
    try: asyncio.run(n.async_set_native_value(invalid));assert False,invalid
    except HomeAssistantError: pass
    assert len(calls)==old
n.coordinator.enable_hot_water=False
try: asyncio.run(n.async_set_native_value(51));assert False
except HomeAssistantError: pass

# Source-level invariants for home-scoped capability, feature flags and states.
coord=(root/'coordinator.py').read_text()
assert 'math.isfinite(value)' in coord and 'minimum <= current <= maximum' in coord
assert 'device.get("thermInterfaceType") == "OPENTHERM"' in coord
assert 'data.dhw_setpoint is not None' in coord
for platform in ('button.py','select.py'):
    s=(root/platform).read_text()
    assert 'coordinator.enable_hot_water' in s
    assert 'RegistryEntryDisabler.INTEGRATION' in s
    assert '_attr_entity_registry_enabled_default = False' in s
assert '"MANUAL_ON", "MANUAL_OFF"' in (root/'sensor.py').read_text()
assert '{coordinator.home_id}_dhw_setpoint' in (root/'number.py').read_text()
# Exercise the actual registry reconciliation condition for all three relay keys.
button_tree = ast.parse((root / 'button.py').read_text())
setup = next(n for n in button_tree.body if isinstance(n, ast.AsyncFunctionDef) and n.name == 'async_setup_entry')
relay_guard = next(n for n in ast.walk(setup) if isinstance(n, ast.If) and 'dhw_relay_actions_unverified' in ast.unparse(n.test))
compiled_guard = compile(ast.fix_missing_locations(ast.Expression(body=relay_guard.test)), '<relay guard>', 'eval')
keys = frozenset({'boost_hot_water', 'disable_hot_water', 'resume_hot_water_schedule'})
for key in keys:
    for disabled_by in (None, 'integration'):
        scope = {'coordinator': SimpleNamespace(enable_hot_water=True, home_id=101, data=SimpleNamespace(dhw_relay_actions_unverified=True)), 'entity_entry': SimpleNamespace(unique_id=f'101_{key}', disabled_by=disabled_by), '_RELAY_DHW_KEYS': keys}
        assert eval(compiled_guard, {'__builtins__': {'any': any}, **scope}), (key, disabled_by)
for unique_id in ('102_resume_hot_water_schedule', '101_resume_schedules'):
    scope['entity_entry'] = SimpleNamespace(unique_id=unique_id, disabled_by='integration')
    assert not eval(compiled_guard, {'__builtins__': {'any': any}, **scope}), unique_id

print('DEV-006.1 standalone checks passed (not Home Assistant integration tests)')

# Options reconciliation must not undo the platform default for this home.
flow = ast.parse((root/'config_flow.py').read_text())
fn = next(n for n in ast.walk(flow) if isinstance(n, ast.AsyncFunctionDef) and n.name == '_update_entity_states')
guard = next(n for n in ast.walk(fn) if isinstance(n, ast.If) and 'dhw_relay_actions_unverified' in ast.unparse(n.test))
expr = compile(ast.fix_missing_locations(ast.Expression(body=guard.test)), '<options guard>', 'eval')
for key in (*keys, 'dhw_mode'):
    scope = {'feature_flag':'enable_hot_water','feature_enabled':True,'coordinator':SimpleNamespace(home_id=101,data=SimpleNamespace(dhw_relay_actions_unverified=True)), 'entity_entry':SimpleNamespace(unique_id=f'101_{key}')}
    assert eval(expr,scope)
    scope['feature_enabled']=False
    assert not eval(expr,scope)
    scope['feature_enabled']=True
    scope['entity_entry'].unique_id=f'102_{key}'
    assert not eval(expr,scope)
print('Options reconciliation guard checks passed')

"""DEV-005 standalone simulated whole-home action tests; no Home Assistant or Tado API."""
import ast
import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

root = Path(__file__).resolve().parents[1]
source = (root/'custom_components/tado_x/__init__.py').read_text()
tree = ast.parse(source)
setup = next(n for n in tree.body if isinstance(n, ast.AsyncFunctionDef) and n.name == 'async_setup_entry')
functions = {n.name:n for n in setup.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
required = ('whole_home_rooms','run_whole_home','whole_home_profile_target','async_set_climate_timer_home','async_set_away_schedule_home','async_save_profile_home','async_restore_profile_home')
assert all(k in functions for k in required)
assert 'coordinator.configured_room_ids = frozenset(coordinator.data.rooms)' in source
manager = (root/'custom_components/tado_x/schedule_profiles.py').read_text()
assert 'async def restore(self, room_id, profile, *, use_default=False, refresh=True)' in manager
assert 'if refresh:' in manager

class HomeAssistantError(Exception):pass
class Log:
    def warning(self,*a):pass
    def info(self,*a):pass

class Manager:
    profiles={'1':{'Normal':{}},'2':{'Normal':{}},'3':{'Normal':{}}}
    def all_names(self):return ['Normal','Eco','Winter']

async def refresh():
    state['refresh']+=1

coordinator=SimpleNamespace(home_id='home-A',data=SimpleNamespace(rooms={
    1:SimpleNamespace(name='Office'),2:SimpleNamespace(name='Hall'),3:SimpleNamespace(name='Kitchen'),
    4:SimpleNamespace(name='New room')}),configured_room_ids=frozenset((1,2,3)),
    schedule_profile_manager=Manager(),async_request_refresh=refresh)
state={'refresh':0}
ns={'HomeAssistantError':HomeAssistantError,'_LOGGER':Log()}
module=ast.Module(body=[functions['whole_home_rooms'],functions['run_whole_home']],type_ignores=[])
exec(compile(ast.fix_missing_locations(module),'<DEV005 action helpers>','exec'),ns)

async def run():
    calls=[]
    async def apply(room):
        calls.append(room)
        if room==2:raise RuntimeError('simulated failure')
    try:
        await ns['run_whole_home'](coordinator,'test_bulk',apply,refresh=True)
    except HomeAssistantError as e:
        msg=str(e)
        assert '2 succeeded' in msg and '2 failed/skipped' in msg
        assert 'Hall' in msg and 'New room' in msg and 'reload' in msg
    else:raise AssertionError('Expected aggregate failure')
    assert calls==[1,2,3],calls
    assert state['refresh']==1
    coordinator.schedule_profile_manager.profiles['3'].pop('Normal')
    calls.clear()
    try:await ns['run_whole_home'](coordinator,'test_bulk',apply)
    except HomeAssistantError as e:assert 'initial Normal profile' in str(e)
    else:raise AssertionError('Expected skipped room')
    assert calls==[1,2]

asyncio.run(run())
for f in [root/'custom_components/tado_x/strings.json',*(root/'custom_components/tado_x/translations').glob('*.json')]:
    data=json.loads(f.read_text())
    assert all(name in data['services'] for name in ('set_climate_timer_home','set_away_schedule_home','save_schedule_profile_home','restore_schedule_profile_home'))
import yaml
services=yaml.safe_load((root/'custom_components/tado_x/services.yaml').read_text())
assert len(services)==25
print('PASS: DEV-005 mocked eligibility, sequential failure continuation, aggregation, single refresh, action/translation coverage')

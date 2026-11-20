"""Exercise actual coordinator methods with stub HA base and simulated API."""
import ast
import asyncio
import logging
import math
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable
from types import SimpleNamespace
from unittest.mock import AsyncMock
root = Path(__file__).resolve().parents[1] / 'custom_components/tado_x'
class TadoXApiError(Exception): pass
class TadoXAuthError(Exception): pass
class TadoXRateLimitError(TadoXApiError):
    reset_time = None
class ConfigEntryAuthFailed(Exception): pass
class UpdateFailed(Exception): pass
class DataUpdateCoordinator:
    def __class_getitem__(cls, item): return cls
TERMINATION_TIMER = 'TIMER'
DEFAULT_TIMER_DURATION_MINUTES = 30
DEFAULT_SUPPLEMENTARY_POLL_MULTIPLIER = 1
_LOGGER = logging.getLogger(__name__)
exec((root/'coordinator_health.py').read_text())
tree = ast.parse((root/'coordinator.py').read_text())
exec(compile(ast.fix_missing_locations(ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+[n for n in tree.body if isinstance(n,ast.ClassDef)],type_ignores=[])),str(root/'coordinator.py'),'exec'))
async def main():
    c = object.__new__(TadoXDataUpdateCoordinator)
    c.home_id=1; c.home_name='Test'; c.health=CoordinatorHealth(); c.data=None
    c._scan_interval=30; c.supplementary_poll_multiplier=1
    c._supplementary_cache={}; c._supplementary_last_success={}; c.room_control_defaults={}; c._save_api_stats_callback=None
    for feature in ('weather','hot_water','mobile_devices','running_times','air_comfort','flow_temp'):
        setattr(c,'enable_'+feature,True)
    outputs={'get_rooms':[{'id':1,'heatingPower':{'percentage':10}}], 'get_rooms_and_devices':{'rooms':[], 'otherDevices':[{'thermInterfaceType':'OPENTHERM'}]}, 'get_home_state':{'presence':'HOME'}, 'get_weather':{'outsideTemperature':{'celsius':12}}, 'get_domestic_hot_water_state':{'state':'BOOST','nextStateChange':'test','setpoint':51,'setpointConstraints':{'min':30,'max':65}}, 'get_mobile_devices':[{'id':1}], 'get_running_times':{'runningTimes':[{'zones':[{'id':1,'runningTimeInSeconds':30}]}]}, 'get_air_comfort':{'comfort':[{'roomId':1}]}, 'get_flow_temperature_optimization':{'maxFlowTemperature':40}}
    c.api=SimpleNamespace(**{k:AsyncMock(return_value=v) for k,v in outputs.items()}, **{k:None for k in ('api_calls_today','api_reset_time','api_last_reset','api_last_observed_at','has_auto_assist','api_quota_limit','api_quota_remaining','api_rolling_daily_usage')})
    c.holiday_mode_manager=SimpleNamespace(poll_enabled=True,refresh=AsyncMock(),data={'enabled':False})
    c.data=await c._async_update_data(); assert c.health.state(30)=='healthy'
    c.api.get_rooms.return_value=[{'id':1,'heatingPower':{'percentage':80}}]
    optional=list(outputs)[3:]
    for k in optional: getattr(c.api,k).side_effect=TadoXApiError('test')
    c.holiday_mode_manager.refresh.side_effect=TadoXApiError('test')
    c.data=await c._async_update_data(); assert c.data.rooms[1].heating_power==80 and c.health.state(30)=='degraded'
    assert len(c.health.optional_errors)==7
    assert c.data.weather.outdoor_temperature==12 and c.data.dhw_state=='BOOST' and 1 in c.data.mobile_devices
    assert (c.data.dhw_setpoint,c.data.dhw_setpoint_min,c.data.dhw_setpoint_max)==(51,30,65) and c.data.dhw_relay_actions_unverified
    assert c.data.rooms[1].running_time_today_seconds==30 and 1 in c.data.air_comfort and c.data.max_flow_temperature==40
    for k in optional: getattr(c.api,k).side_effect=None
    c.holiday_mode_manager.refresh.side_effect=None
    c.data=await c._async_update_data(); assert c.health.state(30)=='healthy'
    old=c.data; fresh=c.health.last_success
    for k in optional:
        getattr(c.api,k).side_effect=TadoXRateLimitError('test')
        result=await c._async_update_data(); assert result.rate_limited and result is not old and not old.rate_limited and c.health.last_success==fresh
        getattr(c.api,k).side_effect=TadoXAuthError('test')
        try: await c._async_update_data()
        except ConfigEntryAuthFailed: pass
        else: raise AssertionError('auth failure swallowed')
        getattr(c.api,k).side_effect=None
    c.api.get_rooms.side_effect=TadoXApiError('test')
    try: await c._async_update_data()
    except UpdateFailed: pass
    else: raise AssertionError('core failure swallowed')
asyncio.run(main())
# Test actual mandatory API methods against malformed top-level shapes.
methods=[n for c in ast.parse((root/'api.py').read_text()).body if isinstance(c,ast.ClassDef) and c.name=='TadoXApi' for n in c.body if isinstance(n,ast.AsyncFunctionDef) and n.name in ('get_rooms','get_rooms_and_devices','get_home_state')]
TADO_HOPS_API_URL=TADO_MY_API_URL='https://example.invalid'
exec(compile(ast.Module(body=methods,type_ignores=[]),'api methods','exec'))
async def shapes():
    for method,bad,good in [(get_rooms,{},[]),(get_rooms_and_devices,{}, {'rooms':[]}),(get_home_state,[],{'presence':None})]:
        obj=SimpleNamespace(_home_id=1,_request=AsyncMock(return_value=bad))
        try: await method(obj)
        except TadoXApiError: pass
        else: raise AssertionError('invalid shape accepted')
        obj._request.return_value=good; assert await method(obj)==good
asyncio.run(shapes())
print('DEV-006.5B simulated coordinator and response checks passed')

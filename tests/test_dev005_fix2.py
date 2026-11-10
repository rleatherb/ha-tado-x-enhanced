"""DEV-005 Fix 2 static and simulated checks (not a live HA test)."""
import ast
import json
from pathlib import Path
import yaml
root = Path(__file__).resolve().parents[1]
component = root / "custom_components/tado_x"
actions = yaml.safe_load((component / "services.yaml").read_text())
assert len(actions) == 25
for name, field in (("set_climate_timer", "temperature"), ("set_climate_timer_home", "temperature"), ("set_away_schedule", "away_temperature"), ("set_away_schedule_home", "away_temperature")):
    number = actions[name]["fields"][field]["selector"]["number"]
    assert number["step"] == 0.1, (name, number)
    if "away" in name:
        assert number["min"] == 5 and number["max"] == 30 and number["mode"] == "slider"
assert set(actions["set_hvac_mode_home"]["fields"]["hvac_mode"]["selector"]["select"]["options"]) == {"auto", "heat", "off"}
source = (component / "__init__.py").read_text()
tree = ast.parse(source)
setup = next(node for node in tree.body if isinstance(node, ast.AsyncFunctionDef) and node.name == "async_setup_entry")
fn = next(node for node in setup.body if isinstance(node, ast.AsyncFunctionDef) and node.name == "async_set_hvac_mode_home")
assert 'SERVICE_SET_HVAC_MODE_HOME' in source
assert 'resume_schedule' in ast.unparse(fn) and 'set_room_off' in ast.unparse(fn) and 'set_room_temperature' in ast.unparse(fn)
assert 'run_whole_home' in ast.unparse(fn)
sensor = (component / "sensor.py").read_text()
assert 'class TadoXHomeScheduleProfileSensor' in sensor
assert 'manager.listen(self.async_write_ha_state)' in sensor
assert 'if "Custom" in values' in sensor
for f in [component / "strings.json", *(component / "translations").glob("*.json")]:
    assert "set_hvac_mode_home" in json.loads(f.read_text())["services"]
print("PASS: DEV-005 Fix 2 selector, action, sensor and translation checks")

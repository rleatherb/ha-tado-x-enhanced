"""DEV-006.2 regression: depleted battery enum and translations.

Run from repository root: python -m unittest tests/test_depleted_battery_dev0062.py
Static source/translation validation; not a Home Assistant runtime test.
"""

import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "tado_x"
EXPECTED = ("normal", "low", "depleted")


class DepletedBatteryRegressionTests(unittest.TestCase):
    def test_battery_sensor_options_and_value_normalization(self):
        module = ast.parse((COMPONENT / "sensor.py").read_text(encoding="utf-8"))
        matches = []
        for node in ast.walk(module):
            if not isinstance(node, ast.Call):
                continue
            keys = {kw.arg: kw.value for kw in node.keywords}
            if not isinstance(keys.get("key"), ast.Constant):
                continue
            if keys["key"].value != "battery":
                continue
            matches.append(keys)
        self.assertEqual(len(matches), 1)
        options = ast.literal_eval(matches[0]["options"])
        self.assertEqual(options, list(EXPECTED))
        # The existing value function lowercases the API battery state.
        self.assertIn(".battery_state.lower()", ast.unparse(matches[0]["value_fn"]))
        self.assertEqual("DEPLETED".lower(), "depleted")

    def test_simulated_api_battery_states(self):
        """Execute the production value_fn with simulated API device data."""
        from types import SimpleNamespace

        module = ast.parse((COMPONENT / "sensor.py").read_text(encoding="utf-8"))
        descriptions = []
        for node in ast.walk(module):
            if isinstance(node, ast.Call):
                keys = {kw.arg: kw.value for kw in node.keywords}
                if isinstance(keys.get("key"), ast.Constant) and keys["key"].value == "battery":
                    descriptions.append(keys)
        self.assertEqual(len(descriptions), 1)
        description = descriptions[0]
        # Compile only the production lambda, avoiding Home Assistant imports.
        expression = ast.Expression(body=description["value_fn"])
        ast.fix_missing_locations(expression)
        value_fn = eval(compile(expression, str(COMPONENT / "sensor.py"), "eval"), {"__builtins__": {}})
        options = ast.literal_eval(description["options"])
        for api_state, expected in (
            ("NORMAL", "normal"),
            ("LOW", "low"),
            ("DEPLETED", "depleted"),
            (None, None),
        ):
            with self.subTest(api_state=api_state):
                actual = value_fn(SimpleNamespace(battery_state=api_state))
                self.assertEqual(actual, expected)
                if actual is not None:
                    self.assertIn(actual, options)

    def test_all_shipped_translations_define_every_battery_state(self):
        paths = [COMPONENT / "strings.json"]
        paths.extend(sorted((COMPONENT / "translations").glob("*.json")))
        self.assertGreaterEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text(encoding="utf-8"))
                states = data["entity"]["sensor"]["battery"]["state"]
                self.assertEqual(set(states), set(EXPECTED))
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in states.values()))


if __name__ == "__main__":
    unittest.main()

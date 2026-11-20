"""Static regression for DEV-006.2; no Home Assistant runtime required."""
import ast
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1] / "custom_components" / "tado_x"
class DepletedBatteryRegressionTests(unittest.TestCase):
    def test_battery_enum(self):
        tree = ast.parse((ROOT / "sensor.py").read_text(encoding="utf-8"))
        matches = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                kws = {kw.arg: kw.value for kw in node.keywords}
                if isinstance(kws.get("key"), ast.Constant) and kws["key"].value == "battery":
                    matches.append(kws)
        self.assertEqual(len(matches), 1)
        self.assertEqual(ast.literal_eval(matches[0]["options"]), ["normal", "low", "depleted"])
        self.assertIn("battery_state.lower()", ast.unparse(matches[0]["value_fn"]))
    def test_simulated_battery_states(self):
        from types import SimpleNamespace
        for filename, key, cases in (
            ('sensor.py', 'battery', [('NORMAL', 'normal'), ('LOW', 'low'), ('DEPLETED', 'depleted'), (None, None)]),
            ('binary_sensor.py', 'battery_low', [('NORMAL', False), ('LOW', True), ('DEPLETED', True), (None, None)]),
        ):
            tree = ast.parse((ROOT / filename).read_text(encoding='utf-8'))
            matches = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    kws = {kw.arg: kw.value for kw in node.keywords}
                    if isinstance(kws.get('key'), ast.Constant) and kws['key'].value == key:
                        matches.append(kws)
            self.assertEqual(len(matches), 1)
            expr = ast.Expression(body=matches[0]['value_fn'])
            ast.fix_missing_locations(expr)
            fn = eval(compile(expr, filename, 'eval'), {'__builtins__': {}})
            for raw, expected in cases:
                with self.subTest(filename=filename, raw=raw):
                    self.assertEqual(fn(SimpleNamespace(battery_state=raw)), expected)

    def test_translations(self):
        paths = [ROOT / "strings.json", *sorted((ROOT / "translations").glob("*.json"))]
        self.assertEqual(len(paths), 6)
        for path in paths:
            with self.subTest(path=path.name):
                states = json.loads(path.read_text(encoding="utf-8"))["entity"]["sensor"]["battery"]["state"]
                self.assertEqual(set(states), {"normal", "low", "depleted"})
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in states.values()))
if __name__ == "__main__":
    unittest.main()

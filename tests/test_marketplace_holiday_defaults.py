"""Static regression guard for Marketplace documentation and Holiday polling defaults."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_holiday_defaults():
    flow = (ROOT / "custom_components/tado_x/config_flow.py").read_text()
    setup = (ROOT / "custom_components/tado_x/__init__.py").read_text()
    assert "user_input.get(CONF_ENABLE_HOLIDAY_POLLING, has_auto_assist)" in flow
    assert "self.config_entry.data.get(CONF_ENABLE_HOLIDAY_POLLING, current_auto_assist)" in flow
    assert "entry.data.get(CONF_ENABLE_HOLIDAY_POLLING, has_auto_assist)" in setup
    assert "CONF_ENABLE_HOLIDAY_POLLING: enable_holiday_polling" in flow

def test_installation_safety():
    doc = (ROOT / "docs/INSTALLATION.md").read_text()
    for term in ("complete Home Assistant backup", "Delete and uninstall", "not a promise", "authorisation", "HACS", "Marketplace", "2700 seconds"):
        assert term.lower() in doc.lower(), term

if __name__ == "__main__":
    test_holiday_defaults()
    test_installation_safety()
    print("Marketplace/holiday defaults static checks passed")

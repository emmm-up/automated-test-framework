from framework.config.settings import Settings


def test_settings_get_returns_existing_value():
    assert Settings.get("BASE_URL") == Settings.BASE_URL


def test_settings_get_returns_default_for_missing_value():
    assert Settings.get("DOES_NOT_EXIST", "fallback") == "fallback"


def test_environment_helpers_are_mutually_readable(monkeypatch):
    monkeypatch.setattr(Settings, "APP_ENV", "test")

    assert Settings.is_test() is True
    assert Settings.is_dev() is False
    assert Settings.is_prod() is False

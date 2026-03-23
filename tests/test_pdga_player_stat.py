from datetime import datetime, timedelta
from unittest.mock import MagicMock
import pytest
from disc_score_bot.pdga.pdgaplayerstat import PdgaPlayerStat


# ---------------------------------------------------------------------------
# NotificationConfig
# ---------------------------------------------------------------------------

def test_pdgaconfig_module_does_not_exist_initially(new_pdga_cfg):
    assert new_pdga_cfg.module_exists() is False

def test_pdgaconfig_create_module(new_pdga_cfg):
    assert new_pdga_cfg.create_module() is True
    assert new_pdga_cfg.module_exists() is True

def test_pdgaconfig_upcoming_events_channel_id_is_none_before_set(new_pdga_cfg):
    new_pdga_cfg.create_module()
    assert new_pdga_cfg.get_upcoming_events_channel_id() is None

def test_pdgaconfig_new_pdga_approved_discs_channel_id_is_none_before_set(new_pdga_cfg):
    new_pdga_cfg.create_module()
    assert new_pdga_cfg.get_new_pdga_approved_discs_channel_id() is None

def test_pdgaconfig_set_and_get_upcoming_events_channel_id(new_pdga_cfg):
    channel_id = 123456789012345678
    assert new_pdga_cfg.set_upcoming_events_channel_id(channel_id) is True
    assert new_pdga_cfg.get_upcoming_events_channel_id() == channel_id

def test_pdgaconfig_set_and_get_new_pdga_approved_discs_channel_id(new_pdga_cfg):
    channel_id = 987654321987654321
    assert new_pdga_cfg.set_new_pdga_approved_discs_channel_id(channel_id) is True
    assert new_pdga_cfg.get_new_pdga_approved_discs_channel_id() == channel_id

def test_pdgaconfig_channels_are_independent(new_pdga_cfg):
    """Setting one channel ID should not affect the other."""
    new_pdga_cfg.set_upcoming_events_channel_id(111111111111111111)
    new_pdga_cfg.set_new_pdga_approved_discs_channel_id(999999999999999999)
    assert new_pdga_cfg.get_upcoming_events_channel_id() == 111111111111111111
    assert new_pdga_cfg.get_new_pdga_approved_discs_channel_id() == 999999999999999999

def test_pdgaconfig_update_channel_id(new_pdga_cfg):
    new_pdga_cfg.set_upcoming_events_channel_id(111111111111111111)
    new_pdga_cfg.set_upcoming_events_channel_id(999999999999999999)
    assert new_pdga_cfg.get_upcoming_events_channel_id() == 999999999999999999

def test_pdgaconfig_update_new_pdga_approved_discs_channel_id(new_pdga_cfg):
    new_pdga_cfg.set_new_pdga_approved_discs_channel_id(111111111111111111)
    new_pdga_cfg.set_new_pdga_approved_discs_channel_id(999999999999999999)
    assert new_pdga_cfg.get_new_pdga_approved_discs_channel_id() == 999999999999999999

def test_pdgaconfig_no_module_returns_none_channel(new_pdga_cfg):
    assert new_pdga_cfg.get_upcoming_events_channel_id() is None
    assert new_pdga_cfg.get_new_pdga_approved_discs_channel_id() is None


# ---------------------------------------------------------------------------
# PdgaPlayerStat._is_upcoming_soon
# ---------------------------------------------------------------------------

@pytest.fixture
def stat():
    # Use __new__ to skip __init__ so the task loop is never started
    instance = PdgaPlayerStat.__new__(PdgaPlayerStat)
    instance.bot = MagicMock()
    return instance


def make_event(date: datetime | None):
    event = MagicMock()
    event.date_start = date.strftime("%a, %b %d, %Y") if date else None
    return event


def test_is_upcoming_soon_within_window(stat):
    event = make_event(datetime.now() + timedelta(days=2))
    assert stat._is_upcoming_soon(event) is True

def test_is_upcoming_soon_today(stat):
    event = make_event(datetime.now())
    assert stat._is_upcoming_soon(event) is True

def test_is_upcoming_soon_exactly_on_boundary(stat):
    event = make_event(datetime.now() + timedelta(days=3))
    assert stat._is_upcoming_soon(event) is True

def test_is_upcoming_soon_outside_window(stat):
    event = make_event(datetime.now() + timedelta(days=4))
    assert stat._is_upcoming_soon(event) is False

def test_is_upcoming_soon_past_event(stat):
    event = make_event(datetime.now() - timedelta(days=1))
    assert stat._is_upcoming_soon(event) is False

def test_is_upcoming_soon_no_date(stat):
    event = make_event(None)
    assert stat._is_upcoming_soon(event) is False

def test_is_upcoming_soon_custom_days(stat):
    event = make_event(datetime.now() + timedelta(days=30))
    assert stat._is_upcoming_soon(event, days=31) is True
    assert stat._is_upcoming_soon(event, days=29) is False

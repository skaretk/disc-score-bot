import shutil
from pathlib import Path
import pytest
from disc_score_bot.config import Config, ClubPlayerConfig, UserConfig, NotificationConfig
from disc_score_bot.score import AliasConfig


def clean_test_config(cfg):
    """Remove config file and directories if they exist."""
    if getattr(cfg, "config", None):
        cfg.config.unlink(missing_ok=True)
    for attr in ("path", "cfg_path"):
        p = getattr(cfg, attr, None)
        if isinstance(p, Path) and p.exists():
            shutil.rmtree(p, ignore_errors=True)

@pytest.fixture
def cfg_factory(tmp_path):
    """Create any config type and ensure cleanup after test."""
    created = []

    def create(cls, name="new_server"):
        cfg = cls(name, tmp_path)
        clean_test_config(cfg)  # pre-clean
        created.append(cfg)
        return cfg

    yield create

    # Teardown all created configs
    for cfg in created:
        clean_test_config(cfg)

@pytest.fixture
def new_cfg(cfg_factory):
    """New Config"""
    return cfg_factory(Config)

@pytest.fixture
def example_cfg():
    """Fetch server_example Config"""
    return Config("server_example")

@pytest.fixture
def new_club_player_cfg(cfg_factory):
    """New Club Player Config"""
    return cfg_factory(ClubPlayerConfig)

@pytest.fixture
def example_club_player_cfg():
    """Fetch server_example Club Player Config"""
    return ClubPlayerConfig("server_example")

@pytest.fixture
def new_user_cfg(cfg_factory):
    """New User Config"""
    return cfg_factory(UserConfig)

@pytest.fixture
def example_user_cfg():
    """Fetch server_example User Config"""
    return UserConfig("server_example")

@pytest.fixture
def new_pdga_cfg(cfg_factory):
    """New NotificationConfig"""
    return cfg_factory(NotificationConfig)

@pytest.fixture
def new_alias_cfg(cfg_factory):
    """New Alias Config"""
    return cfg_factory(AliasConfig)

@pytest.fixture
def example_alias_cfg():
    """Fetch server_example Club Alias Config"""
    return AliasConfig("server_example")

import shutil
from pathlib import Path
import pytest
from disc_score_bot.config import Config, ClubPlayerConfig, DiscordUserConfig
from disc_score_bot.pdga.pdgaplayerconfig import PdgaPlayerConfig
from disc_score_bot.discgolfmetrix import DiscgolfmetrixConfig
from disc_score_bot.score import AliasConfig
from disc_score_bot.bag import BagConfig


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
    return cfg_factory(Config)

@pytest.fixture
def new_bag_cfg(cfg_factory):
    return cfg_factory(BagConfig)

@pytest.fixture
def example_bag_cfg():
    return BagConfig("server_example")

@pytest.fixture
def new_club_player_cfg(cfg_factory):
    return cfg_factory(ClubPlayerConfig)

@pytest.fixture
def example_club_player_cfg():
    return ClubPlayerConfig("server_example")

@pytest.fixture
def new_alias_cfg(cfg_factory):
    return cfg_factory(AliasConfig)

@pytest.fixture
def example_alias_cfg():
    return AliasConfig("server_example")

@pytest.fixture
def new_discord_user_cfg(cfg_factory):
    return cfg_factory(DiscordUserConfig)

@pytest.fixture
def example_discord_user_cfg():
    return DiscordUserConfig("server_example")

@pytest.fixture
def new_discgolfmetrix_cfg(cfg_factory):
    return cfg_factory(DiscgolfmetrixConfig)

@pytest.fixture
def example_discgolfmetrix_cfg():
    return DiscgolfmetrixConfig("server_example")

@pytest.fixture
def new_pdga_player_cfg(cfg_factory):
    return cfg_factory(PdgaPlayerConfig)

@pytest.fixture
def example_pdga_player_cfg():
    return PdgaPlayerConfig("server_example")

import pytest
from disc_score_bot.pdga.pdgaplayerconfig import PdgaPlayerConfig

@pytest.fixture
def example_cfg():
    return PdgaPlayerConfig("server_example")

@pytest.fixture
def new_cfg(tmp_path):
    """Create Pdga Player Config"""
    cfg = PdgaPlayerConfig("new_server", tmp_path)
    prepare_test_config(cfg)

    yield cfg

    clean_test_config(cfg)

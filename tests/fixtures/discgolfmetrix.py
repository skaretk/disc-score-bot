import pytest
from disc_score_bot.discgolfmetrix import DiscgolfmetrixConfig

@pytest.fixture
def example_cfg():
    return DiscgolfmetrixConfig("server_example")

@pytest.fixture
def new_cfg(tmp_path):
    """Create Discgolfmetrix Config"""
    cfg = DiscgolfmetrixConfig("new_server", tmp_path)
    prepare_test_config(cfg)

    yield cfg

    clean_test_config(cfg)

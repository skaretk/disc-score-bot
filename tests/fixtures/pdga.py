import pytest
from pdga.pdgaplayerconfig import PdgaPlayerConfig
from tests.fixtures.helpers import prepare_test_config, clean_test_config

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

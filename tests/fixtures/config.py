import pytest
from config import Config
from tests.fixtures.helpers import prepare_test_config, clean_test_config

@pytest.fixture
def example_cfg():
    """Return existing server_example"""
    return Config("server_example")

@pytest.fixture
def new_cfg(tmp_path):
    """Create cfg"""
    cfg = Config("new_server", tmp_path)
    prepare_test_config(cfg)

    yield cfg

    clean_test_config(cfg)

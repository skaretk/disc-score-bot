import pytest
from config import Config

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

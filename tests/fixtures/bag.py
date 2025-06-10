import pytest
from bag.bagconfig import BagConfig
from tests.fixtures.helpers import prepare_test_config, clean_test_config

@pytest.fixture
def example_cfg():
    """Fetch existing Bag Config"""
    return BagConfig("server_example")

@pytest.fixture
def new_cfg(tmp_path):
    """Create Bag Config"""
    cfg = BagConfig("new_server", tmp_path)
    prepare_test_config(cfg)

    yield cfg

    clean_test_config(cfg)

import pytest
from score.aliasconfig import AliasConfig
from tests.fixtures.helpers import prepare_test_config, clean_test_config

@pytest.fixture
def example_cfg():
    """Fetch existing Alias Config"""
    return AliasConfig("server_example")

@pytest.fixture
def new_cfg(tmp_path):
    """Create AliasConfig"""
    cfg = AliasConfig("new_server", tmp_path)
    prepare_test_config(cfg)

    yield cfg

    clean_test_config(cfg)

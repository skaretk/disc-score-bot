import sys
from pathlib import Path
from context import config
from config.config import Config
from tests.fixtures.helpers import prepare_test_config, clean_test_config
from fixtures.config import example_cfg, new_cfg
sys.path.insert(0, str(Path().cwd()))

def test_valid_config(example_cfg):
    """Valid Config"""
    assert example_cfg.path_exists() is True
    assert example_cfg.config_exists() is True
    assert example_cfg.read() is not None

def test_invalid_config(new_cfg):
    """Invalid Config"""
    assert new_cfg.path_exists() is False
    assert new_cfg.config_exists() is False
    assert new_cfg.read() is None

def test_config_module_exist(example_cfg):
    """Check module exist"""
    assert example_cfg.module_exists() is False

def test_config_create(new_cfg):
    """Create config"""
    assert new_cfg.create() is True

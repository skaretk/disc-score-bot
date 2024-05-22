import sys
from pathlib import Path
from context import config
from config.config import Config
from testhelpers import prepare_test_server, cleanup_test_server
sys.path.insert(0, str(Path().cwd()))

def test_valid_config():
    """Valid Config"""
    cfg = Config("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is True
    assert cfg.read() is not None

def test_invalid_config():
    """Invalid Config"""
    cfg = Config("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False
    assert cfg.read() is None

def test_config_module_exist():
    """Check module exist"""
    cfg = Config("server_example")
    assert cfg.module_exists() is False

def test_config_create():
    """Create config"""
    cfg = Config("new_server")
    prepare_test_server(cfg)
    assert cfg.create() is True
    cleanup_test_server(cfg)

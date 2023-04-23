import sys
from pathlib import Path
from context import config
from config.config import Config
sys.path.insert(0, str(Path().cwd()))

def test_config_exist():
    cfg = Config("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is False

def test_config_not_exist():
    cfg = Config("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False

def test_config_read():
    cfg = Config("server_example")
    assert cfg.read() is None

def test_config_read_not_exist():
    cfg = Config("wrong_server")
    assert cfg.read() is None

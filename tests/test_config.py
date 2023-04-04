import os
import sys
from context import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_config_exist():
    cfg = config.Config("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is False

def test_config_not_exist():
    cfg = config.Config("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False

def test_config_read():
    cfg = config.Config("server_example")
    assert cfg.read() is None

def test_config_read_not_exist():
    cfg = config.Config("wrong_server")
    assert cfg.read() is None

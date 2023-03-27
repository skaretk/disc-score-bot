import os
import sys
from context import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

from context import apis

def test_cfg_exist():
    cfg = config.Config("server_example")
    assert cfg.exists() is True
    assert cfg.json() is not None

def test_cfg_not_exist():
    cfg = config.Config("wrong_server")
    assert cfg.exists() is False
    assert cfg.json() is None
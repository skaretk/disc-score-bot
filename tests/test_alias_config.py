import json
import os
import sys
from context import score
from score.name import Name
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_alias_config_exist():
    cfg = score.AliasConfig("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is True

def test_alias_config_not_exist():
    cfg = score.AliasConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False
#
def test_alias_config_read():
    cfg = score.AliasConfig("server_example")
    assert cfg.read() is not None

def test_alias_config_read_not_exist():
    cfg = score.AliasConfig("wrong_server")
    assert cfg.read() is None

def test_alias_config_get_user_alias():
    cfg = score.AliasConfig("server_example")
    assert cfg.get_user_alias("uDisc name") is not None
    assert cfg.get_user_alias("uDisc league or tournament name") is not None
    assert cfg.get_user_alias("uDisc name 2") is not None
    assert cfg.get_user_alias("alias1") is not None
    assert cfg.get_user_alias("alias2") is not None
    assert cfg.get_user_alias("etc") is not None
    assert cfg.get_user_alias("wrong uDisc name") is None
    assert cfg.get_user_alias("uDisc name") is not None

def test_alias_config_add_modify_remove_alias_user():
    """Test to add, modify and remove player aliases"""
    cfg = score.AliasConfig("server_example")
    # add user and alias
    assert cfg.get_user_alias("test user") is None
    assert cfg.add_user_alias("test user", "test user alias") is True
    assert cfg.add_user_alias("test user", "test user alias 2") is True
    # Validate user and aliases is added
    assert cfg.get_user_alias("test user") is not None
    assert cfg.get_user_alias("test user alias") is not None
    assert cfg.get_user_alias("test user alias 2") is not None
    # Remove aliases
    assert cfg.remove_user_alias("test user", "test user alias") is True
    assert cfg.remove_user_alias("test user", "test user alias 2") is True
    assert cfg.get_user_alias("test user alias") is None
    assert cfg.get_user_alias("test user alias 2") is None
    # Remove user
    assert cfg.remove_user("test user")
    assert cfg.get_user_alias("test user") is None

import sys
from pathlib import Path
from context import score
from testhelpers import prepare_test_server, cleanup_test_server
from score.aliasconfig import AliasConfig
sys.path.insert(0, str(Path().cwd()))

def test_alias_valid_config():
    """Check and read a valid configuration"""
    cfg = AliasConfig("server_example")
    assert cfg.module_exists() is True
    assert cfg.read(AliasConfig.__name__) is not None

def test_alias_invlid_config():
    """Check unknown configuration"""
    cfg = AliasConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.module_exists() is False
    assert cfg.read(AliasConfig.__name__) is None
#
def test_alias_config_get_alias():
    """Check a valid alias"""
    cfg = AliasConfig("server_example")
    assert cfg.get_user_alias("uDisc name") is not None

def test_alias_config_get_user_alias():
    cfg = AliasConfig("server_example")
    assert cfg.get_user_alias("uDisc name") is not None
    assert cfg.get_user_alias("uDisc league or tournament name") is not None
    assert cfg.get_user_alias("uDisc name 2") is not None
    assert cfg.get_user_alias("alias1") is not None
    assert cfg.get_user_alias("alias2") is not None
    assert cfg.get_user_alias("etc") is not None
    assert cfg.get_user_alias("wrong uDisc name") is None

def test_alias_config_add_modify_remove_alias_user():
    """Test to add, modify and remove player aliases"""
    cfg = AliasConfig("server_example")
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

def test_alias_config_create():
    """Test to add, modify and remove a player"""
    cfg = AliasConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.add_user_alias("test user", "test user alias") is True
    assert cfg.get_user_alias("test user") is not None
    assert cfg.get_user_alias("test user alias") is not None
    # Cleanup
    cleanup_test_server(cfg)

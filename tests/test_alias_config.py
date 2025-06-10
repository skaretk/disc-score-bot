import sys
from pathlib import Path
from context import score
from fixtures.alias import new_cfg, example_cfg
from score.aliasconfig import AliasConfig
sys.path.insert(0, str(Path().cwd()))

def test_alias_valid_config(example_cfg):
    """Check and read a valid configuration"""
    assert example_cfg.module_exists() is True
    assert example_cfg.read(AliasConfig.__name__) is not None

def test_alias_invlid_config():
    """Check unknown configuration"""
    cfg = AliasConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.module_exists() is False
    assert cfg.read(AliasConfig.__name__) is None
#
def test_alias_config_get_alias(example_cfg):
    """Check a valid alias"""
    assert example_cfg.get_user_alias("uDisc name") is not None

def test_alias_config_get_user_alias(example_cfg):
    assert example_cfg.get_user_alias("uDisc name") is not None
    assert example_cfg.get_user_alias("uDisc league or tournament name") is not None
    assert example_cfg.get_user_alias("uDisc name 2") is not None
    assert example_cfg.get_user_alias("alias1") is not None
    assert example_cfg.get_user_alias("alias2") is not None
    assert example_cfg.get_user_alias("etc") is not None
    assert example_cfg.get_user_alias("wrong uDisc name") is None

def test_alias_config_add_modify_remove_alias_user(new_cfg):
    """Test to add, modify and remove player aliases"""
    # add user and alias
    assert new_cfg.get_user_alias("test user") is None
    assert new_cfg.add_user_alias("test user", "test user alias") is True
    assert new_cfg.add_user_alias("test user", "test user alias 2") is True
    # Validate user and aliases is added
    assert new_cfg.get_user_alias("test user") is not None
    assert new_cfg.get_user_alias("test user alias") is not None
    assert new_cfg.get_user_alias("test user alias 2") is not None
    # Remove aliases
    assert new_cfg.remove_user_alias("test user", "test user alias") is True
    assert new_cfg.remove_user_alias("test user", "test user alias 2") is True
    assert new_cfg.get_user_alias("test user alias") is None
    assert new_cfg.get_user_alias("test user alias 2") is None
    # Remove user
    assert new_cfg.remove_user("test user")
    assert new_cfg.get_user_alias("test user") is None

def test_alias_config_create(new_cfg):
    """Test to add, modify and remove a player"""
    assert new_cfg.add_user_alias("test user", "test user alias") is True
    assert new_cfg.get_user_alias("test user") is not None
    assert new_cfg.get_user_alias("test user alias") is not None

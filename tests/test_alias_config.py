from pathlib import Path
from disc_score_bot.score import AliasConfig

def test_alias_valid_config(example_alias_cfg):
    """Check and read a valid configuration"""
    assert example_alias_cfg.module_exists() is True
    assert example_alias_cfg.read(AliasConfig.__name__) is not None

def test_alias_invlid_config():
    """Check unknown configuration"""
    cfg = AliasConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.module_exists() is False
    assert cfg.read(AliasConfig.__name__) is None
#
def test_alias_config_get_alias(example_alias_cfg):
    """Check a valid alias"""
    assert example_alias_cfg.get_user_alias("uDisc name") is not None

def test_alias_config_get_user_alias(example_alias_cfg):
    assert example_alias_cfg.get_user_alias("uDisc name") is not None
    assert example_alias_cfg.get_user_alias("uDisc league or tournament name") is not None
    assert example_alias_cfg.get_user_alias("uDisc name 2") is not None
    assert example_alias_cfg.get_user_alias("alias1") is not None
    assert example_alias_cfg.get_user_alias("alias2") is not None
    assert example_alias_cfg.get_user_alias("etc") is not None
    assert example_alias_cfg.get_user_alias("wrong uDisc name") is None

def test_alias_config_add_modify_remove_alias_user(new_alias_cfg):
    """Test to add, modify and remove player aliases"""
    # add user and alias
    assert new_alias_cfg.get_user_alias("test user") is None
    assert new_alias_cfg.add_user_alias("test user", "test user alias") is True
    assert new_alias_cfg.add_user_alias("test user", "test user alias 2") is True
    # Validate user and aliases is added
    assert new_alias_cfg.get_user_alias("test user") is not None
    assert new_alias_cfg.get_user_alias("test user alias") is not None
    assert new_alias_cfg.get_user_alias("test user alias 2") is not None
    # Remove aliases
    assert new_alias_cfg.remove_user_alias("test user", "test user alias") is True
    assert new_alias_cfg.remove_user_alias("test user", "test user alias 2") is True
    assert new_alias_cfg.get_user_alias("test user alias") is None
    assert new_alias_cfg.get_user_alias("test user alias 2") is None
    # Remove user
    assert new_alias_cfg.remove_user("test user")
    assert new_alias_cfg.get_user_alias("test user") is None

def test_alias_config_create(new_alias_cfg):
    """Test to add, modify and remove a player"""
    assert new_alias_cfg.add_user_alias("test user", "test user alias") is True
    assert new_alias_cfg.get_user_alias("test user") is not None
    assert new_alias_cfg.get_user_alias("test user alias") is not None

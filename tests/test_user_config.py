from pathlib import Path
from disc_score_bot.config.userconfig import UserConfig, User

def test_userconfig_valid_config(example_user_cfg):
    """Check and read a valid configuration"""
    assert example_user_cfg.module_exists() is True
    assert example_user_cfg.read(UserConfig.__name__) is not None
    user = example_user_cfg.get_user_by_discord_id(123456789012345678)
    assert user is not None
    assert user['discord_id'] == 123456789012345678
    assert user['pdga_number'] == 12345
    assert user['discgolfmetrix_code'] == "metrix_code"
    assert user['bag_url'] == "https://www.discgolfbagbuilder.com/bags/testbag"

def test_userconfig_invalid_config():
    """Check if unknown configuration"""
    cfg = UserConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(UserConfig.__name__) is None
    assert cfg.get_user_by_discord_id(123456789012345678) is None
    assert cfg.get_user_by_pdga_number(12345) is None
    assert cfg.get_user_by_discgolfmetrix_code("metrix_code") is None

def test_userconfig_add_remove_user(new_user_cfg):
    """Add, modify and remove a user"""
    discord_id = 87654321987654321

    assert new_user_cfg.get_user_by_discord_id(discord_id) is None
    assert new_user_cfg.remove_user(discord_id) is False

    # Add
    written, modified = new_user_cfg.add_user(User(discord_id=discord_id))
    assert (written, modified) == (True, False)
    _user = new_user_cfg.get_user_by_discord_id(discord_id)
    assert _user is not None
    assert _user["discord_id"] == discord_id
    assert _user["pdga_number"] is None
    assert _user["discgolfmetrix_code"] is None
    assert _user["bag_url"] is None

    # Remove
    assert new_user_cfg.remove_user(discord_id) is True
    assert new_user_cfg.get_user_by_discord_id(discord_id) is None

def test_userconfig_add_user_pdga_number(new_user_cfg):
    """Add user with pdga number"""

def test_userconfig_modify_user_pdga_number(new_user_cfg):
    """Modify user with pdga number"""

def test_userconfig_add_user_discgolfmetrix_code(new_user_cfg):
    """Add user with discgolfmetrix_code"""

def test_userconfig_modify_user_discgolfmetrix_code(new_user_cfg):
    """Modify user with discgolfmetrix_code"""

def test_userconfig_add_user_bag_url(new_user_cfg):
    """Add user with bag url"""

def test_userconfig_modify_user_bag_url(new_user_cfg):
    """Modify user with bag url"""

def test_userconfig_config_create_module(new_user_cfg):
    """Add a new module to a server"""
    assert new_user_cfg.module_exists() is False
    assert new_user_cfg.create_module() is True
    assert new_user_cfg.module_exists() is True

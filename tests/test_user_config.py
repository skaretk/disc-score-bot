import pytest
from disc_score_bot.config.userconfig import UserConfig, User

def test_userconfig_valid_config(example_user_cfg):
    """Check and read a valid configuration"""
    assert example_user_cfg.module_exists() is True
    assert example_user_cfg.read(UserConfig.__name__) is not None
    user = example_user_cfg.get_user(123456789012345678)
    assert user is not None
    assert user.discord_id == 123456789012345678
    assert user.pdga_number == 12345
    assert user.discgolfmetrix_code == "metrix_code"
    assert user.bag_url == "https://www.discgolfbagbuilder.com/bags/testbag"

def test_userconfig_invalid_config():
    """Check if unknown configuration"""
    cfg = UserConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(UserConfig.__name__) is None
    assert cfg.get_user(123456789012345678) is None
    assert cfg.get_user_by_pdga_number(12345) is None
    assert cfg.get_user_by_discgolfmetrix_code("metrix_code") is None

def test_userconfig_config_create_module(new_user_cfg):
    """Add a new module to a server"""
    assert new_user_cfg.module_exists() is False
    assert new_user_cfg.create_module() is True
    assert new_user_cfg.module_exists() is True

def test_userconfig_add_remove_user(new_user_cfg):
    """Add, modify and remove a user"""
    discord_id = 87654321987654321

    assert new_user_cfg.get_user(discord_id) is None
    assert new_user_cfg.remove_user(discord_id) is False

    # Add
    written, modified = new_user_cfg.add_user(User(discord_id=discord_id))
    assert (written, modified) == (True, False)

    #Check
    user = new_user_cfg.get_user(discord_id)
    assert user is not None
    assert user.discord_id == discord_id
    assert user.pdga_number is None
    assert user.discgolfmetrix_code is None
    assert user.bag_url is None

    # Remove
    assert new_user_cfg.remove_user(discord_id) is True
    assert new_user_cfg.get_user(discord_id) is None

def test_user_invalid_discord_id_too_short():
    """Discord ID that is too short is invalid"""
    with pytest.raises(ValueError):
        User(discord_id=123456789012345)  # 15 digits

def test_user_invalid_discord_id_too_long():
    """Discord ID that is too long is invalid"""
    with pytest.raises(ValueError):
        User(discord_id=12345678901234567890123)  # 23 digits

def test_userconfig_add_user_pdga_number(new_user_cfg):
    """Add user with pdga number"""
    discord_id = 123456789012345678
    pdga_number = 12345

    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, pdga_number=pdga_number))
    assert (written, modified) == (True, False)

    user = new_user_cfg.get_user_by_pdga_number(pdga_number)
    assert user is not None
    assert user.discord_id == discord_id
    assert user.pdga_number == pdga_number

def test_userconfig_modify_user_pdga_number(new_user_cfg):
    """Modify user with pdga number"""
    discord_id = 123456789012345678
    pdga_number_1 = 12345
    pdga_number_2 = 54321

    # Add initial user
    new_user_cfg.add_user(User(discord_id=discord_id, pdga_number=pdga_number_1))

    # Modify PDGA number
    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, pdga_number=pdga_number_2))
    assert (written, modified) == (True, True)

    user = new_user_cfg.get_user_by_pdga_number(pdga_number_2)
    assert user is not None
    assert user.pdga_number == pdga_number_2

def test_userconfig_invalid_pdga_number_zero():
    """PDGA number 0 is invalid"""
    with pytest.raises(ValueError):
        User(discord_id=123456789012345678, pdga_number=0)

def test_userconfig_invalid_pdga_number_negative():
    """Negative PDGA number is invalid"""
    with pytest.raises(ValueError):
        User(discord_id=123456789012345678, pdga_number=-1)

def test_userconfig_invalid_pdga_number_too_high():
    """PDGA number 500000 is invalid"""
    with pytest.raises(ValueError):
        User(discord_id=123456789012345678, pdga_number=500000)

def test_userconfig_get_user_by_pdga_number_not_found(new_user_cfg):
    """get_user_by_pdga_number returns None when not found"""
    new_user_cfg.create_module()
    assert new_user_cfg.get_user_by_pdga_number(99999) is None

def test_userconfig_add_user_discgolfmetrix_code(new_user_cfg):
    """Add user with discgolfmetrix_code"""
    discord_id = 123456789012345678
    metrix_code = "test_code"

    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, discgolfmetrix_code=metrix_code))
    assert (written, modified) == (True, False)

    user = new_user_cfg.get_user_by_discgolfmetrix_code(metrix_code)
    assert user is not None
    assert user.discord_id == discord_id
    assert user.discgolfmetrix_code == metrix_code

def test_userconfig_modify_user_discgolfmetrix_code(new_user_cfg):
    """Modify discgolfmetrix_code for existing user"""
    discord_id = 123456789012345678
    code_1 = "code_one"
    code_2 = "code_two"

    new_user_cfg.add_user(User(discord_id=discord_id, discgolfmetrix_code=code_1))

    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, discgolfmetrix_code=code_2))
    assert (written, modified) == (True, True)

    user = new_user_cfg.get_user_by_discgolfmetrix_code(code_2)
    assert user is not None
    assert user.discgolfmetrix_code == code_2

def test_userconfig_get_user_by_discgolfmetrix_code_not_found(new_user_cfg):
    """get_user_by_discgolfmetrix_code returns None when not found"""
    new_user_cfg.create_module()
    assert new_user_cfg.get_user_by_discgolfmetrix_code("unknown_code") is None


def test_userconfig_add_user_bag_url(new_user_cfg):
    """Add user with bag url"""
    discord_id = 123456789012345678
    bag_url = "https://www.discgolfbagbuilder.com/bags/testbag"

    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, bag_url=bag_url))
    assert (written, modified) == (True, False)

    user = new_user_cfg.get_user(discord_id)
    assert user is not None
    assert user.bag_url == bag_url

def test_userconfig_modify_user_bag_url(new_user_cfg):
    """Modify bag_url for existing user"""
    discord_id = 123456789012345678
    url_1 = "https://www.discgolfbagbuilder.com/bags/bag1"
    url_2 = "https://www.discgolfbagbuilder.com/bags/bag2"

    new_user_cfg.add_user(User(discord_id=discord_id, bag_url=url_1))

    written, modified = new_user_cfg.add_user(User(discord_id=discord_id, bag_url=url_2))
    assert (written, modified) == (True, True)

    user = new_user_cfg.get_user(discord_id)
    assert user is not None
    assert user.bag_url == url_2

#from pathlib import Path
#from disc_score_bot.bag.bagconfig import BagConfig
#from disc_score_bot.bag.baguser import BagUser
#
#def test_bag_valid_config(example_bag_cfg):
#    """Check and read a valid configuration"""
#    assert example_bag_cfg.module_exists() is True
#    assert example_bag_cfg.read(BagConfig.__name__) is not None
#    assert example_bag_cfg.get_url(1) == "https://www.discgolfbagbuilder.com/bags/testbag"
#
#def test_bag_invalid_config():
#    """Check if unknown configuration"""
#    cfg = BagConfig("wrong_server")
#    assert cfg.module_exists() is False
#    assert cfg.read(BagConfig.__name__) is None
#
#def test_bag_config_create_module(new_bag_cfg):
#    """Add a new module to a server"""
#    assert new_bag_cfg.module_exists() is False
#    assert new_bag_cfg.create_module() is True
#    assert new_bag_cfg.module_exists() is True
#
#def test_bag_config_create_modify_remove(new_bag_cfg):
#    """Add a new server, add a user"""
#    assert new_bag_cfg.get_url(2) is None
#    assert new_bag_cfg.remove_user(2) is False
#    assert new_bag_cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbag2")) == (True, False)
#    assert new_bag_cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbag2"
#    assert new_bag_cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbagtest")) == (True, True)
#    assert new_bag_cfg.add_user(BagUser(3, "https://www.discgolfbagbuilder.com/bags/testbagtest_2")) == (True, False)
#    assert new_bag_cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbagtest"
#    assert new_bag_cfg.get_url(3) == "https://www.discgolfbagbuilder.com/bags/testbagtest_2"
#    assert new_bag_cfg.remove_user(2) is True
#    assert new_bag_cfg.remove_user(3) is True
#    assert new_bag_cfg.get_url(2) is None

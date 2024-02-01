import sys
from pathlib import Path
from context import bag, config
from bag.bagconfig import BagConfig
from bag.baguser import BagUser
from testhelpers import prepare_test_server, cleanup_test_server
sys.path.insert(0, str(Path().cwd()))

def test_bag_valid_config():
    """Check and read a valid configuration"""
    cfg = BagConfig("server_example")
    assert cfg.module_exists() is True
    assert cfg.read(BagConfig.__name__) is not None
    assert cfg.get_url(1) == "https://www.discgolfbagbuilder.com/bags/testbag"

def test_bag_invalid_config():
    """Check if unknown configuration"""
    cfg = BagConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(BagConfig.__name__) is None

def test_bag_config_add_modify_remove_player():
    """Test to add, modify and remove a users bag"""
    cfg = BagConfig("server_example")
    assert cfg.get_url(2) is None
    assert cfg.remove_user(2) is False
    assert cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbag2")) == (True, False)
    assert cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbagtest")) == (True, True)
    assert cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbagtest"
    assert cfg.remove_user(2) is True
    assert cfg.get_url(2) is None

def test_bag_config_create_module():
    """Add a new module to a server"""
    cfg = BagConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.module_exists() is False
    assert cfg.create_module() is True
    assert cfg.module_exists() is True
    # Cleanup
    cleanup_test_server(cfg)

def test_bag_config_create():
    """Add a new server, add a user"""
    cfg = BagConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.get_url(2) is None
    assert cfg.remove_user(2) is False
    assert cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbag2")) == (True, False)
    assert cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.add_user(BagUser(2, "https://www.discgolfbagbuilder.com/bags/testbagtest")) == (True, True)
    assert cfg.add_user(BagUser(3, "https://www.discgolfbagbuilder.com/bags/testbagtest_2")) == (True, False)
    assert cfg.get_url(2) == "https://www.discgolfbagbuilder.com/bags/testbagtest"
    assert cfg.get_url(3) == "https://www.discgolfbagbuilder.com/bags/testbagtest_2"
    assert cfg.remove_user(2) is True
    assert cfg.remove_user(3) is True
    assert cfg.get_url(2) is None
    # Cleanup
    cleanup_test_server(cfg)

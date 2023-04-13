import os
import sys
#from context import config
from context import bag
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_bag_config_exist():
    cfg = bag.BagConfig("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is True

def test_bag_config_not_exist():
    cfg = bag.BagConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False

def test_bag_config_read():
    cfg = bag.BagConfig("server_example")
    assert cfg.read() is not None

def test_bag_config_read_not_exist():
    cfg = bag.BagConfig("wrong_server")
    assert cfg.read() is None

def test_bag_config_get_player():
    cfg = bag.BagConfig("server_example")
    assert cfg.get_bag(1) == "https://www.discgolfbagbuilder.com/bags/testbag"

def test_bag_config_add_modify_remove_player():
    '''Test to add, modify and remove a player'''
    cfg = bag.BagConfig("server_example")
    assert cfg.get_bag(2) is None
    assert cfg.remove_bag(2) is False
    assert cfg.add_bag(2, "https://www.discgolfbagbuilder.com/bags/testbag2") is False
    assert cfg.get_bag(2) == "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.add_bag(2, "https://www.discgolfbagbuilder.com/bags/testbagtest") is True
    assert cfg.get_bag(2) == "https://www.discgolfbagbuilder.com/bags/testbagtest"
    assert cfg.remove_bag(2) is True
    assert cfg.get_bag(2) is None

def test_bag_config_create():
    '''Test to add, modify and remove a player'''
    cfg = bag.BagConfig("new_server")
    assert cfg.get_bag(2) is None
    assert cfg.remove_bag(2) is False
    assert cfg.add_bag(2, "https://www.discgolfbagbuilder.com/bags/testbag2") is False
    assert cfg.get_bag(2) == "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.add_bag(2, "https://www.discgolfbagbuilder.com/bags/testbagtest") is True
    assert cfg.get_bag(2) == "https://www.discgolfbagbuilder.com/bags/testbagtest"
    assert cfg.remove_bag(2) is True
    assert cfg.get_bag(2) is None
    # Cleanup
    os.remove(cfg.config)
    os.rmdir(cfg.path)

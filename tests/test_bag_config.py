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
    assert cfg.get_player_bag("TestPlayer") == "https://www.discgolfbagbuilder.com/bags/testbag"

def test_bag_config_add_modify_remove_player():
    '''Test to add, modify and remove a player'''
    cfg = bag.BagConfig("server_example")
    bag_url = "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.get_player_bag("TestPlayer2") is None
    assert cfg.remove_player_bag("TestPlayer2") is False
    assert cfg.add_player_bag("TestPlayer2", bag_url) is False
    assert cfg.get_player_bag("TestPlayer2") == bag_url
    assert cfg.add_player_bag("TestPlayer2", bag_url) is True
    assert cfg.get_player_bag("TestPlayer2") == bag_url
    assert cfg.remove_player_bag("TestPlayer2") is True
    assert cfg.get_player_bag("TestPlayer2") is None

def test_bag_config_create():
    '''Test to add, modify and remove a player'''
    cfg = bag.BagConfig("new_server")
    assert cfg.get_player_bag("TestPlayer2") is None
    assert cfg.remove_player_bag("TestPlayer2") is False
    bag_url = "https://www.discgolfbagbuilder.com/bags/testbag2"
    assert cfg.add_player_bag("TestPlayer2", bag_url) is False
    assert cfg.get_player_bag("TestPlayer2") == bag_url
    bag_url_test = "https://www.discgolfbagbuilder.com/bags/testbagtest"
    assert cfg.add_player_bag("TestPlayer2", bag_url_test) is True
    assert cfg.get_player_bag("TestPlayer2") == bag_url_test
    assert cfg.remove_player_bag("TestPlayer2") is True
    assert cfg.get_player_bag("TestPlayer2") is None
    # Cleanup
    os.remove(cfg.config)
    os.rmdir(cfg.path)

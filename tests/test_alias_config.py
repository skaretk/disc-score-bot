import os
import sys
from context import score
#from score.player import PlayerName
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
    player_name = cfg.get_user_alias("uDisc nickname")
    assert player_name is not None
    assert player_name.has_alias("uDisc league or tournament name") is True
    assert player_name.has_alias("wrong") is False
    player_name = cfg.get_user_alias("uDisc name")
    assert player_name is not None
    assert player_name.has_alias("alias1") is True
    assert player_name.has_alias("alias2") is True
    assert player_name.has_alias("etc") is True
    assert player_name.has_alias("alias3") is False

def test_alias_config_add_modify_remove_player():
    '''Test to add, modify and remove player aliases'''
    #cfg = config.AliasConfig("server_example")
    #bag_url = "https://www.discgolfbagbuilder.com/bags/james-conrad-2021-in-the-bag"
    #assert cfg.get_player_bag("James") is None
    #assert cfg.remove_player_bag("James") is False
    #assert cfg.add_player_bag("James", bag_url) is False
    #assert cfg.get_player_bag("James") == bag_url
    #assert cfg.add_player_bag("James", bag_url) is True
    #assert cfg.get_player_bag("James") == bag_url
    #assert cfg.remove_player_bag("James") is True
    #assert cfg.get_player_bag("James") is None

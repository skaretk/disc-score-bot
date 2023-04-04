import os
import sys
from context import discgolfmetrix
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_discgolfmetrix_config_exist():
    cfg = discgolfmetrix.DiscgolfmetrixConfig("server_example")
    assert cfg.config_exists() is True

def test_discgolfmetrix_config_not_exist():
    cfg = discgolfmetrix.DiscgolfmetrixConfig("wrong_server")
    assert cfg.config_exists() is False

def test_discgolfmetrix_config_read():
    cfg = discgolfmetrix.DiscgolfmetrixConfig("server_example")
    assert cfg.read() is not None

def test_discgolfmetrix_config_read_not_exist():
    cfg = discgolfmetrix.DiscgolfmetrixConfig("wrong_server")
    assert cfg.read() is None

def test_discgolfmetrix_config_get_player_code():
    cfg = discgolfmetrix.DiscgolfmetrixConfig("server_example")
    assert cfg.get_player_code('metrixuser') == "metrix_code"

def test_discgolfmetrix_config_add_modify_remove_player():
    '''Test to add, modify and remove a player'''

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
    assert cfg.get_code(1) == "metrix_code"

def test_discgolfmetrix_config_add_modify_remove_player():
    """Test to add, modify and remove a player"""
    cfg = discgolfmetrix.DiscgolfmetrixConfig("server_example")
    assert cfg.get_code(2) is None
    assert cfg.remove_code(2) is False
    assert cfg.add_code(2, "metrix_code2") is False
    assert cfg.get_code(2) == "metrix_code2"
    assert cfg.add_code(2, "metrix_code_test") is True
    assert cfg.get_code(2) == "metrix_code_test"
    assert cfg.remove_code(2) is True
    assert cfg.get_code(2) is None

def test_discgolfmetrix_config_create():
    """Test to add a new server, add a user"""
    cfg = discgolfmetrix.DiscgolfmetrixConfig("new_server")
    assert cfg.get_code(2) is None
    assert cfg.remove_code(2) is False
    assert cfg.add_code(2, "metrix_code2") is False
    assert cfg.get_code(2) == "metrix_code2"
    assert cfg.add_code(2, "metrix_code_test") is True
    assert cfg.get_code(2) == "metrix_code_test"
    assert cfg.remove_code(2) is True
    assert cfg.get_code(2) is None
    # Cleanup
    os.remove(cfg.config)
    os.rmdir(cfg.path)
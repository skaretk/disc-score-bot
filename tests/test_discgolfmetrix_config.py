from pathlib import Path
import sys
from context import discgolfmetrix
from discgolfmetrix.discgolfmetrixconfig import DiscgolfmetrixConfig
sys.path.insert(0, str(Path().cwd()))

def test_discgolfmetrix_config_exist():
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.config_exists() is True

def test_discgolfmetrix_config_not_exist():
    cfg = DiscgolfmetrixConfig("wrong_server")
    assert cfg.config_exists() is False

def test_discgolfmetrix_config_read():
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.read() is not None

def test_discgolfmetrix_config_read_not_exist():
    cfg = DiscgolfmetrixConfig("wrong_server")
    assert cfg.read() is None

def test_discgolfmetrix_config_get_player_code():
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.get_code(1) == "metrix_code"

def test_discgolfmetrix_config_add_modify_remove_player():
    """Test to add, modify and remove a player"""
    cfg = DiscgolfmetrixConfig("server_example")
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
    cfg = DiscgolfmetrixConfig("new_server")
    if cfg.config_exists():
        cfg.config.unlink()
        cfg.path.rmdir()
    assert cfg.get_code(2) is None
    assert cfg.remove_code(2) is False
    assert cfg.add_code(2, "metrix_code2") is False
    assert cfg.get_code(2) == "metrix_code2"
    assert cfg.add_code(2, "metrix_code_test") is True
    assert cfg.get_code(2) == "metrix_code_test"
    assert cfg.remove_code(2) is True
    assert cfg.get_code(2) is None
    # Cleanup
    cfg.config.unlink()
    cfg.path.rmdir()
from pathlib import Path
import sys
from context import config
from discgolfmetrix.discgolfmetrixconfig import DiscgolfmetrixConfig
from discgolfmetrix.discgolfmetrixuser import DiscgolfmetrixUser
from testhelpers import prepare_test_server, cleanup_test_server
sys.path.insert(0, str(Path().cwd()))

def test_discgolfmetrix_valid_config():
    """Check and read a valid configuration"""
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.module_exists() is True
    assert cfg.read(DiscgolfmetrixConfig.__name__) is not None

def test_discgolfmetrix_invalid_config():
    """Check unknown configuration"""
    cfg = DiscgolfmetrixConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(DiscgolfmetrixConfig.__name__) is None

def test_discgolfmetrix_config_get_code():
    """Check a valid code"""
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.get_code(1) == "metrix_code"

def test_discgolfmetrix_config_add_modify_remove_player():
    """Add, modify and remove a player"""
    cfg = DiscgolfmetrixConfig("server_example")
    assert cfg.get_code(2) is None
    assert cfg.remove_user(2) is False
    assert cfg.add_user(DiscgolfmetrixUser(2, "metrix_code2")) == (True, False)
    assert cfg.get_code(2) == "metrix_code2"
    assert cfg.add_user(DiscgolfmetrixUser(2, "metrix_code_test")) == (True, True)
    assert cfg.get_code(2) == "metrix_code_test"
    assert cfg.remove_user(2) is True
    assert cfg.get_code(2) is None

def test_discgolfmetrix_config_create_module():
    """Add a new module to a server"""
    cfg = DiscgolfmetrixConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.module_exists() is False
    assert cfg.create_module() is True
    assert cfg.module_exists() is True
    # Cleanup
    cleanup_test_server(cfg)

def test_discgolfmetrix_config_create():
    """Add a new server and add a user"""
    cfg = DiscgolfmetrixConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.get_code(2) is None
    assert cfg.remove_user(2) is False
    assert cfg.add_user(DiscgolfmetrixUser(2, "metrix_code2")) == (True, False)
    assert cfg.get_code(2) == "metrix_code2"
    assert cfg.add_user(DiscgolfmetrixUser(2, "metrix_code_test")) == (True, True)
    assert cfg.add_user(DiscgolfmetrixUser(3, "metrix_code_test_2")) == (True, False)
    assert cfg.get_code(2) == "metrix_code_test"
    assert cfg.get_code(3) == "metrix_code_test_2"
    assert cfg.remove_user(2) is True
    assert cfg.remove_user(3) is True
    assert cfg.get_code(2) is None
    # Cleanup
    cleanup_test_server(cfg)

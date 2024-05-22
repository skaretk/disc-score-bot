import sys
from pathlib import Path
from context import pdga
from pdga.pdgaplayerconfig import PdgaPlayerConfig
from pdga.pdgaplayer import PdgaPlayer
from testhelpers import prepare_test_server, cleanup_test_server
sys.path.insert(0, str(Path().cwd()))

def test_pdga_valid_config():
    """Check and read a valid configuration"""
    cfg = PdgaPlayerConfig("server_example")
    assert cfg.module_exists() is True
    assert cfg.read(PdgaPlayerConfig.__name__) is not None
    assert cfg.get_pdga_number(123456789012345678) == 12345

def test_pdga_invalid_config():
    """Check if unknown configuration"""
    cfg = PdgaPlayerConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(PdgaPlayerConfig.__name__) is None
    assert cfg.get_pdga_number(123456789012345678) is None

def test_pdga_config_add_modify_remove_player():
    """Add, modify and remove a pdga number"""
    cfg = PdgaPlayerConfig("server_example")
    assert cfg.get_pdga_number(876543210987654321) is None
    assert cfg.remove_user(876543210987654321) is False
    assert cfg.add_user(PdgaPlayer(876543210987654321, 87654)) == (True, False)
    assert cfg.get_pdga_number(876543210987654321) == 87654
    assert cfg.add_user(PdgaPlayer(876543210987654321, 23456)) == (True, True)
    assert cfg.get_pdga_number(876543210987654321) == 23456
    assert cfg.remove_user(876543210987654321) is True
    assert cfg.get_pdga_number(876543210987654321) is None

def test_pdga_config_create_module():
    """Add a new module to a server"""
    cfg = PdgaPlayerConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.module_exists() is False
    assert cfg.create_module() is True
    assert cfg.module_exists() is True
    # Cleanup
    cleanup_test_server(cfg)

def test_pdga_config_create():
    """Add a new server, add a user"""
    cfg = PdgaPlayerConfig("new_server")
    prepare_test_server(cfg)
    assert cfg.get_pdga_number(123456789012345678) is None
    assert cfg.remove_user(123456789012345678) is False
    assert cfg.add_user(PdgaPlayer(123456789012345678, 12345)) == (True, False)
    assert cfg.get_pdga_number(123456789012345678) == 12345
    assert cfg.add_user(PdgaPlayer(123456789012345678, 23456)) == (True, True)
    assert cfg.add_user(PdgaPlayer(876543210987654321, 87654)) == (True, False)
    assert cfg.get_pdga_number(123456789012345678) == 23456
    assert cfg.get_pdga_number(876543210987654321) == 87654
    assert cfg.remove_user(123456789012345678) is True
    assert cfg.remove_user(876543210987654321) is True
    assert cfg.get_pdga_number(123456789012345678) is None
    # Cleanup
    cleanup_test_server(cfg)

from pathlib import Path
import sys
from context import config
from discgolfmetrix.discgolfmetrixconfig import DiscgolfmetrixConfig
from discgolfmetrix.discgolfmetrixuser import DiscgolfmetrixUser
from fixtures.discgolfmetrix import new_cfg, example_cfg
from tests.fixtures.helpers import prepare_test_config
sys.path.insert(0, str(Path().cwd()))

def test_discgolfmetrix_valid_config(example_cfg):
    """Check and read a valid configuration"""
    assert example_cfg.module_exists() is True
    assert example_cfg.read(DiscgolfmetrixConfig.__name__) is not None

def test_discgolfmetrix_invalid_config():
    """Check unknown configuration"""
    cfg = DiscgolfmetrixConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(DiscgolfmetrixConfig.__name__) is None

def test_discgolfmetrix_config_get_code(example_cfg):
    """Check a valid code"""
    assert example_cfg.get_code(1) == "metrix_code"

def test_discgolfmetrix_config_add_modify_remove_player(example_cfg):
    """Add, modify and remove a player"""
    assert example_cfg.get_code(2) is None
    assert example_cfg.remove_user(2) is False
    assert example_cfg.add_user(DiscgolfmetrixUser(2, "metrix_code2")) == (True, False)
    assert example_cfg.get_code(2) == "metrix_code2"
    assert example_cfg.add_user(DiscgolfmetrixUser(2, "metrix_code_test")) == (True, True)
    assert example_cfg.get_code(2) == "metrix_code_test"
    assert example_cfg.remove_user(2) is True
    assert example_cfg.get_code(2) is None

def test_discgolfmetrix_config_create_module(new_cfg):
    """Add a new module to a server"""
    assert new_cfg.module_exists() is False
    assert new_cfg.create_module() is True
    assert new_cfg.module_exists() is True

def test_discgolfmetrix_config_create(new_cfg):
    """Add a new server and add a user"""
    assert new_cfg.get_code(2) is None
    assert new_cfg.remove_user(2) is False
    assert new_cfg.add_user(DiscgolfmetrixUser(2, "metrix_code2")) == (True, False)
    assert new_cfg.get_code(2) == "metrix_code2"
    assert new_cfg.add_user(DiscgolfmetrixUser(2, "metrix_code_test")) == (True, True)
    assert new_cfg.add_user(DiscgolfmetrixUser(3, "metrix_code_test_2")) == (True, False)
    assert new_cfg.get_code(2) == "metrix_code_test"
    assert new_cfg.get_code(3) == "metrix_code_test_2"
    assert new_cfg.remove_user(2) is True
    assert new_cfg.remove_user(3) is True
    assert new_cfg.get_code(2) is None

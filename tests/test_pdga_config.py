#from pathlib import Path
#from disc_score_bot.pdga.pdgaplayerconfig import PdgaPlayerConfig
#from disc_score_bot.pdga.pdgaplayer import PdgaPlayer
#
#def test_pdga_valid_config(example_pdga_player_cfg):
#    """Check and read a valid configuration"""
#    assert example_pdga_player_cfg.module_exists() is True
#    assert example_pdga_player_cfg.read(PdgaPlayerConfig.__name__) is not None
#    assert example_pdga_player_cfg.get_pdga_number(123456789012345678) == 12345
#
#def test_pdga_invalid_config():
#    """Check if unknown configuration"""
#    cfg = PdgaPlayerConfig("wrong_server")
#    assert cfg.module_exists() is False
#    assert cfg.read(PdgaPlayerConfig.__name__) is None
#    assert cfg.get_pdga_number(123456789012345678) is None
#
#def test_pdga_config_add_modify_remove_player(example_pdga_player_cfg):
#    """Add, modify and remove a pdga number"""
#    assert example_pdga_player_cfg.get_pdga_number(876543210987654321) is None
#    assert example_pdga_player_cfg.remove_user(876543210987654321) is False
#    assert example_pdga_player_cfg.add_user(PdgaPlayer(876543210987654321, 87654)) == (True, False)
#    assert example_pdga_player_cfg.get_pdga_number(876543210987654321) == 87654
#    assert example_pdga_player_cfg.add_user(PdgaPlayer(876543210987654321, 23456)) == (True, True)
#    assert example_pdga_player_cfg.get_pdga_number(876543210987654321) == 23456
#    assert example_pdga_player_cfg.remove_user(876543210987654321) is True
#    assert example_pdga_player_cfg.get_pdga_number(876543210987654321) is None
#
#def test_pdga_config_create_module(new_pdga_player_cfg):
#    """Add a new module to a server"""
#    assert new_pdga_player_cfg.module_exists() is False
#    assert new_pdga_player_cfg.create_module() is True
#    assert new_pdga_player_cfg.module_exists() is True
#
#def test_pdga_config_create(new_pdga_player_cfg):
#    """Add a new server, add a user"""
#    assert new_pdga_player_cfg.get_pdga_number(123456789012345678) is None
#    assert new_pdga_player_cfg.remove_user(123456789012345678) is False
#    assert new_pdga_player_cfg.add_user(PdgaPlayer(123456789012345678, 12345)) == (True, False)
#    assert new_pdga_player_cfg.get_pdga_number(123456789012345678) == 12345
#    assert new_pdga_player_cfg.add_user(PdgaPlayer(123456789012345678, 23456)) == (True, True)
#    assert new_pdga_player_cfg.add_user(PdgaPlayer(876543210987654321, 87654)) == (True, False)
#    assert new_pdga_player_cfg.get_pdga_number(123456789012345678) == 23456
#    assert new_pdga_player_cfg.get_pdga_number(876543210987654321) == 87654
#    assert new_pdga_player_cfg.remove_user(123456789012345678) is True
#    assert new_pdga_player_cfg.remove_user(876543210987654321) is True
#    assert new_pdga_player_cfg.get_pdga_number(123456789012345678) is None

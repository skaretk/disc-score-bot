from pathlib import Path
from disc_score_bot.config.clubplayerconfig import ClubPlayerConfig

def test_clubplayerconfig_valid_config(example_club_player_cfg):
    """Check and read a valid configuration"""
    assert example_club_player_cfg.module_exists() is True
    assert example_club_player_cfg.read(ClubPlayerConfig.__name__) is not None
    player1 = example_club_player_cfg.get_player(discord_id=123456789012345678)
    player2 = example_club_player_cfg.get_player(name="Ola Nordmann")
    player3 = example_club_player_cfg.get_player(pdga_number=12345)
    player4 = example_club_player_cfg.get_player(discgolfmetrix_id=123456789012345678)
    assert player1 is not None
    assert player1['discord_id'] == 123456789012345678
    assert player1['name'] == "Ola Nordmann"
    assert player1['pdga_number'] == 12345
    assert player1['discgolfmetrix_id'] == 123456789012345678
    assert player2 is not None
    assert player2['discord_id'] == 123456789012345678
    assert player2['name'] == "Ola Nordmann"
    assert player2['pdga_number'] == 12345
    assert player2['discgolfmetrix_id'] == 123456789012345678
    assert player3 is not None
    assert player3['discord_id'] == 123456789012345678
    assert player3['name'] == "Ola Nordmann"
    assert player3['pdga_number'] == 12345
    assert player3['discgolfmetrix_id'] == 123456789012345678
    assert player4 is not None
    assert player4['discord_id'] == 123456789012345678
    assert player4['name'] == "Ola Nordmann"
    assert player4['pdga_number'] == 12345
    assert player4['discgolfmetrix_id'] == 123456789012345678

def test_clubplayerconfig_invalid_config():
    """Check if unknown configuration"""
    cfg = ClubPlayerConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(ClubPlayerConfig.__name__) is None
    assert cfg.get_player(discord_id=123456789012345678) is None

def test_clubplayerconfig_config_add_modify_remove_player(example_club_player_cfg):
    """Add, modify and remove a pdga number"""
    assert example_club_player_cfg.get_pdga_number(876543210987654321) is None
    assert example_club_player_cfg.remove_user(876543210987654321) is False
    assert example_club_player_cfg.add_user(ClubPlayerConfig(876543210987654321, 87654)) == (True, False)
    assert example_club_player_cfg.get_player(876543210987654321) == 87654
    assert example_club_player_cfg.add_user(ClubPlayerConfig(876543210987654321, 23456)) == (True, True)
    assert example_club_player_cfg.get_pdga_number(876543210987654321) == 23456
    assert example_club_player_cfg.remove_user(876543210987654321) is True
    assert example_club_player_cfg.get_pdga_number(876543210987654321) is None

def test_clubplayerconfig_config_create_module(new_club_player_cfg):
    """Add a new module to a server"""
    assert new_club_player_cfg.module_exists() is False
    assert new_club_player_cfg.create_module() is True
    assert new_club_player_cfg.module_exists() is True

def test_clubplayerconfig_config_create(new_club_player_cfg):
    """Add a new server, add a user"""
    assert new_club_player_cfg.get_pdga_number(123456789012345678) is None
    assert new_club_player_cfg.remove_user(123456789012345678) is False
    assert new_club_player_cfg.add_user(ClubPlayerConfig(123456789012345678, 12345)) == (True, False)
    assert new_club_player_cfg.get_pdga_number(123456789012345678) == 12345
    assert new_club_player_cfg.add_user(ClubPlayerConfig(123456789012345678, 23456)) == (True, True)
    assert new_club_player_cfg.add_user(ClubPlayerConfig(876543210987654321, 87654)) == (True, False)
    assert new_club_player_cfg.get_pdga_number(123456789012345678) == 23456
    assert new_club_player_cfg.get_pdga_number(876543210987654321) == 87654
    assert new_club_player_cfg.remove_user(123456789012345678) is True
    assert new_club_player_cfg.remove_user(876543210987654321) is True
    assert new_club_player_cfg.get_pdga_number(123456789012345678) is None

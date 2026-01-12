from pathlib import Path
from disc_score_bot.config.clubplayerconfig import ClubPlayerConfig, Player

def test_clubplayerconfig_valid_config(example_club_player_cfg):
    """Check and read a valid configuration"""
    assert example_club_player_cfg.module_exists() is True
    assert example_club_player_cfg.read(ClubPlayerConfig.__name__) is not None
    player1 = example_club_player_cfg.get_player_by_pdga_number(12345)
    player2 = example_club_player_cfg.get_player_by_name("Ola Nordmann")
    player3 = example_club_player_cfg.get_player_by_discord_id(123456789012345678)
    player4 = example_club_player_cfg.get_player_by_discgolfmetrix_id(123456789012345678)
    assert player1 is not None
    assert player1['pdga_number'] == 12345
    assert player1['name'] == "Ola Nordmann"
    assert player1['discord_id'] == 123456789012345678
    assert player1['discgolfmetrix_id'] == 123456789012345678
    assert player2 is not None
    assert player2['pdga_number'] == 12345
    assert player2['name'] == "Ola Nordmann"
    assert player2['discord_id'] == 123456789012345678
    assert player2['discgolfmetrix_id'] == 123456789012345678
    assert player3 is not None
    assert player3['pdga_number'] == 12345
    assert player3['name'] == "Ola Nordmann"
    assert player3['discord_id'] == 123456789012345678
    assert player3['discgolfmetrix_id'] == 123456789012345678
    assert player4 is not None
    assert player4['pdga_number'] == 12345
    assert player4['name'] == "Ola Nordmann"
    assert player4['discord_id'] == 123456789012345678
    assert player4['discgolfmetrix_id'] == 123456789012345678

def test_clubplayerconfig_invalid_config():
    """Check if unknown configuration"""
    cfg = ClubPlayerConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(ClubPlayerConfig.__name__) is None
    assert cfg.get_player_by_pdga_number(12345) is None
    assert cfg.get_player_by_name("Player") is None
    assert cfg.get_player_by_discord_id(123456789012345678) is None
    assert cfg.get_player_by_discgolfmetrix_id(123456789012345678) is None

def test_clubplayerconfig_config_add_modify_remove_player(example_club_player_cfg):
    """Add, modify and remove a pdga number"""
    pdga_number = 87654
    name = "Player"
    discord_id = 123456789012345678
    discgolfmetrix_id = 12345

    assert example_club_player_cfg.get_player_by_pdga_number(pdga_number) is None
    assert example_club_player_cfg.remove_player(pdga_number) is False

    # Add
    written, modified = example_club_player_cfg.add_player(
        Player(pdga_number=pdga_number, name=name)
        )
    assert (written, modified) == (True, False)
    _player = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert _player is not None
    assert _player["pdga_number"] == pdga_number
    assert _player["name"] == name
    assert _player["discord_id"] is None
    assert _player["discgolfmetrix_id"] is None

    # Modify, add discord_id
    written, modified = example_club_player_cfg.add_player(
        Player(pdga_number=pdga_number, name="Modified Player", discord_id=discord_id)
        )
    assert (written, modified) == (True, True)
    _player = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert _player is not None
    assert _player["pdga_number"] == pdga_number
    assert _player["name"] == "Modified Player"
    assert _player["discord_id"] == discord_id
    assert _player["discgolfmetrix_id"] is None

    # Modify, add discord_id
    written, modified = example_club_player_cfg.add_player(
        Player(pdga_number=pdga_number, name="Modified Player", discord_id=discord_id, discgolfmetrix_id=discgolfmetrix_id)
        )
    assert (written, modified) == (True, True)
    _player = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert _player is not None
    assert _player["pdga_number"] == pdga_number
    assert _player["name"] == "Modified Player"
    assert _player["discord_id"] == discord_id
    assert _player["discgolfmetrix_id"] == discgolfmetrix_id

    # Remove (use alias to satisfy old name if needed)
    assert example_club_player_cfg.remove_player(pdga_number) is True
    assert example_club_player_cfg.get_player_by_pdga_number(pdga_number) is None


def test_clubplayerconfig_config_create_module(new_club_player_cfg):
    """Add a new module to a server"""
    assert new_club_player_cfg.module_exists() is False
    assert new_club_player_cfg.create_module() is True
    assert new_club_player_cfg.module_exists() is True

def test_clubplayerconfig_config_create(new_club_player_cfg):
    """Add a new server, add a player"""
    pdga_number_1 = 1
    pdga_number_2 = 2

    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_1) is None
    assert new_club_player_cfg.remove_player(pdga_number_1) is False

    # Add first player
    written, modified = new_club_player_cfg.add_player(
        Player(pdga_number=pdga_number_1, name="Ola Nordmann")
    )
    assert written, modified == (True, False)
    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_1) is not None

    # Modify first player
    written, modified = new_club_player_cfg.add_player(
        Player(pdga_number=pdga_number_1, name="Ola Nordmann")
    )
    assert written, modified == (True, True)

    # Add second player
    written, modified = new_club_player_cfg.add_player(
        Player(pdga_number=pdga_number_2, name="N/A")
    )
    assert written, modified  == (True, False)

    # Verify both
    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_1) is not None
    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_2) is not None
    # Remove both
    assert new_club_player_cfg.remove_player(pdga_number_1) is True
    assert new_club_player_cfg.remove_player(pdga_number_2) is True
    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_1) is None
    assert new_club_player_cfg.get_player_by_pdga_number(pdga_number_2) is None

from pathlib import Path
from disc_score_bot.config.clubplayerconfig import ClubPlayerConfig, Player

def test_clubplayerconfig_valid_config(example_club_player_cfg):
    """Check and read a valid configuration"""
    assert example_club_player_cfg.module_exists() is True
    assert example_club_player_cfg.read(ClubPlayerConfig.__name__) is not None
    player1 = example_club_player_cfg.get_player("Ola Nordmann")
    player2 = example_club_player_cfg.get_player_by_pdga_number(12345)
    player3 = example_club_player_cfg.get_player_by_discord_id(123456789012345678)
    player4 = example_club_player_cfg.get_player_by_discgolfmetrix_code("metrix_code")
    assert player1 is not None
    assert player1.name == "Ola Nordmann"
    assert player1.pdga_number == 12345
    assert player1.discord_id == 123456789012345678
    assert player1.discgolfmetrix_code == "metrix_code"
    assert player1 == player2 == player3 == player4

def test_clubplayerconfig_invalid_config():
    """Check if unknown configuration"""
    cfg = ClubPlayerConfig("wrong_server")
    assert cfg.module_exists() is False
    assert cfg.read(ClubPlayerConfig.__name__) is None
    assert cfg.get_player("Player") is None
    assert cfg.get_player_by_pdga_number(12345) is None
    assert cfg.get_player_by_discord_id(123456789012345678) is None
    assert cfg.get_player_by_discgolfmetrix_code("metrix_code") is None

def test_clubplayerconfig_config_add_modify_remove_player(example_club_player_cfg):
    """Add, modify and remove a pdga number"""
    pdga_number = 87654
    name = "Player"
    discord_id = 123456789012345678
    discgolfmetrix_code = "12345"

    assert example_club_player_cfg.get_player_by_pdga_number(pdga_number) is None
    assert example_club_player_cfg.remove_player(name) is False

    # Add
    written, modified = example_club_player_cfg.add_player(
        Player(name=name, pdga_number=pdga_number)
        )
    assert (written, modified) == (True, False)
    p = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert p is not None
    assert p.name == name
    assert p.pdga_number == pdga_number
    assert p.discord_id is None
    assert p.discgolfmetrix_code is None

    # Modify, add discord_id
    written, modified = example_club_player_cfg.add_player(
        Player(name=name, pdga_number=pdga_number, discord_id=discord_id)
        )
    assert (written, modified) == (True, True)
    p = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert p is not None
    assert p.name == name
    assert p.pdga_number == pdga_number
    assert p.discord_id == discord_id
    assert p.discgolfmetrix_code is None

    # Modify, add discord_id
    written, modified = example_club_player_cfg.add_player(
        Player(name=name, pdga_number=pdga_number, discord_id=discord_id, discgolfmetrix_code=discgolfmetrix_code)
        )
    assert (written, modified) == (True, True)
    p = example_club_player_cfg.get_player_by_pdga_number(pdga_number)
    assert p is not None
    assert p.pdga_number == pdga_number
    assert p.name == name
    assert p.discord_id == discord_id
    assert p.discgolfmetrix_code == discgolfmetrix_code

    # Remove (use alias to satisfy old name if needed)
    assert example_club_player_cfg.remove_player(name) is True
    assert example_club_player_cfg.get_player_by_pdga_number(pdga_number) is None


def test_clubplayerconfig_config_create_module(new_club_player_cfg):
    """Add a new module to a server"""
    assert new_club_player_cfg.module_exists() is False
    assert new_club_player_cfg.create_module() is True
    assert new_club_player_cfg.module_exists() is True

def test_clubplayerconfig_config_create(new_club_player_cfg):
    """Add a new server, add a player"""
    pdga_number_1 = 1
    name_1 = "Ola Nordmann"
    pdga_number_2 = 2
    name_2 = "N/A"

    assert new_club_player_cfg.get_player(name_1) is None
    assert new_club_player_cfg.remove_player(name_1) is False

    # Add first player
    written, modified = new_club_player_cfg.add_player(
        Player(name="Ola Nordmann", pdga_number=pdga_number_1)
    )
    assert written, modified == (True, False)
    assert new_club_player_cfg.get_player(name_1) is not None

    # Modify first player
    written, modified = new_club_player_cfg.add_player(
        Player(name=name_1, pdga_number=pdga_number_1)
    )
    assert written, modified == (True, True)

    # Add second player
    written, modified = new_club_player_cfg.add_player(
        Player(pdga_number=pdga_number_2, name=name_2)
    )
    assert written, modified  == (True, False)

    # Verify both
    assert new_club_player_cfg.get_player(name_1) is not None
    assert new_club_player_cfg.get_player(name_2) is not None
    # Remove both
    assert new_club_player_cfg.remove_player(name_1) is True
    assert new_club_player_cfg.remove_player(name_2) is True
    assert new_club_player_cfg.get_player(name_1) is None
    assert new_club_player_cfg.get_player(name_2) is None

import json
import sys
from pathlib import Path
from context import score
from score.playeralias import PlayerAlias
from score.alias import Alias
sys.path.insert(0, str(Path().cwd()))

def test_alias_list():
    """Test alias list"""
    wrong_server_alias = Alias("wrong_server")
    assert wrong_server_alias.server == "wrong_server"
    assert wrong_server_alias.alias_list is None
    server_example_alias = Alias("server_example")
    assert server_example_alias.server == "server_example"
    assert server_example_alias.alias_list is not None

def test_alias_get_player_with_alias():
    """Test get_player_with_alias"""
    server_example_alias = Alias("server_example")
    assert server_example_alias.get_player_with_alias("uDisc name") is not None
    assert server_example_alias.get_player_with_alias("uDisc league or tournament name") is not None
    assert server_example_alias.get_player_with_alias("uDisc name 2") is not None
    assert server_example_alias.get_player_with_alias("alias1") is not None
    assert server_example_alias.get_player_with_alias("alias2") is not None
    assert server_example_alias.get_player_with_alias("etc") is not None
    assert server_example_alias.get_player_with_alias("alias3") is None

def test_alias_name_serialize_deserialize():
    """Test to create a Name, serialize it and deserialize"""
    player_name = PlayerAlias("uDisc name 2",["alias1", "alias2", "etc"])
    json_file = json.dumps(player_name.__dict__)
    assert json_file is not None
    json_object = json.loads(json_file)
    assert json_object is not None
    player_name_copy = PlayerAlias.from_json(json_object)
    assert player_name == player_name_copy

def test_alias_name_has_alias():
    """Test to create a Name, and check for alias"""
    player_name = PlayerAlias("uDisc name 2", ["alias1", "alias2", "etc"])
    assert player_name.has_alias("alias1") is True
    assert player_name.has_alias("alias2") is True
    assert player_name.has_alias("etc") is True

def test_alias_name_remove_alias():
    """Test to create a Name, and remove aliases"""
    player_name = PlayerAlias("uDisc name 2", ["alias1", "alias2", "etc"])
    player_name.remove_alias("alias1")
    assert player_name.has_alias("alias1") is False
    player_name.remove_alias("alias2")
    assert player_name.has_alias("alias2") is False
    player_name.remove_alias("etc")
    assert player_name.has_alias("etc") is False

def test_alias_name_eq():
    """Test if Name aliases are equal"""
    assert PlayerAlias("uDisc name 1", ["alias1"]) != PlayerAlias("uDisc name 2", ["alias2"])
    assert PlayerAlias("uDisc name 1") == PlayerAlias("", ["uDisc name 1"])
    assert PlayerAlias("uDisc name 1") != PlayerAlias("uDisc name 2")
    assert PlayerAlias("uDisc name 1") == PlayerAlias("uDisc name 2", ["uDisc name 1"])
    assert PlayerAlias("", ["uDisc name 2"]) == PlayerAlias("uDisc name 2")
    assert PlayerAlias("uDisc name 1 ") == PlayerAlias("", ["uDisc name 1"])

import json
import os
import sys
from context import score
from score.name import Name
from score.alias import Alias
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_alias_list():
    """Test alias list"""
    wrong_server_alias = score.Alias("wrong_server")
    assert wrong_server_alias.server == "wrong_server"
    assert len(wrong_server_alias.alias_list) == 0
    server_example_alias = score.Alias("server_example")
    assert server_example_alias.server == "server_example"
    assert len(server_example_alias.alias_list) != 0

def test_alias_get_player_with_alias():
    """Test get_player_with_alias"""
    server_example_alias = score.Alias("server_example")
    assert server_example_alias.get_player_with_alias("uDisc name") is not None
    assert server_example_alias.get_player_with_alias("uDisc league or tournament name") is not None
    assert server_example_alias.get_player_with_alias("uDisc name 2") is not None
    assert server_example_alias.get_player_with_alias("alias1") is not None
    assert server_example_alias.get_player_with_alias("alias2") is not None
    assert server_example_alias.get_player_with_alias("etc") is not None
    assert server_example_alias.get_player_with_alias("alias3") is None

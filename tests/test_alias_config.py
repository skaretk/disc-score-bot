import json
import os
import sys
from context import score
from score.name import Name
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_alias_config_exist():
    cfg = score.AliasConfig("server_example")
    assert cfg.path_exists() is True
    assert cfg.config_exists() is True

def test_alias_config_not_exist():
    cfg = score.AliasConfig("wrong_server")
    assert cfg.path_exists() is False
    assert cfg.config_exists() is False
#
def test_alias_config_read():
    cfg = score.AliasConfig("server_example")
    assert cfg.read() is not None

def test_alias_config_read_not_exist():
    cfg = score.AliasConfig("wrong_server")
    assert cfg.read() is None

def test_alias_config_get_user_alias():
    cfg = score.AliasConfig("server_example")
    assert cfg.get_user_alias("wrong uDisc name") is None
    udisc_name_json = cfg.get_user_alias("uDisc name")
    assert udisc_name_json is not None
    udisc_name = Name.from_json(udisc_name_json)
    assert udisc_name is not None
    assert udisc_name.has_alias("uDisc league or tournament name") is True
    assert udisc_name.has_alias("wrong") is False
    udisc_name_2_json = cfg.get_user_alias("uDisc name 2")
    assert udisc_name_2_json is not None
    udisc_name_2 = Name.from_json(udisc_name_2_json)
    assert udisc_name_2 is not None
    assert udisc_name_2.has_alias("alias1") is True
    assert udisc_name_2.has_alias("alias2") is True
    assert udisc_name_2.has_alias("etc") is True
    assert udisc_name_2.has_alias("alias3") is False

def test_alias_config_add_modify_remove_user():
    """Test to add, modify and remove player aliases"""
    cfg = score.AliasConfig("server_example")
    assert cfg.get_user_alias("test user") is None
    assert cfg.add_user_alias("test user", "test user alias") is True
    assert cfg.add_user_alias("test user", "test user alias 2") is True
    test_user_json = cfg.get_user_alias("test user")
    assert test_user_json is not None
    test_user = Name.from_json(test_user_json)
    assert test_user is not None
    assert test_user.has_alias("test user alias") is True
    assert test_user.has_alias("test user alias 2") is True
    assert test_user.has_alias("test user alias 3") is False
    assert cfg.remove_user("test user")
    assert cfg.get_user_alias("test user") is None

def test_alias_config_json_dump_player_name():
    """Test to add, modify and remove player aliases"""
    cfg = score.AliasConfig("server_example")
    file_json_object = cfg.read()
    assert file_json_object is not None
    player_name = Name("uDisc name 2",["alias1, alias2", "etc"])
    json_file = json.dumps(player_name.__dict__)
    assert json_file is not None
    json_object = json.loads(json_file)
    assert json_object is not None
    player_name_copy = Name.from_json(json_object)
    assert player_name == player_name_copy

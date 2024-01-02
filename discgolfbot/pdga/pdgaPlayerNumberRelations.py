import json
from .pdgaPlayer import PdgaPlayer
from pathlib import Path
class PdgaPlayerNumberRelations:
    def __init__(self, db_file):
        self.db_file = db_file
        self.pdga_players = {}
        self.player_objects = {}
        self.load_db()
    
    def add_relation(self, player_object, save=True):
        self.pdga_players[player_object.discord_id] = player_object.__dict__
        self.player_objects[player_object.discord_id] = player_object
        if save:
            self.save_relations()

    def load_db(self):
        if not self.__db_file_exists__():
            self.__init_db_file__()
        relations = self.__load_json__()
        if len(relations) >=1:
            # loop through they pdga_players.json keys(discord_id)
            for discord_id_key in relations: 
                # construct a player object per discord_id entry saved and add them to the relation manager
                player_object = PdgaPlayer(pdga_number=relations[discord_id_key]['pdga_number'], player_name=relations[discord_id_key]['player_name'], discord_id=relations[discord_id_key]['discord_id'])
                self.add_relation(player_object=player_object, save=False)
    
    def __db_file_exists__(self):
        if not isinstance(self.db_file, Path):
            self.db_file = Path(self.db_file)
        return self.db_file.exists()
    
    def __init_db_file__(self):
        self.save_relations()
        
    def __validate_json__(self):
        try:
            with open(self.db_file.as_posix(), "r") as rf:
                json.load(rf)
        except:
            return False
        return True
        
    def __load_json__(self):
        if self.__validate_json__():
            with open(self.db_file.as_posix(), "r") as readf:
                relations = json.load(readf)
                return relations
        else:
            if self.db_file.exists():
                jres = json.loads(self.db_file.read_text())
                if isinstance(jres, dict) and len(jres) ==0:
                    print(f"Database file is empty: '{ self.db_file.as_posix() }'")
                    return jres
    def save_relations(self):
        with open(self.db_file.as_posix(), "w") as writef:
            json.dump(obj=self.pdga_players,fp=writef, indent=6)
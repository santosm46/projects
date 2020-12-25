import json
from Thing import Thing
from common import DATA_PATH, NAMES_FILE, random_name
import random

class RandomName(Thing):

    names_list = None

    def __init__(self) -> None:
        super().__init__()

        try:
            with open(f"{DATA_PATH}{NAMES_FILE}", 'r+') as json_file:
                self.names_list = json.load(json_file)
        except:
            pass


    
    def gen_person_info(self):
        if(self.names_list is None):
            genre = random.choice(["male", "female"])
            name = random_name()
        else:
            obj = random.choice(self.names_list)
            name = obj["Name"]
            genre = obj["Genre"]
        
        return {
            "name": name,
            "genre": genre
        }

from utils.common import DEBUG_ENABLED, line, log_error
from game.Game import Game
from game.Category import Category
from utils.beauty_print import debug_error, print_debug

class DataStructure(Game):

    def __init__(self):
        super().__init__()
        # may be redundant because it's gonna be overwritten by setup()
        # but it prevents the need to run this when creating a new game
    
    def setup(self, data: dict):
        self.data = data
        self.check_new_categories(self.data)
    
    
    def check_new_categories(self, data):
        new = self.get("Category").get_categories_copy()
        for category, info in new.items():
            if category not in data:
                info["concrete_things"] = {}
                data[category] = info.copy()
    

    def new_data_structure(self):
        category : Category = self.get("Category")
        self.data = category.get_categories_copy()

        # add fields
        for k, v in self.data.items():
            # v["last_id"] = 0 # não sei se vou usar
            # every Class has it's own way to create it using new_concrete_thing()
            v["concrete_things"] = {}

    def get_data(self):
        return self.data
    
    def keep_concrete_thing(self, id: str, concrete_thing: dict, category: str):
        try:
            self.data[category]["concrete_things"][id] = concrete_thing
        except:
            log_error(f"self.data isn't instantiated or there isn't category {category}", __name__, line())

    def get_concrete_thing(self, id: str, category: str):
        try:
            # print_debug(f"id={id}, categ={category}",__name__,line())
            concrete_thing = self.data[category]["concrete_things"][id]
            return concrete_thing
        except:
            log_error(f"Error getting thing {id} of category {category}", __name__, line())
            return None


    def delete_concrete_thing(self, thing_ref: dict):
        try:
            category = thing_ref["category"]
            _id = thing_ref["id"]
            del self.data[category]["concrete_things"][_id]
        except:
            log_error(f"self.data isn't instantiated or there isn't thing {thing_ref}", __name__, line())


    



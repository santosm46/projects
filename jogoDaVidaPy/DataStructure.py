from os import error
from common import DEBUG_ENABLED
from Thing import Thing
from Category import Category
from beauty_print import debug_error, print_debug

class DataStructure(Thing):

    def __init__(self):
        super().__init__()
        # may be redundant because it's gonna be overwritten by setup()
        # but it prevents the need to run this when creating a new game
        # self.new_data_structure()
    
    def setup(self, data):
        self.data = data
    
    def new_data_structure(self):
        category : Category = self.factory.get_instance("Category")
        self.data = category.get_categories_copy()

        # add fields
        for k, v in self.data.items():
            # v["last_id"] = 0 # não sei se vou usar
            # every Class has it's own way to create it using new_concrete_thing()
            v["concrete_things"] = {}

    def get_data(self):
        try:
            return self.data
        except:
            self.new_data_structure()
            return self.data
    
    def keep_concrete_thing(self, id: str, concrete_thing: dict, category: str):
        try:
            self.data[category]["concrete_things"][id] = concrete_thing
        except:
            debug_error(f"self.data isn't instantiated or there isn't category {category}", fname=__name__, enabled=DEBUG_ENABLED)

    def get_concrete_thing(self, id: str, category: str):
        # return self.data[category]["concrete_things"][id]
        try:
            concrete_thing = self.data[category]["concrete_things"][id]
            # print_debug(f"peguei concrete_thing: {concrete_thing}. ({id},{category}) ", fname=__name__)
            return concrete_thing
        except:
            debug_error(f"Error getting thing {id} of category {category}", fname=__name__, enabled=DEBUG_ENABLED)
            return None


    



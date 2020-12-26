

from beauty_print import debug_error, print_debug


class Thing:
    def __init__(self):
        pass
        
    
    def get_category(self) -> str:
        return type(self).__name__
    
    def run_func(self, name: str, *args, **kwargs):
        do = f"{name}"
        # print_debug(f"finally running func() {name} of {self.get_category()}",__name__)
        if hasattr(self, do) and callable(getattr(self, do)):
            func = getattr(self, do)
            func(*args, **kwargs)
        else:
            debug_error(f"Erro! Função {name} não existe nessa classe {self.get_category()}",__name__)
    
    # every class will implement their own method new_concrete_thing()
    def new_concrete_thing(self):
        game_manager = self.factory.get_instance("GameManager")

        _id = game_manager.generate_id()
        return {
            "id": _id
        }

    
    # small package with basic information of a thing, to help find it in the data structure
    def reference(self, id: str, category: str = None):
        if category is None:
            category = self.get_category()
        return {
            "id": id,
            "category": category
        }
    
    def set_factory(self, factory):
        self.factory  = factory
        if(self.get_category() != "Event"):
            self.event = factory.get_instance("Event")

    def get_concrete_thing(self, id: str):
        data = self.factory.get_instance("DataStructure")
        concrete_thing = data.get_concrete_thing(id, self.get_category())
        return concrete_thing
    
    def get_dict_list(self):
        data = self.factory.get_instance("DataStructure")
        dict_list = data.data[self.get_category()]
        # print(dict_list)
        return dict_list
    
    
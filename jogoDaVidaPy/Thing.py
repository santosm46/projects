# from Instanciator import Instanciator
# from GameManager import GameManager

class Thing:
    def __init__(self):
        pass
    
    def get_category(self) -> str:
        return type(self).__name__
    
    def run_func(self, name: str, *args, **kwargs):
        do = f"{name}"
        if hasattr(self, do) and callable(getattr(self, do)):
            func = getattr(self, do)
            func(*args, **kwargs)
        else:
            print(f"Erro! Função {name} não existe nessa classe {self.__class__}")
    
    # every class will implement their own method new_concrete_thing()
    # def new_concrete_thing(self, id: str = None):
    #     factory : Instanciator = self.factory
    #     game_manager : GameManager = factory.get_instance("GameManager")

    #     if id is None:
    #         id = game_manager.generate_id()
    #     return {
    #         "id": id
    #     }
    
    # small package with basic information of a thing, to help find it in the data structure
    def reference(self, id: str, category: str = None):
        if category is None:
            category = self.get_category()
        return {
            "id": id,
            "category": category
        }
    
    def set_factory(self, factory):
        self.factory = factory

    def get_concrete_thing(self, id: str):
        data = self.factory.get_instance("DataStructure")
        concrete_thing = data.get_concrete_thing(id, self.get_category())
        return concrete_thing
    
    def get_dict_list(self):
        data = self.factory.get_instance("DataStructure")
        # print(data)
        return data.data[self.get_category()]
    
    
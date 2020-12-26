from common import DEBUG_ENABLED
from beauty_print import print_debug
from Thing import Thing
from GameManager import GameManager
from DataStructure import DataStructure

class Tester(Thing):
    

    def __init__(self):
        super().__init__()


    def setup(self, event, name):
        self.event = event
        self.name = name
    
    def new_concrete_thing(self, name):
        concrete_thing = super().new_concrete_thing()

        data : DataStructure = self.factory.get_instance("DataStructure")

        concrete_thing["name"] = name

        data.keep_concrete_thing(concrete_thing["id"], concrete_thing, self.get_category())

        return concrete_thing


    def gritar(self, interested, event_causer, additional=None):
        olhar = type(interested["id"])

        data : DataStructure = self.factory.get_instance("DataStructure")
        me = data.get_concrete_thing(interested["id"], interested["category"])
        other = data.get_concrete_thing(event_causer["id"], event_causer["category"])
        me_name = me["name"]
        other_name = other["name"]
        if additional is None:
            roubado = "alguém"
        else:
            roubado = additional
        print(f"{me_name}: Aaaaaaa chamem a polícia!!! O {other_name} roubou {roubado}!")
    
    def chorar(self, interested, event_causer, additional=None):
        me = self.get_concrete_thing(interested["id"])
        name = me["name"]
        print(f"{name}: 😭😭😭😭😭😭😭")
    

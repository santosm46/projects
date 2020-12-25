from common import DEBUG_ENABLED
from Thing import Thing
# from Instanciator import Instanciator
from beauty_print import debug_error, print_debug
from DataStructure import DataStructure

event_debug = {
    "player_was_robbed": {
        "Robber": {
            "5": ["func1", "func2"],
            "7": ["func1"],
            "13": ["func1", "func2", "func3"],
        }
    }
}


class Event(Thing):
    

    def __init__(self):
        super().__init__()
    
    # É preciso dar setup após pegar instância
    def setup(self):
        # get events pointer of concrete_things of Event
        pass
    
    def set_factory(self, factory):
        self.factory = factory
        data_structure : DataStructure = self.factory.get_instance("DataStructure")
        self.events = data_structure.get_data()[self.get_category()]["concrete_things"]

    # new_concrete_thing
    def subscribe(self, event_name: str, interested: dict, function_name: str):
        
        if(event_name not in self.events):
            self.events[event_name] = {}
        
        category = interested["category"]
        if(category not in self.events[event_name]):
            self.events[event_name][category] = {}
        
        id = interested["id"]
        if(id not in self.events[event_name][category]):
            self.events[event_name][category][id] = []
        
        self.events[event_name][category][id].append(function_name)


    def unsubscribe(self, event_name: str, interested: dict) -> bool:
        try:
            category = interested["category"]
            id = interested["id"]
            self.events[event_name][category][id].clear()
            return True
        except:
            return False


    def unsubscribe_func(self, event_name: str, interested: dict, function_name: str) -> bool:
        try:
            category = interested["category"]
            id = interested["id"]
            self.events[event_name][category][id].remove(function_name)
            return True
        except:
            return False
    

    def notify(self, event_name: str, event_causer: dict, additional = None):
        if(event_name not in self.events):
            debug_error(f"There aren't listeners for event {event_name}", fname=__name__, enabled=DEBUG_ENABLED)
            return False
        
        for category, interesteds in self.events[event_name].items():
            # print_debug(f"category {category}")
            self.notify_category(event_name, event_causer, category, additional)
        
        return True


    def notify_category(self, event_name: str, event_causer: dict, category: str, additional = None):
        try:
            interesteds = self.events[event_name][category]
            # print_debug(f"interesteds {interesteds}")
        except:
            debug_error(f"There ins't event {event_name} registered or no category {category} here to notify", fname=__name__, enabled=DEBUG_ENABLED)
            return False

        for _id, function_name_list in interesteds.items():
            self.run_function_list(event_causer, category, function_name_list, _id, additional)


    def run_function_list(self, event_causer: dict, category: str, function_list: list, _id: str, additional = None):
        func_debug = None
        for function_name in function_list:
            try:    
                func_debug = function_name
                category_inst : Thing = self.factory.get_instance(category)
                # print_debug(f"peguei category_inst -> {category_inst}", fname=__name__)
                if additional is None:
                    category_inst.run_func(function_name, category_inst.reference(_id), event_causer)
                else:
                    category_inst.run_func(function_name, category_inst.reference(_id), event_causer, additional)
            except:
                # fix descomentar
                # debug_error(f"There ins't a function {func_debug} of {category}", fname=__name__, enabled=DEBUG_ENABLED)
                pass
                # return False
    


            


"""


events = {
    "player_landed_on" :{
        "id":{"func": ".."}, 
        "id":func2
    },
}


"""



# salvar no arquivo
# events = {
#   "player_landed_on" :{"id":"func1", "id":"func2"},
# }

# ao carregar do arquivo, usar um parser "func1" -> func1

#   em player.py
# event.notify("player_landed_on", {"player":"..", "tile":".."})

#   quem escuta, se inscreve
# event.subscribe("player_landed_on", função_a_ser_rodada)

#   em event.py

  
from common import DEBUG_ENABLED
from Thing import Thing
# from Instanciator import Instanciator
from beauty_print import debug_error, print_debug, print_error, print_beauty_json
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

all_events = [
    "entity_moved_to_coord",
    "building_board_print",
]


class Event(Thing):

    # def has_event(self, event_name):
    #     return event_name in self.events
    
    # def has_category_on_event(self, category, event_name):
    #     return self.has_event(event_name) and category in self.events[event_name]

    # def has_id_on_category_of_event(self, _id, category, event_name):
    #     return (self.has_category_on_event(category, event_name)
    #         and _id in self.events[event_name][category]
    #     )
    
    # def has_function_for_event_of_entity(self, function, event_name, reference: dict[str, str]):
    #     category = reference["category"]
    #     _id = reference["id"]
    #     return (
    #         self.has_id_on_category_of_event(_id, category, event_name)
    #         and function in self.events[event_name][category][_id]
    #     )

    def __init__(self):
        super().__init__()
    
    # É preciso dar setup após carregar data structure na main
    def setup(self):
        self.update_events_data_ref()
        # get events pointer of concrete_things of Event
        
    def set_factory(self, factory):
        self.factory = factory
        self.update_events_data_ref()
        
    # update reference to data structure
    def update_events_data_ref(self):
        data_structure : DataStructure = self.factory.get_instance("DataStructure")
        self.events : dict = data_structure.data[self.get_category()]["concrete_things"]


    # subscribe a function of an entity for an event
    def subscribe(self, event_name: str, interested, function_name: str):
        # interested -> {"id":"n",  "category":"ClassName"}
        category = interested["category"]
        _id = interested["id"]
        try:
            if(function_name in self.events[event_name][category][_id]):
                # can subscribe the same function only once
                return
        except:
            pass
        
        if(event_name not in self.events):
            self.events[event_name] = {}
        
        if(category not in self.events[event_name]):
            self.events[event_name][category] = {}
        
        if(_id not in self.events[event_name][category]):
            self.events[event_name][category][_id] = []
        
        self.events[event_name][category][_id].append(function_name)

    # unsubscribe all functions of an entity for an event
    def unsubscribe(self, event_name: str, interested: dict) -> bool:
        try:
            category = interested["category"]
            _id = interested["id"]
            self.events[event_name][category][_id].clear()
            return True
        except:
            return False

    # unsubscribe a function of an entity for an event
    def unsubscribe_func(self, event_name: str, interested: dict, function_name: str) -> bool:
        try:
            category = interested["category"]
            _id = interested["id"]
            self.events[event_name][category][_id].remove(function_name)
            return True
        except:
            return False
    

    def notify(self, event_name: str, event_causer: dict = None, additional = None):
        if(event_name not in self.events):
            # debug_error(f"There aren't listeners for event {event_name}", fname=__name__, enabled=DEBUG_ENABLED)
            return False
        
        for category, interesteds in self.events[event_name].items():
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

  
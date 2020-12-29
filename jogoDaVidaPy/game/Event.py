from utils.common import DEBUG_ENABLED
from game.Game import Game
# from Instanciator import Instanciator
from utils.beauty_print import debug_error, print_debug, print_error, print_beauty_json
from game.DataStructure import DataStructure

event_debug = {
    "entity_was_robbed": {
        "Police": {
            "5": ["func1", "func2"],
            "7": ["func1"],
            "13": ["func1", "func2", "func3"],
        }
    }
}

all_events = [
    "entity_moved_to_coord",
    "building_board_print",
    "new_round",
    "entity_choosing_spot",
    "entity_interacting_with_building",
]

"""
Event will run the function for the subscribers passing these parameters
(interested, event_causer, additional=None)

interested  and event_causer are on the format {"id": str, "category":str}
param additional format depends on the interested to extract the correct params
according to the function

"""

class Event(Game):


    def __init__(self):
        super().__init__()
    
    # É preciso dar setup após carregar data structure na main
    def setup(self):
        self.update_events_data_ref()
        pass
        # get events pointer of concrete_things of Event
        
    def set_factory(self, factory):
        self.factory = factory
        # self.update_events_data_ref()
        
    # update reference to data structure
    def update_events_data_ref(self):
        data_structure : DataStructure = self.get("DataStructure")
        # print_beauty_json(data_structure.data)
        self.events : dict = data_structure.data[self.get_category()]["concrete_things"]

    # subscribe a function of an entity for an event
    def subscribe(self, event_name: str, interested, function_name: str):
        # interested -> {"id":"n",  "category":"ClassName"}
        category = interested["category"]
        _id = interested["id"]

        if(self.has_event_categ_id_func(event_name, category, _id, function_name)):
            # can subscribe the same function only once
            return
        
        self.events[event_name][category][_id].append(function_name)

    # unsubscribe all functions of an entity for an event
    def unsubscribe(self, event_name: str, interested: dict) -> bool:
        category = interested["category"]
        _id = interested["id"]

        if(self.has_event_categ_id()):
            self.events[event_name][category][_id].clear()
            return True
        else:
            return False

    # unsubscribe a function of an entity for an event
    def unsubscribe_func(self, event_name: str, interested: dict, function_name: str) -> bool:
        category = interested["category"]
        _id = interested["id"]
        if(self.has_event_categ_id_func(event_name, category, _id, function_name)):
            self.events[event_name][category][_id].remove(function_name)
            return True
        else:
            return False
    

    def notify(self, event_name: str, event_causer: dict = None, additional = None):
        if(not self.has_event(event_name)):
            return False
        for category, interesteds in self.events[event_name].items():
            self.notify_category(event_name, event_causer, category, additional)
        
        return True


    def notify_category(self, event_name: str, event_causer: dict, category: str, additional = None):
        if(category not in self.events[event_name]):
            debug_error(f"There ins't event {event_name} registered or no category {category} here to notify", fname=__name__, enabled=DEBUG_ENABLED)
            return False
            # print_debug(f"interesteds {interesteds}")
        interesteds = self.events[event_name][category]

        for _id, function_name_list in interesteds.items():
            self.run_function_list(event_causer, category, function_name_list, _id, additional)
        return True

    def run_function_list(self, event_causer: dict, category: str, function_list: list, _id: str, additional = None):
        for function_name in function_list:
            category_inst : Thing = self.get(category)
            if additional is None:
                category_inst.run_func(function_name, category_inst.reference(_id), event_causer)
            else:
                category_inst.run_func(function_name, category_inst.reference(_id), event_causer, additional)
    


            
    def has_event(self, event_name):
        if event_name in self.events:
            return True
        self.events[event_name] = {}
        return False
    
    def has_event_categ(self, event_name, category):
        if self.has_event(event_name) and category in self.events[event_name]:
            return True
        self.events[event_name][category] = {}
        return False
    
    def has_event_categ_id(self, event_name, category, _id):
        if ( self.has_event_categ(event_name, category) and _id in self.events[event_name][category]):
            return True
        self.events[event_name][category][_id] = []
        return False

    def has_event_categ_id_func(self, event_name, category, _id, func):
        return (
            self.has_event_categ_id(event_name, category, _id) and
            func in self.events[event_name][category][_id]
        )


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

  
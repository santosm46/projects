from Event import Event
from beauty_print import print_warning
from LivingBeing import LivingBeing
from RandomName import RandomName
from common import modes

class Person(LivingBeing):

    def __init__(self):
        super().__init__()
        self.MAX_HP = 10
        self.mode_func[modes.ON_BOARD] = self.move_on_board
        self.mode_func[modes.ON_BUILDING] = self.interact_with_building
    
    def new_concrete_thing(self):
        info_gen : RandomName = self.get("RandomName")
        info = info_gen.gen_person_info()

        concrete = super().new_concrete_thing()
        concrete["genre"] = info["genre"]
        concrete["name"] = info["name"]
        concrete["money"] = 200
        concrete["hp"] = self.MAX_HP
        concrete["max_hp"] = self.MAX_HP
        concrete["modes_info"] = {modes.ON_BOARD: None, modes.ON_BUILDING: {"building":None}}


        return concrete

        
    def on_school_move(self, params=None):
        person = self.get_concrete_thing(params["id"])
        # name = person["name"]
        # print_warning(f"Pessoa {name} está na escola")
        event : Event = self.get("Event")
        event.notify("interact_with_building", self.reference(params["id"]))
    
    def interact_with_building(self, reference=None):
        info = self.get_mode_info_of(reference, modes.ON_BUILDING)
        event : Event = self.get("Event")
        event.notify("entity_interacting_with_building", reference, info["building"])

    def move_on_board(self, reference=None):
        print_warning("Pessoa genéria movendo no tabueiro...")


    def gui_output(self, text, color=None,end='\n',pause=False):
        pass

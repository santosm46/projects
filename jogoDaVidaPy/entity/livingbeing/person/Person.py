from game.Event import Event
from utils.beauty_print import print_warning
from entity.livingbeing.LivingBeing import LivingBeing

class Person(LivingBeing):

    def __init__(self):
        super().__init__()
        self.MAX_HP = 10
        self.modes_func[self.mode_on_board] = self.move_on_board
        self.modes_func[self.mode_on_building] = self.interact_with_building

        self.attr_genre = "genre"
        self.attr_name = "name"
        self.attr_money = "money"

    

    def new_concrete_thing(self):
        person = super().new_concrete_thing()
        self.update_concrete(person)
        person[self.attr_hp] = self.MAX_HP
        person[self.attr_max_hp] = self.MAX_HP
        person[self.attr_mode_info] = {self.mode_on_board: None, self.mode_on_building: {"building":None}}
        return person


    def update_concrete(self, person: dict):
        super().update_concrete(person)

        info = self.get("RandomName").gen_person_info()
        
        self.add_attr_if_not_exists(person, self.attr_genre, info["genre"])
        self.add_attr_if_not_exists(person, self.attr_name, info["name"])
        self.add_attr_if_not_exists(person, self.attr_money, 200)
        self.add_attr_if_not_exists(person, self.attr_hp, self.MAX_HP)
        self.add_attr_if_not_exists(person, self.attr_max_hp, self.MAX_HP)
        self.add_attr_if_not_exists(person, self.attr_mode_info, {self.mode_on_board: None, self.mode_on_building: {"building":None}})


        
    def on_school_move(self, params=None):
        person = self.get_concrete_thing(params["id"])
        # name = person["name"]
        # print_warning(f"Pessoa {name} está na escola")
        event : Event = self.get("Event")
        event.notify("interact_with_building", self.reference(params["id"]))
    
    def interact_with_building(self, reference=None):
        info = self.get_mode_info_of(reference, self.mode_on_building)
        event : Event = self.get("Event")
        event.notify("entity_interacting_with_building", reference, info["building"])

    def move_on_board(self, reference=None):
        print_warning("Pessoa genéria movendo no tabueiro...")


    def gui_output(self, text, color=None,end='\n',pause=False):
        pass



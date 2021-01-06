from game.DataStructure import DataStructure
from game.Event import Event
from utils.beauty_print import bcolors, debug_error, get_number_list, input_question, print_debug, print_number_list
from entity.Entity import Entity
from utils.common import MOCK_ID, emotions, line, stats, valid_number
import random


class LivingBeing(Entity):

    def __init__(self):
        super().__init__()

        self.attr_hp = "hp"
        self.attr_max_hp = "max_hp"
        self.attr_qi = "qi"
        self.attr_emotion = "emotion"
        self.attr_inventory = "inventory"
        self.attr_energy = "energy"
        self.attr_max_energy = "max_energy"

        self.modes_func[self.mode_on_board] = self.move_on_board

        self.mode_wandering = "wandering"
        self.mode_sleeping = "sleeping"
        self.mode_attaking = "attaking"
        self.mode_on_building = "on_building"

        self.first_interaction = 'Interagir com'

    def on_new_round(self, target_ref, event_maker_ref, a=None):
        self.reduce_energy(target_ref)
        self.being_move(target_ref["id"])

    def being_move(self, being_id):
        # being = self.get_beings()[being_id]
        being = self.get_concrete_thing(being_id)
        
        # execute a function according to the mode of the being
        self.modes_func[being[self.attr_mode]](self.reference(being_id))

    def new_concrete_thing(self):
        being = super().new_concrete_thing()
        self.update_concrete(being)

        return being
    
    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        e : Event = self.get("Event")
        e.subscribe("new_round", reference, "on_new_round")
    

    def update_concrete(self, being: dict):
        super().update_concrete(being)
        
        self.add_attr_if_not_exists(being, self.attr_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_max_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_qi, stats.QI)
        self.add_attr_if_not_exists(being, self.attr_emotion, emotions.NEUTRAL)
        self.add_attr_if_not_exists(being, self.attr_inventory, {})
        self.add_attr_if_not_exists(being, self.attr_energy, 1000)
        self.add_attr_if_not_exists(being, self.attr_max_energy, 1000)

    def reduce_energy(self, being_ref, decrease=1):
        # print_debug(f"being_ref = {being_ref}", __name__)
        being = self.get_concrete_thing_by_ref(being_ref)
        if not being:
            return
        
        # fix descomenar
        being[self.attr_energy] -= decrease

        if(being[self.attr_energy] <= 0):
            being[self.attr_energy] = 0
            self.reduce_hp(being_ref, decrease)
    
    def reduce_hp(self, being_ref, hp):
        being = self.get_concrete_thing_by_ref(being_ref)
        being[self.attr_hp] -= hp

        if(being[self.attr_hp] <= 0):
            being[self.attr_hp] = 0
            self.kill_being(being_ref, "no hp")

    def kill_being(self, being_ref, cause=None):
        data : DataStructure = self.get("DataStructure")
        # put being on cemitery later instead of deleting it
        data.delete_concrete_thing(being_ref)

    def move_on_board(self, reference=None):
        being_id = reference["id"]
        # being = self.get_concrete_thing(being_id)

        self.roll_dice_to_move(being_id)
    

    def roll_dice_to_move(self, _id: str):
        result = self.roll_dice(_id)
        self.choose_spot_to_move(_id, result)
    
    def gui_output(self, text, color=None,end='\n',pause=False):
        pass

    def gui_input(self, _id=None, function=None, question_id=None, params=None):
        if function == "choose_spot_to_move":
            return random.choice(params["valid_spots"])

        return None

    """
    When choosing spot to move, the options are, to just go to a place
    or go to a place to interact with an entity.
    valid_spots = ['A1', 'B1', 'A2']

    # some of them might be at the same spot
    entities_to_interact = {
        {"id": ".", "category": "School"},  # the interaction is to enter
        {"id": "7", "category": "Citizen"},
        {"id": "5", "category": "PlayerIM"},
    }
    """
    def choose_spot_to_move(self, _id, range_):
        player = self.get_concrete_thing(_id)
        board : Board = self.get("Board")
        valid_spots = board.get_valid_spots_for_range(player["coord"], range_)

        entities_to_interact = []
        # [
        #   {"ref":... , "interaction": "entrar na", "name": "Escola"},
        #   {"ref":... , "interaction": "entrar no", "name": "Mercado"},
        # ]

        if(len(valid_spots) == 0):
            self.gui_output("Não há lugares para ir")
            return
        params = {"valid_spots": valid_spots, "range":range_, "entities_to_interact": entities_to_interact}
        event : Event = self.get("Event")
        event.notify("entity_choosing_spot", self.reference(player["id"]), params)
        spot = None
        self.get("GameManager").print_game()
        self.gui_output(f"Resultado do dado: {range_}",color=bcolors.OKGREEN)
        self.gui_output("\nPara interagir: ",color=bcolors.HEADER)
        # parse entities ref to it's names, spots and interaction name
        interactions = []
        for entity_info in entities_to_interact:
            interactions.append(entity_info["interaction"])
        self.gui_output(get_number_list(interactions, title="", layed=True))
        self.gui_output(f"Casas: {bcolors.OKCYAN}" + ", ".join(valid_spots) + f"{bcolors.ENDC}")

        entity_ref = None
        while True:
            # question 1
            self.gui_output("\n\nDigite a casa ou n° da interação: ", bcolors.HEADER)
            option = self.gui_input(_id, "choose_spot_to_move",1, params).upper()
            if option in valid_spots:
                spot = option
                break
            if(valid_number(option, 1, len(entities_to_interact))):
                # if a number of the list of entities is chosen, take the reference to it 
                # then it's spot
                entity_ref = entities_to_interact[int(option)-1]["ref"]
                # entity_concr = self.get_concrete_thing_by_ref(entity_ref)
                break
        # if spot in buildings_list:
        #     place = buildings_list[spot]
        name = player["name"]
        if entity_ref is None:
            self.gui_output(f"Movendo {name} para {spot}... ")
            board.move_entity_to(reference=self.reference(player["id"]), alphanum=spot)
        else:
            self.gui_output(f"Movendo {name} para interagir com {entity_ref}... ")
            self.move_to_and_interact_with(self.reference(_id), entity_ref)
    


    def move_to_and_interact_with(self, me_ref, other_ref):
        e : Event = self.get("Event")
        board : Board = self.get("Board")
        other = self.get_concrete_thing_by_ref(other_ref)
        board.move_entity_to(reference=self.reference(me_ref["id"]), coord=other["coord"])
        e.notify("entity_interacting_with_entity", me_ref, other_ref)


        """
        the keys of an inventory is the class that will handle the
        information of the associated dict
        "inventory" -> {
            "Food": {
                "Apple": 3,
                "Banana": 3,
            }
            "Firearm": {
                "Pistol": 7,
                "MachineGun": 10
            },

            "School": {
                "Diploms": {
                    "elementary_school": school_id
                    "middle_school": school_id
                    "high_school": school_id
                }
            },

            "College": {
                "Diploms": {
                    "medicine": {
                        "first_year": college_id,
                        "second_year": college_id,
                    },
                }
            }

        }
        """


    



from game.DataStructure import DataStructure
from game.Event import Event
from utils.beauty_print import debug_error, print_debug
from entity.Entity import Entity
from utils.common import MOCK_ID, emotions, stats

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

        self.mode_wandering = "wandering"
        self.mode_sleeping = "sleeping"
        self.mode_attaking = "attaking"
        self.mode_on_building = "on_building"

    def new_concrete_thing(self):
        being = super().new_concrete_thing()
        self.update_concrete(being)

        return being
    
    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        e : Event = self.get("Event")
        e.subscribe("new_round", reference, "reduce_energy")

    def update_concrete(self, being: dict):
        super().update_concrete(being)
        
        self.add_attr_if_not_exists(being, self.attr_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_max_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_qi, stats.QI)
        self.add_attr_if_not_exists(being, self.attr_emotion, emotions.NEUTRAL)
        self.add_attr_if_not_exists(being, self.attr_inventory, {})
        self.add_attr_if_not_exists(being, self.attr_energy, 1000)
        self.add_attr_if_not_exists(being, self.attr_max_energy, 1000)

    def reduce_energy(self, being_ref, b=None, decrease=1):
        # print_debug(f"being_ref = {being_ref}", __name__)
        being = self.get_concrete_thing_by_ref(being_ref)
        if not being:
            return
        # fix descomenar
        # being[self.attr_energy] -= decrease

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


        """
        the keys of an inventory is the class that will handle the
        information of the associated dict
        "inventory" -> {
            "Food": {
                "Apple": 3
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


    



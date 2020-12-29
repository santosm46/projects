from beauty_print import debug_error
from Entity import Entity
from common import emotions, stats

class LivingBeing(Entity):

    def __init__(self):
        super().__init__()

        self.attr_hp = "hp"
        self.attr_max_hp = "max_hp"
        self.attr_qi = "qi"
        self.attr_emotion = "emotion"
        self.attr_inventory = "inventory"

        self.mode_wandering = "wandering"
        self.mode_sleeping = "sleeping"
        self.mode_attaking = "attaking"
        self.mode_on_building = "on_building"

    def new_concrete_thing(self):
        being = super().new_concrete_thing()
        self.update_concrete(being)

        return being


    def update_concrete(self, being: dict):
        super().update_concrete(being)
        
        self.add_attr_if_not_exists(being, self.attr_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_max_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_qi, stats.QI)
        self.add_attr_if_not_exists(being, self.attr_emotion, emotions.NEUTRAL)
        self.add_attr_if_not_exists(being, self.attr_inventory, {})


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
            "Education": {
                "Diploms": {
                    "School": {}
                }
                "School": {
                    "Diploms": {
                        "elementary_school": school_id
                        "middle_school": school_id
                        "high_school": school_id
                    }
                },
                "College": {
                    "Diploms": {
                        "medicine": college_id
                    }
                }
            }
        }
        """


    



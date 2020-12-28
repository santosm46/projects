from beauty_print import debug_error
from Entity import Entity
from common import emotions, stats, modes

class LivingBeing(Entity):

    def __init__(self):
        super().__init__()
        self.mode_func = {}


    def new_concrete_thing(self):
        concrete = super().new_concrete_thing()

        concrete["hp"] = stats.MAX_HP
        concrete["max_hp"] = stats.MAX_HP
        concrete["qi"] = stats.QI
        concrete["emotion"] = emotions.NEUTRAL
        concrete["mode"] = modes.ON_BOARD
        concrete["modes_info"] = {}

        concrete["inventory"] = {}
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


        return concrete
    
    def change_mode(self, _id, new_mode, mode_info=None):
        being = self.get_concrete_thing(_id)
        being["mode"] = new_mode
        if not mode_info:
            being["modes_info"][new_mode] = mode_info


    def get_mode_info_of(self, reference, mode):
        being = self.get_concrete_thing_by_ref(reference)
        try:
            return being["modes_info"][mode]
        except:
            debug_error(f"Can't get mode {mode} of {self.get_category()}",__name__)
            return None




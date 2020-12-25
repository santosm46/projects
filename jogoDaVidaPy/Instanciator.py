from beauty_print import print_debug

from Thing import Thing

from GameManager import GameManager
from Player import Player
from Event import Event
from Tester import Tester
from Category import Category
from SaveManager import SaveManager
from DataStructure import DataStructure
from PlayerIM import PlayerIM
from PlayerOOM import PlayerOOM

class Instanciator(Thing):

    classes = {
        "GameManager": GameManager,
        "Player": Player,
        "Event": Event,
        "Tester": Tester,
        "Category": Category,
        "SaveManager": SaveManager,
        "DataStructure": DataStructure,
        "PlayerIM": PlayerIM,
        "PlayerOOM": PlayerOOM,
    }

    instances = {}

    def __init__(self):
        super().__init__()

    def get_instance(self, class_name):
        # print_debug(f"Going to get instance of {class_name}", fname=__name__)

        # If not instantiated, create a instance
        if(class_name not in self.instances):
            self.instances[class_name] = self.classes[class_name]()
            self.instances[class_name].set_factory(self)
            # print_debug(f"Creating new instance of {class_name}", fname=__name__)

        # print_debug(f"returning instance {self.instances[class_name]} of {class_name}", fname=__name__)
        
        return self.instances[class_name]

# For debug

# b: GameManager = a.get_instance('GameManager')
# c: GameManager = a.get_instance('GameManager')

# b.setup2("Arroz")
# # c.setup2("Batata")

# print(b.teste)
# b.teste = "Batata"
# print(c.teste)

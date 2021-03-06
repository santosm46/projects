from entity.livingbeing.person.npc.Citizen import Citizen
from entity.livingbeing.person.npc.criminal.Killer import Killer
from entity.object.building.Jail import Jail
from entity.object.weapon.Weapon import *
from entity.object.building.commerce.GunShop import GunShop
from entity.object.building.Cemetery import Cemetery
from entity.livingbeing.person.npc.criminal.Robber import Robber
from entity.object.building.commerce.SuperMarket import SuperMarket
from entity.object.Food import Food
from utils.beauty_print import print_debug

# from Thing import Thing

from game.GameManager import GameManager
from game.SaveManager import SaveManager
from game.Event import Event
from game.Category import Category
from game.DataStructure import DataStructure
from game.dicerandom.DiceRandom import DiceRandom
from game.dicerandom.DiceRollOrRandom import DiceRollOrRandom
from game.RandomName import RandomName
from game.Board import Board
from game.Logger import Logger

from entity.livingbeing.person.player.PlayerIM import PlayerIM
from entity.livingbeing.person.player.PlayerOOM import PlayerOOM
from entity.livingbeing.person.player.Player import Player

from entity.object.building.education.School import School
from entity.object.building.education.College import Medicine
from entity.object.building.education.College import Pedagogy
from entity.object.building.education.College import LawCourse
from entity.object.building.education.College import Engineer
from entity.object.building.commerce.Bank import Bank
from entity.object.building.commerce.Bank import MoneyBag

class Instanciator:

    classes = {
        "GameManager": GameManager,
        "Player": Player,
        "Event": Event,
        "Category": Category,
        "SaveManager": SaveManager,
        "DataStructure": DataStructure,
        "PlayerIM": PlayerIM,
        "PlayerOOM": PlayerOOM,
        "Board": Board,
        "RandomName": RandomName,
        "DiceRandom": DiceRandom,
        "DiceRollOrRandom": DiceRollOrRandom,
        "School": School,
        "Bank": Bank,
        "Logger": Logger,
        "Medicine": Medicine,
        "Pedagogy": Pedagogy,
        "LawCourse": LawCourse,
        "Engineer": Engineer,
        "MoneyBag": MoneyBag,
        "Food": Food,
        "SuperMarket": SuperMarket,
        "Robber": Robber,
        "Cemetery": Cemetery,
        "GunShop": GunShop,
        "Weapon": Weapon,
        "Knife":Knife,
        "Pistol":Pistol,
        "MachineGun":MachineGun,
        "Shotgun":Shotgun,
        "Jail": Jail,
        "Killer": Killer,
        "Citizen": Citizen,
    }


    instances = {}

    def __init__(self):
        super().__init__()

    def get_instance(self, class_name):
        # print_debug(f"Going to get instance of {class_name}", fname=__name__)

        # If not instantiated, create a instance
        if(class_name not in self.instances):
            self.instances[class_name] = self.classes[class_name]() # instanciating class
            self.instances[class_name].set_factory(self)
            # print_debug(f"Creating new instance of {class_name}", fname=__name__)

        # print_debug(f"returning instance {self.instances[class_name]} of {class_name}", fname=__name__)
        
        return self.instances[class_name]
    
    def gi(self, class_name):
        return self.get_instance(class_name)

    def get(self, class_name):
        return self.get_instance(class_name)

# For debug

# b: GameManager = a.get_instance('GameManager')
# c: GameManager = a.get_instance('GameManager')

# b.setup2("Arroz")
# # c.setup2("Batata")

# print(b.teste)
# b.teste = "Batata"
# print(c.teste)

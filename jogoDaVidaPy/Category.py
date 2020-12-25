from beauty_print import *
from Thing import Thing

tree = {
    "DataStructure": {
        "Entity": {
            "Person": {
                "Player": {},
                "Npc": {
                    "Citizen": {
                        "Medic": {},
                    },
                    "Homeless": {},
                    "Criminal": {
                        "Dealer": {},
                        "Robber": {},
                    }
                }
            },
            "Object": {
                "Food":{
                    "Steak": {},
                    "Cookie": {},
                    "Cake": {},
                },
                "Weapon": {
                    "Firearm": {
                        "Sniper": {},
                        "Shotgun": {},
                        "Pistol": {},
                        "Machine_gun": {},
                    },
                    "White_gun": {
                        "Sword": {},
                        "Knife": {},
                    },
                },
            },
            "Animal":{},
        },
        "Building":{
            "Health": {
                "Hospital": {},
            },
            "Education": {
                "School": {},
                "College": {},
            },
            "Commerce": {
                "DrugStore": {},
                "Market": {},
            }
        },
        "Tester": {}
    },
    "Game": {
        "GameManager": {},
        "Event": {},
        "Category": {},
        "SaveManager": {},
    },
    "Instanciator": {},
}

class Category(Thing):


    def __init__(self) -> None:
        super().__init__()
        self.root = self.create_new_list()
    
    # não sei se vou usar setup() em Category
    # setar Dicionário para ver as categorias
    def setup(self, category_list):
        self.root = category_list
    
    def get_categories(self):
        return self.root
    def get_categories_copy(self):
        return self.root.copy()
    def get_keys(self):
        return self.root.keys()
    def get_list(self):
        return list(self.get_keys())

    # private
    def create_new_list(self) -> dict:
        lista = {}
        self.add_nodes(tree, lista)
        return lista
    
    # private
    def add_nodes(self, node, lista, super_category=None, tree_level=0):
        if node == {}:
            return
        for key, value in node.items():
            lista[key] = {
                "super_category": super_category,
                "sub_categories": list(value.keys()),
                "tree_level": tree_level, # for visualitation porposes
            }
            self.add_nodes(node[key], lista, key, tree_level+1)
    
    def category_exists(self, category) -> bool:
        if category not in self.get_categories():
            print_error(f"Category '{category}' doesn't exist")
            # input("")
            return False
        return True

    ## Nodes
    def node_category(self, node):
        return node["category"]
    def node_super_category(self, node):
        return node["super_category"]
    def node_sub_categories(self, node):
        return node["sub_categories"]
    
    ## Nome da Category
    def get_super_category(self, category) -> str:
        self.category_exists(category)
        try:
            return self.root[category]["super_category"]
        except:
            return None
    
    def get_sub_categories(self, category) -> list:
        self.category_exists(category)
        try:
            return self.root[category]["sub_categories"]
        except:
            return None   
    
    def inside_of_category(self, category, super_category) -> bool:
        if(not self.category_exists(category)):
            return False
        if(not self.category_exists(super_category)):
            return False
        try:
            while True:
                parent = self.get_super_category(category)
                if(parent == None):
                    return False
                if(parent == super_category):
                    return True
                category = parent
        except:
            return False  
    
    def is_category_or_inside(self, category, super_category) -> bool:
        if(category == super_category):
            return True
        return self.inside_of_category(category, super_category)


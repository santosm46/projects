

from utils.common import MOCK_ID, line, log_error
from utils.beauty_print import debug_error, print_debug


class Thing:
    def __init__(self):
        self.id_attr = 'id'
        self.attr_id = 'id'


    all_images = {
        
        "Teacher": '👩‍🏫',
        "Animal": {
            "Dog": '🐶',
            "Cat": '🐱',
            "Cow": '🐮',
            "Pig": '🐷',
            "Chicken": '🐔',
            "Jaguar":'🐆',
            "Mosquito": '🦟',
        },
        "Tree": {
            "GrownTree": '🌳',
            "SmallTree": '🌱',
        },
        "Car": {
            "White": '🚗',
            "Yellow": '🚕',
            "Blue": '🚙'
        },
        # "Money": '💵💴💶💷'
    }
        
    
    def get_category(self) -> str:
        return type(self).__name__
    
    def run_func(self, name: str, *args, **kwargs):
        do = f"{name}"
        # print_debug(f"finally running func() {name} of {self.get_category()}",__name__)
        if hasattr(self, do) and callable(getattr(self, do)):
            func = getattr(self, do)
            func(*args, **kwargs)
        else:
            debug_error(f"Erro! Função {name} não existe nessa classe {self.get_category()}",__name__)
    
    # every class will implement their own method new_concrete_thing()
    def new_concrete_thing(self):
        game_manager = self.get("GameManager")

        _id = game_manager.generate_id()
        return {
            "id": _id
        }

    
    # small package with basic information of a thing, to help find it in the data structure
    def reference(self, id: str, category: str = None):
        if category is None:
            category = self.get_category()
        return {
            "id": id,
            "category": category
        }
    
    def set_factory(self, factory):
        self.factory  = factory
        self.fac  = factory
        
    
    # Get instance of a class
    def get(self, class_name):
        return self.factory.get_instance(class_name)

    def get_concrete_thing(self, id: str, category=None):
        if category is None:
            category = self.get_category()
        data = self.get("DataStructure")
        concrete_thing = data.get_concrete_thing(id, category)
        return concrete_thing
    
    def get_dict_list(self):
        data = self.get("DataStructure")
        dict_list = data.data[self.get_category()]
        # print(dict_list)
        return dict_list["concrete_things"]
    
    def get_concrete_thing_by_ref(self, reference: dict):
        data = self.get("DataStructure")
        r = data.get_concrete_thing(reference["id"], reference["category"])
        return r

    # will be overwritten
    def get_image(self, _id=None):
        try:
            return self.all_images[self.get_category()]
        except:
            return 'i'


    def add_attr_if_not_exists(self, concrete, attr, default):
        if(attr not in concrete):
            concrete[attr] = default


    # to be overwritten
    def update_subscriber(self, reference: dict):
        pass
    
    def update_subscribers(self):
        event = self.get("Event")
        # for this event, it doesn't need a reference to an entity, because the function
        # takes all the entities of the class
        event.subscribe("building_board_print", self.reference(MOCK_ID), "on_building_board_print")
        for _id in self.get_dict_list().keys():
            try:
                self.update_subscriber(self.reference(_id))
            except:
                log_error(f"Couldn't update subscriber {_id} of category {self.get_category()}",__name__,line())
        
    def update_concrete(self, concrete: dict):
        pass

    def update_concretes(self):
        for _id in self.get_dict_list().keys():
            self.update_concrete(self.reference(_id))


    def on_building_board_print(self, interested=None, event_causer=None, additional=None):
        # pegar dict de concrete_things da classe
        entities : dict = self.get_dict_list() 

        category = self.get_category()
        if(category not in additional):
            additional[category] = []
        
        # print_debug(f"chegou na escola -> {entity}",__name__)

        for entity_id, entity in entities.items():
            additional[category].append({
                "image": self.get_image(entity_id),
                "coord": entity["coord"]
            })




from game.Logger import Logger
from game.Event import Event
from utils.beauty_print import bcolors, debug_error, input_question, print_debug, print_number_list
from entity.object.Object import Object
from utils.common import GOVERNMENT, line, log_error
from game.Board import Board
import random

class Building(Object):

    def __init__(self) -> None:
        super().__init__()
        self.attr_money = 'money'
        self.attr_name = 'name'

        self.first_interaction = 'Entrar em'

        self.interactions['put_person_on_building'] = 'Entrar aqui'

        # overwrite these
        self.wage_start = -2
        self.wage_multipl = 50
        self.work_nick = 'Trabalhador aqui'
    
    images = {
        "Medicine": '💉',
        "Pedagogy": '📚',
        # "LawCourse": '⚖ ',
        # "LawCourse": ' 🖋️',
        "LawCourse": '🔏',
        "Engineer": '🔩',
        "School": '🏫',
        "House": ['🏠', '🏡'],
        "Hospital": '🏥',
        "Church": '⛪',
        "Bank": '🏦',
        "TownHall": '🏛️',
        "GasStation": '⛽',
        "Castle": '🏰',
        "Jail": '🏰',
        "SuperMarket": '🛒',
        "Casino": '🎰',
        "GunShop": '🔫',
        "Cemetery": f'⚰️{bcolors.FAIL}✝{bcolors.ENDC}'
    }

    # def custom_requirement_to_interact(self, building_data, person_ref, additional):
    #     return self.is_person(person_ref["category"])

    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        event : Event = self.get("Event")
        # event.subscribe("entity_interacting_with_entity", reference, "put_person_on_building")
        
        # event.subscribe("entity_interacting_with_building", reference, "on_building_interact")

    def on_building_interact(self, building_ref, person_ref, additional=None):
        log_error(f"This funcion [on_building_interact] needs to be overwritten for {building_ref}",__name__,line())
        self.remove_from_building(building_ref, person_ref)

    def on_person_working(self, building_ref, person_ref):
        log_error(f"on_person_working() needs to be overwritten for {building_ref}",__name__,line())
        self.remove_from_building(building_ref, person_ref)

    # def entity_interaction(self, me_ref, other_ref, additional):
    #     input(f"Botei a pessoa na {me_ref}.   ({__name__}:{line()})")
    #     self.put_person_on_building(me_ref, other_ref, additional)
    

    def get_image(self, _id=None):
        categ = self.get_category()
        image = self.images[categ]
        if(type(image) == list):
            return random.choice(image)
        return image

    def new_concrete_thing(self):
        building = super().new_concrete_thing()

        self.update_concrete(building)
        building[self.attr_owner] = GOVERNMENT

        return building
    
    # interface
    def can_work_here(self, person_ref):
        return False
    
    def get_interactions_for(self, entity_ref):
        interacts = super().get_interactions_for(entity_ref)
        if self.can_work_here(entity_ref):
            interacts['put_person_to_work'] = 'Trabalhar aqui'
        return interacts
        # return super().get_interactions_for(entity_ref)
    
    def put_person_to_work(self, person_ref, building_ref):
        # from entity.livingbeing.person.Person import Person

        person_class : Person = self.get(person_ref['category'])
        mode_name = person_class.mode_working_on_building
        self.put_person_on_building(person_ref, building_ref, mode_name=mode_name)
    
    def update_concrete(self, building: dict):
        super().update_concrete(building)

        board : Board = self.get("Board")
        
        self.add_attr_if_not_exists(building, self.attr_coord, board.alphanum_to_coord("A1"))
        self.add_attr_if_not_exists(building, self.attr_price, 125000000)
        self.add_attr_if_not_exists(building, self.attr_money, 0)
        self.add_attr_if_not_exists(building, self.attr_name  ,"Nome da construção")

    def remove_from_building(self, building_ref, person_ref):
        try:
            building = self.get_concrete_thing_by_ref(building_ref)
            person_class = self.get(person_ref["category"])
            person_class.change_mode(person_ref["id"], person_class.mode_on_board)
            board : Board = self.get("Board")
            close_free_spot = board.closer_free_spot_to(building[self.attr_coord])
            board.move_entity_to(person_class.reference(person_ref["id"]), alphanum=close_free_spot)
        except:
            log_error(f"Error trying to take person {person_ref} out of building {building_ref}",__name__,line())

    def is_person(self, person_categ):
        categ_mg = self.get("Category")
        return categ_mg.is_category_or_inside(person_categ, "Person")


    def put_person_on_building(self, person_ref, building_ref, additional=None, mode_name=None):
        # print_debug(f"tentando colocar {person_ref} em b {building_ref}",__name__,line())
        person_categ = person_ref["category"]
        if(not self.is_person(person_categ)):
            # print_debug(f"não é pessoa {person_ref}, mas esse é -> {building_ref}",__name__,line())
            # only people can enter building
            return False
        person_class = self.get(person_categ)
        if mode_name is None:
            mode_name = person_class.mode_on_building

        building_id = building_ref["id"]
        building = self.get_concrete_thing(building_id)
        person = person_class.get_concrete_thing(person_ref["id"])
        # can only put person if stepping at building
        # if(person["coord"] != building["coord"]):
        #     return False
        # print_debug("está na mesma coordenada",__name__,line())
        
        # print_debug("tentando colocar pessoa na escola 3")
        mode_info = person_class.get_mode_info_of(person_ref,mode_name)
        # print_debug(f"peguei mode info {mode_info} de {mode_name}",__name__,line())
        
        # print_beauty_json(mode_info)
        mode_info["building"] = self.reference(building_id)

        person_class.change_mode(person["id"], mode_name, self.reference(building_id))
        # print_debug("coloquei pessoa em building",__name__,line())

        return True
    

    def on_person_working(self, building_ref, person_ref):
        # return super().on_person_working(building_ref, person_ref)
        person_class : Person = self.get(person_ref['category'])

        school = self.get_concrete_thing_by_ref(building_ref)
        person = self.get_concrete_thing_by_ref(person_ref)
        name = school["name"]
        pname = person["name"]

        person_class.gui_output(f"\nVocê é {self.work_nick}. escolha uma opção")
        options = ["trabalhar", "trabalhar e sair", "sair"]
        print_number_list(options)
        # fix colocar gui_input
        option = input_question("Opção: ")
        if(str(option) == "3"):
            self.remove_from_building(building_ref, person_ref)
            return

        person_class.gui_output("Role o dado e veja quanto ganhará")
        dice_num = person_class.roll_dice(person_ref['id'])
        earned_money = self.wage_multipl * (dice_num - self.wage_start)
        log : Logger = self.get("Logger")

        # from entity.object.building.commerce.Bank import Bank

        bank : Bank = self.get("Bank")

        dice_inf = f"(Dado: {dice_num})"

        if(earned_money < 0):
            bank.decrease_person_money(person_ref, earned_money)
            log.add(f"{name} atrasou o salário do/a {pname} e teve que arcar com as despesas, gastou {earned_money} {dice_inf}", color=bcolors.FAIL)
        elif(earned_money == 0):
            log.add(f"{name} atrasou o salário do/a {pname}, ganhou nada {dice_inf}", color=bcolors.FAIL)
        else:
            if(not bank.transfer_money_from_to(building_ref, person_ref, earned_money)):
                log.add(f"{name} está sem verbas. {pname} ganhou nada {dice_inf}", color=bcolors.FAIL)
                self.remove_from_building(building_ref, person_ref)
                return
            log.add(f"{name} pagou {earned_money} a/o {pname} {dice_inf}", color=bcolors.OKGREEN)

        if(str(option) == "2"):
            self.remove_from_building(building_ref, person_ref)

    


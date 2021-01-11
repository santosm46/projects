from entity.Entity import Entity
from game.DataStructure import DataStructure
from game.Event import Event
from utils.beauty_print import bcolors, debug_error, get_number_list, input_question, print_debug, print_error, print_number_list
from utils.common import MOCK_ID, emotions, line, log_error, penalty, scale, stats, valid_number
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
        self.attr_age = "age"
        self.attr_birth_year = "birth_year"

        self.modes_func[self.mode_on_board] = self.move_on_board

        self.mode_wandering = "wandering"
        self.mode_sleeping = "sleeping"
        self.mode_attaking = "attaking"
        self.mode_on_building = "on_building"

        self.first_interaction = f"{self.category_nick()}"

        self.interactions['be_attacked'] = "Atacar"

        self.death_causes = {
            'heart_attack': 'de ataque cardíaco',
            'starved': 'de fome',
            'killed': 'assassinado',
        }

        self.categ_color = bcolors.WARNING


    # for all entities
    def on_new_round(self, target_ref, event_maker_ref, a=None):
        # debug_error(f"{self.get_category()} chaves -> {self.get_dict_list().keys()}",__name__,line())
        beings = self.get_dict_list()
        keys_list = list(beings.keys())
        for key in keys_list:
            # advance age
            beings[key][self.attr_age] += 1

            ref = self.reference(key)
            if not self.reduce_energy(ref):
                # if being died when reduced energy, skip this iteraction
                continue
            if random.randrange(0,100) < self.risk_of_death(being_ref=ref):
                damage = random.randrange(6, 9)
                if not self.reduce_hp(ref, damage, {'type':'heart_attack', 'info':'de ataque cardíaco'}):
                    continue
                else:
                    name = beings[key]['name']
                    self.get("Logger").add(f"{name} sofreu um ataque cardícado perdendo {damage}💜", color=bcolors.WARNING)
            self.being_move(key)
            # debug_error(f"{self.get_category()} chaves -> {self.get_dict_list().keys()}",__name__,line())

    def being_move(self, being_id):
        # being = self.get_beings()[being_id]
        being = self.get_concrete_thing(being_id)
        # execute a function according to the mode of the being
        self.modes_func[being[self.attr_mode]](self.reference(being_id))

    def new_concrete_thing(self):
        being = super().new_concrete_thing()
        self.update_concrete(being)
        self.update_subscriber(self.reference(being["id"]))
        return being
    
    def update_subscribers(self):
        super().update_subscribers()
        e : Event = self.get("Event")
        e.subscribe("new_round", self.reference(MOCK_ID), "on_new_round")
    
    # def update_subscriber(self, reference: dict):
    #     super().update_subscriber(reference)
    
    def unsubscribe_entity(self, reference: dict):
        super().unsubscribe_entity(reference)
        e : Event = self.get("Event")
        # e.unsubscribe("new_round", reference)

    def update_concrete(self, being: dict):
        super().update_concrete(being)
        
        self.add_attr_if_not_exists(being, self.attr_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_max_hp, stats.MAX_HP)
        self.add_attr_if_not_exists(being, self.attr_qi, stats.QI)
        self.add_attr_if_not_exists(being, self.attr_emotion, emotions.NEUTRAL)
        self.add_attr_if_not_exists(being, self.attr_inventory, {})
        self.add_attr_if_not_exists(being, self.attr_energy, 1000)
        self.add_attr_if_not_exists(being, self.attr_max_energy, 1000)
        self.add_attr_if_not_exists(being, self.attr_age, random.randrange(16, 21))
        birth_year = self.get("GameManager").get_year() - being[self.attr_age]
        self.add_attr_if_not_exists(being, self.attr_birth_year, birth_year)

    def reduce_energy(self, being_ref, decrease=1):
        # print_debug(f"being_ref = {being_ref}", __name__)
        being = self.get_concrete_thing_by_ref(being_ref)
        if not being:
            return False
        
        # fix descomenar
        being[self.attr_energy] -= decrease

        if(being[self.attr_energy] <= 0):
            being[self.attr_energy] = 0
            return self.reduce_hp(being_ref, decrease, {'type':'starved', 'info':'de fome'})
        return True
    
    def reduce_hp(self, being_ref, hp, cause=None):
        being = self.get_concrete_thing_by_ref(being_ref)
        being[self.attr_hp] -= hp

        if(being[self.attr_hp] <= 0):
            being[self.attr_hp] = 0
            self.kill_being(being_ref, cause)
            return False
        if being[self.attr_hp] > 15:
            being[self.attr_hp] = 15
        return True



    def kill_being(self, being_ref, cause=None):
        log = self.get("Logger")
        if cause is None:
            cause = {'type':'unknown', 'info': ''}
        death_descrp = cause['info']
        bname = self.person_name(being_ref,last=bcolors.FAIL)
        log.add(f"[{self.category_nick()}] {bname} morreu {death_descrp}", color=bcolors.FAIL)
        being = self.get_concrete_thing_by_ref(being_ref)
        being["death_year"] = self.get("GameManager").get_year()
        being["death_cause"] = cause['info']
        being["death_type"] = cause['type']
        self.unsubscribe_entity(being_ref)
        self.get("Cemetery").bury_being(being_ref)

    def move_on_board(self, reference=None):
        being_id = reference["id"]
        categ = reference["category"]
        # being = self.get_concrete_thing(being_id)
        # self.get("Logger").add(f" {categ}.{being_id} movendo... file={__name__}:{line()}")
        self.roll_dice_to_move(being_id)
    

    def roll_dice_to_move(self, _id: str):
        result = self.roll_dice(_id)
        self.choose_spot_to_move(_id, result)
    
    def gui_output(self, text, color=None,end='\n',pause=False):
        pass

    def gui_input(self, _id=None, function=None, question_id=None, params=None):
        if function == "choose_spot_to_move":
            return random.choice(params["valid_spots"])
        if function == "interact_with":
            return random.choice(params["interactions"])
        if function == 'eat_food':
            return random.randrange(1, params)
        log_error(f"There is no action made for {function}",__name__,line())
        # return None
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
        # if(_id == '13'):
        #     self.get("Logger").add(f" Robber 13 choose_spot_to_move... file={__name__}:{line()}")

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
        if(self.get_category() == "PlayerIM"): self.get("GameManager").print_game()
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
        
        
        pref = self.reference(player["id"])
        name = self.person_name(pref)
        if entity_ref is None:
            self.gui_output(f"Movendo {name} para {spot}... ")
            board.move_entity_to(reference=pref, alphanum=spot)
        else:
            entity = self.get_concrete_thing_by_ref(entity_ref)
            name = self.person_name(entity_ref)
            self.gui_output(f"Movendo {name} para p/ interagir com {name}... ")
            self.move_to_and_interact_with(self.reference(_id), entity_ref)
        
        # if(_id == '13'):
        #     input("Deu certo?")
    


    def move_to_and_interact_with(self, me_ref, other_ref):
        e : Event = self.get("Event")
        board : Board = self.get("Board")
        other = self.get_concrete_thing_by_ref(other_ref)
        board.move_entity_to(reference=self.reference(me_ref["id"]), coord=other["coord"])
        # hey, I'm gonna interact!
        self.interact_with(me_ref, other_ref)
        # e.notify("entity_interacting_with_entity", me_ref, other_ref)

    
    def person_name(self, person_ref,last=bcolors.ENDC):
        person = self.get_concrete_thing_by_ref(person_ref)
        name = person['name']

        return f"{self.categ_color}{name}{last}"

    def interact_with(self, me_ref, other_ref):
        # print_debug(f"indo interagir com {other_ref}",__name__,line())
        target : Entity = self.get(other_ref["category"])
        myself : Entity = self.get(me_ref["category"])
        # get what ways it can interact
        interactions = target.get_interactions_for(me_ref)
        if(len(interactions) == 0): 
            # print_debug(f":( não dá para interagir com {other_ref}",__name__,line())
            
            return

        params = {"interactions":interactions, "other_ref":other_ref}
        target_concr = self.get_concrete_thing_by_ref(other_ref)
        target_name = self.person_name(other_ref)


        interac_nicks = list(interactions.values())
        interac_keys = list(interactions.keys())

        if(len(interactions) > 1): 
            myself.gui_output(f"")
            myself.gui_output(get_number_list(interac_nicks, title=f"Escolha uma opção para interagir com {target_name} (ENTER p/ cancelar)\n"))
            while True:
                myself.gui_output("Opção: ",end='')
                option = myself.gui_input(me_ref["id"], "interact_with", 1, params)
                if(len(option) == 0):
                    return
                if(option in interac_keys):
                    break
                if(valid_number(option, 1, len(interac_nicks))):
                    option = interac_keys[int(option)-1]
                    break
        else:
            option = interac_keys[0]
        
        # print_debug(f"indo interagir com {other_ref} rodando sua função {option}",__name__,line())
        
        target.run_func(option, me_ref, other_ref)
    
    def get_weapon_attack(self, being_ref):
        return 0

    def get_attack(self, being_ref):
        being_class : LivingBeing = self.get(being_ref["category"])
        being_class.gui_output("Jogue o dado para calcular o aumento de dano [1 a 3]: ")
        while True:
            try:
                attack = being_class.roll_dice(being_ref["id"], 3)
            except:
                log_error(f'cant roll dice for {being_ref}, returning rand 3',__name__,line())
                return random.randrange(1,3)
            # fix validade attack
            break

        return int(attack) + self.get_weapon_attack(being_ref)

    def is_dead(self, ref=None):
        concr = self.get_concrete_thing_by_ref(ref)
        if(not concr):
            # fix remove this log?
            log_error(f"{ref} isn't in the game to check if it is dead",__name__,line())
            return True
        # debug_error(f"achei? concr= {concr}",__name__)
        return concr[self.attr_hp] == 0

    def be_attacked(self, attacker_ref, me_ref, add_info='atacou'):
        e : Event = self.get('Event')
        total_damage = self.get_attack(attacker_ref)
        if total_damage is None: return False
        atk_nick = 'Soco'
        attacker = self.get_concrete_thing_by_ref(attacker_ref)
        me = self.get_concrete_thing_by_ref(me_ref)
        if not attacker: return False
        if not me: return False
        atk_name = self.person_name(attacker_ref)
        me_name = self.person_name(me_ref)
        dmg_info = f"com um/a {atk_nick} e dano {total_damage}💜"
        death_info = {'type':'killed', 'info':f"assasinado por {atk_name} {dmg_info}"}
        self.reduce_hp(me_ref, total_damage, death_info)
        if not self.is_dead(ref=me_ref):
            self.get("Logger").add(f"{atk_name} {add_info} {me_name} {dmg_info}")
        else:
            e.notify('being_killed_being', attacker_ref, {'years_in_prision': penalty.KILL})
            return False
        e.notify('being_attacked_being', attacker_ref, {'years_in_prision': penalty.ATTACK})
        return True

    def risk_of_death(self, being_concr=None, being_ref=None) -> int:
        if being_ref is not None:
            being_concr = self.get_concrete_thing_by_ref(being_ref)
        if self.attr_age not in being_concr: return 0
        age = being_concr[self.attr_age]

        risks = [
            # {"age_range": (0, 60), "risk": (50, 100)},
            {"age_range": (0, 60), "risk": (1, 5)},
            {"age_range": (60, 120), "risk": (5, 20)},
            {"age_range": (120, 130), "risk": (20, 99)},
        ]

        for risk in risks:
            i = risk["age_range"][0]
            f = risk["age_range"][1]
            if age in range(i, f):
                r = scale(age, risk["age_range"], risk["risk"])
                return int(r)

        return 99
            # {'range':range(0, )}
    
    # def eat_food

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


    



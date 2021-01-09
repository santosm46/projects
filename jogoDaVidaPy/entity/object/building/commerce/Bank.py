
from utils.beauty_print import debug_error, print_beauty_json, print_debug
from game.DataStructure import DataStructure
from entity.livingbeing import person
from game.Logger import Logger
from entity.object.Object import Object
from utils.common import MOCK_ID, line, log_error
from game.Board import Board
from game.Event import Event

from entity.object.building.commerce.Commerce import Commerce

class Bank(Commerce):


    def __init__(self) -> None:
        super().__init__()
    


    # def update_subscriber(self, school_ref):
        # event : Event = self.get("Event")
        # event.subscribe("entity_moved_to_coord", school_ref, "put_person_on_school")
        # event.subscribe("building_board_print", school_ref, "on_building_board_print")
        # event.subscribe("entity_choosing_spot", school_ref, "on_entity_choosing_spot")
        # event.subscribe("entity_interacting_with_building", school_ref, "person_school_interaction")



    def new_concrete_thing(self):
        bank = super().new_concrete_thing()
        self.update_concrete(bank)
        board : Board = self.get("Board")
        bank["id"] = MOCK_ID
        bank[self.attr_name] = "Banco"
        bank[self.attr_money] = 10000000
        # bank[self.attr_owner] = 10000000
        bank[self.attr_coord] = board.alphanum_to_coord("H7")
        self.update_subscriber(self.reference(bank["id"]))

        return bank

    
    def not_has_attr_money(self, entity):
        if(self.attr_money not in entity):
            log_error(f"Can't transfer money, entity doesn't have attr_money\n     -> {entity}",__name__,line())
            return False

    def transfer_money_from_to(self, sender_ref, receiver_ref, amount):
        if amount <= 0: return False
        
        sender = self.get_concrete_thing_by_ref(sender_ref)
        receiver = self.get_concrete_thing_by_ref(receiver_ref)

        # sender has to have sufficient money
        # already checks if it has attr money
        if(not self.entity_can_pay(sender, amount)):
            return False

        # receiver needs to have attr money
        if(self.not_has_attr_money(receiver)):
            return False

        sender[self.attr_money] -= amount
        receiver[self.attr_money] += amount

        return True

    def transfer_from_bank_to(self, receiver_ref, amount):
        # bank = self.get
        if(not self.transfer_money_from_to(self.reference(MOCK_ID), receiver_ref, amount)):
            log_error(f"Bank has no money to pay {receiver_ref} value {amount}", __name__, line())
            return False
        return True

    def decrease_person_money(self, person_ref, amount):
        return self.transfer_money_or_the_rest(person_ref, self.reference(MOCK_ID), amount)

    def entity_can_pay(self, entity_concr: dict, amount: int):
        if self.not_has_attr_money(entity_concr):
            return False
        
        money = entity_concr[self.attr_money]

        return money >= amount
        

    def transfer_all_money(self, sender_ref, receiver_ref):
        sender = self.get_concrete_thing_by_ref(sender_ref)
        receiver = self.get_concrete_thing_by_ref(receiver_ref)
        # debug_error(f"bag_ref = {receiver_ref}",__name__,line())
        # debug_error(f"send = {sender},  bag_ref = {receiver}",__name__,line())

        if(self.not_has_attr_money(sender)):
            return False
        if(self.not_has_attr_money(receiver)):
            return False
        

        all_money = sender[self.attr_money]
        if(all_money < 0):
            log_error(f"entity {sender_ref} has negative money",__name__, line())
            return False
        
        sender[self.attr_money] = 0

        receiver[self.attr_money] += all_money

        return True

    # tries to transfer money amount, if doesn't have the money required, transfer the rest
    def transfer_money_or_the_rest(self, sender_ref, receiver_ref, amount):
        
        if(not self.transfer_money_from_to(sender_ref, receiver_ref, amount)):
            if(not self.transfer_all_money(sender_ref, receiver_ref)):
                return False
        return True
    
    def put_all_money_on_board(self, entity_ref):
        bag : MoneyBag = self.get("MoneyBag")
        person = self.get_concrete_thing_by_ref(entity_ref)
        moneybag = bag.new_concrete_thing()
        # print_debug(f"\n\t-> p={person}\n\t-> m={moneybag}",__name__,line())

        moneybag[self.attr_coord] = person[self.attr_coord]
        data : DataStructure = self.get("DataStructure")
        data.keep_concrete_thing(moneybag["id"], moneybag, bag.get_category())
        bag_ref = bag.reference(moneybag["id"])
        self.transfer_all_money(entity_ref, bag_ref)

        
    


class MoneyBag(Object):

    def __init__(self):
        super().__init__()
        self.attr_money = "money"
    
    def new_concrete_thing(self):
        bag = super().new_concrete_thing()
        self.update_concrete(bag)
        self.update_subscriber(self.reference(bag["id"]))
        # bag[self.mon]
        # print_debug(f"esse foi o saco de $ criado...",__name__,line())
        # print_beauty_json(bag)
        return bag
    
    def get_image(self, _id=None):
        return '💰'


    def update_subscriber(self, reference: dict):
        super().update_subscriber(reference)
        e : Event = self.get("Event")


    def update_concrete(self, concrete: dict):
        super().update_concrete(concrete)
        self.add_attr_if_not_exists(concrete, self.attr_money, 0)

    def entity_entered_my_spot(self, myself_ref, entity_ref):
        self.entity_stepped_on_money(myself_ref, entity_ref)

    
    def entity_stepped_on_money(self, interested, event_causer, additional=None):
        # print_debug(f"{event_causer} pisou no dinheiro {interested} ",__name__,line())
        log : Logger = self.get("Logger")
        moneybag = self.get_concrete_thing_by_ref(interested)
        money = moneybag[self.attr_money]
        bank : Bank = self.get("Bank")
        bank.transfer_all_money(interested, event_causer)

        name = self.get(event_causer['category']).person_name(event_causer)
        log.add(f"{name} achou um saco de dinheiro com R$ {money}")

        self.delete_myself(interested)


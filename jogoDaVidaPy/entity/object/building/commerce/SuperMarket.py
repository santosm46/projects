from entity.object.building.commerce.Bank import Bank
from math import trunc
from utils.beauty_print import input_question, print_debug, print_normal, print_number_list, print_sucess
from entity.object.Food import Food
from game.Board import Board
from entity.object.building.commerce.Commerce import Commerce
from utils.common import MOCK_ID, line, log_error, prim_opt, valid_number




class SuperMarket(Commerce):


    def __init__(self) -> None:
        # self.interactions['buy_food'] = 'comprar comida'
        super().__init__()
    
    # def get_interactions_for(self, me_ref):
    #     return self.interactions


    def new_concrete_thing(self):
        market = super().new_concrete_thing()
        self.update_concrete(market)
        board : Board = self.get("Board")
        market["id"] = MOCK_ID
        market[self.attr_name] = "Super Mercado"
        market[self.attr_money] = 100
        # market[self.attr_owner] = 10000000
        market[self.attr_coord] = board.alphanum_to_coord("C2")
        self.update_subscriber(self.reference(market["id"]))

        return market

    def food_categs_to_options(self, food_categ_list):
        options = []
        food_dict = []
        food_names = []

        food : Food = self.get("Food")

        # food_values = food.food_info.values()

        for name in food_categ_list:
            food_names.append(name)
            info = food.food_info[name]
            imgage = info[food.i_image]
            energy = info[food.i_energy]
            price = info[food.i_price]
            health = info[food.i_health]
            opt = f"{imgage}: {energy}⚡ {price}💲 {health}💜"
            food_dict.append(info)
            options.append(opt)
        
        return options, food_dict, food_names

    def on_building_interact(self, building_ref, person_ref, additional=None):
        
        bank : Bank = self.get("Bank")
        food : Food = self.get("Food")

        options, food_dict, food_names = self.food_categs_to_options(list(food.food_info.keys()))
        
        while True:

            print_number_list(options, "\nEscolha uma comida [ENTER para sair]\n")

            while True:
                opt = input_question("Opção: ")
                if(len(opt) == 0):
                    self.remove_from_building(additional, person_ref)
                    return
                if(valid_number(opt, 1, len(options))):
                    break
            
            opt = int(opt)-1

            person = self.get_concrete_thing_by_ref(person_ref)
            
            out = ''

            while True:
                qtd = input_question("Quantidade [ENTER para sair]: ")
                if(len(qtd) == 0):
                    self.remove_from_building(additional, person_ref)
                    return
                if(not valid_number(opt, 0, 1000)):
                    continue
                qtd = int(qtd)
                price = food_dict[opt][food.i_price] * qtd
                out += f"Deu {price}, "
                if(not bank.entity_can_pay(person, price)):
                    out += "você não tem dinheiro para isso, escolha outra quantidade\n"
                    print_normal(out)
                    continue
                

                out += f"Aperte enter para continuar compra, {prim_opt.LEAVE} para sair do mercado, ou outra coisa para ver outras comidas\n"
                cont = input_question(out)
                if(cont == prim_opt.LEAVE):
                    self.remove_from_building(additional, person_ref)
                    return
                if(len(cont) > 0):
                    break

                bank.transfer_money_from_to(person_ref, additional, price)
                self.add_to_inventory(person_ref, food_names[opt], qtd)
                food_name = food_names[opt]
                print_sucess(f"você comprou {qtd} unidades de {food_name}.")
                break




    
    def add_to_inventory(self, being_ref, food_to_add, quantity):
        being = self.get_concrete_thing_by_ref(being_ref)
        inventory = being["inventory"]
        if("Food" not in inventory):
            inventory["Food"] = {}
        if(food_to_add not in inventory["Food"]):
            inventory["Food"][food_to_add] = 0
        inventory["Food"][food_to_add] += quantity
        
    




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

        self.work_nick = 'Caixa de supermercado'

        self.wage_multipl = 30
    
    # def get_interactions_for(self, me_ref):
    #     return self.interactions
    def can_work_here(self, person_ref):
        return self.get('School').person_has_highest_level(person_ref)

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

    

    def on_building_interact(self, building_ref, person_ref, additional=None):
        
        bank : Bank = self.get("Bank")
        food : Food = self.get("Food")

        options, food_dict, food_names = food.food_categs_to_options(list(food.food_info.keys()))
        
        while True:

            print_number_list(options, "\nEscolha uma comida [ENTER para sair]\n")

            while True:
                opt = input_question("Opção: ")
                if(len(opt) == 0):
                    self.remove_from_building(building_ref, person_ref)
                    return
                if(valid_number(opt, 1, len(options))):
                    break
            
            opt = int(opt)-1

            person = self.get_concrete_thing_by_ref(person_ref)
            
            out = ''

            while True:
                qtd = input_question("Quantidade [ENTER para sair]: ")
                if(len(qtd) == 0):
                    self.remove_from_building(building_ref, person_ref)
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
                    self.remove_from_building(building_ref, person_ref)
                    return
                if(len(cont) > 0):
                    break

                bank.transfer_money_from_to(person_ref, building_ref, price)
                food.add_to_inventory(person_ref, food_names[opt], qtd)
                food_name = food_names[opt]
                print_sucess(f"você comprou {qtd} unidades de {food_name}.")
                break




    
    



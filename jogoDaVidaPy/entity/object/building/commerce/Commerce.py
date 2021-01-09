from entity.object.building.Building import Building

from utils.beauty_print import input_question, print_debug, print_normal, print_number_list, print_sucess
from utils.common import MOCK_ID, line, log_error, prim_opt, valid_number




class Commerce(Building):

    def __init__(self) -> None:
        super().__init__()
        self.sell_item_class = 'Unknown'
        self.sell_nick = 'unkn'
        self.qtd_min = 1
        self.qtd_max = 1000


    def on_building_interact(self, building_ref, person_ref, additional=None):
        
        bank : Bank = self.get("Bank")
        food : Object = self.get(self.sell_item_class)

        options, item_dict, item_names = food.item_categs_to_options(list(food.items_info.keys()))
        
        while True:

            print_number_list(options, f"\nEscolha um/a {self.sell_nick} [ENTER para sair]\n")

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
                qtd = self.choose_quantity(building_ref, person_ref)
                if not qtd: return

                price = item_dict[opt][food.i_price] * qtd
                out += f"Deu {price}, "
                if(not bank.entity_can_pay(person, price)):
                    out += "você não tem dinheiro para isso, escolha outra coisa\n"
                    print_normal(out)
                    break
                
                commerce_name = self.get_concrete_thing_by_ref(building_ref)['name']
                out += f"Aperte enter para continuar compra, {prim_opt.LEAVE} para sair do/a {commerce_name}, ou outra coisa para ver outras {self.sell_nick}s\n"
                cont = input_question(out)
                if(cont == prim_opt.LEAVE):
                    self.remove_from_building(building_ref, person_ref)
                    return
                if(len(cont) > 0):
                    break

                bank.transfer_money_from_to(person_ref, building_ref, price)
                food.add_to_inventory(person_ref, item_names[opt], qtd)
                item_name = item_names[opt]
                print_sucess(f"você comprou {qtd} unidades de {item_name}.")
                break


    def choose_quantity(self, building_ref, person_ref):
        while True:
            qtd = input_question("Quantidade [ENTER para sair]: ")
            if(len(qtd) == 0):
                self.remove_from_building(building_ref, person_ref)
                return None
            if(not valid_number(qtd, self.qtd_min, self.qtd_max)):
                continue
            return int(qtd)






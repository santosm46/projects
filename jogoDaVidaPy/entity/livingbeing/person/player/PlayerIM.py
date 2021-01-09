from game.Event import Event
from utils.beauty_print import *
from utils.common import line, prim_opt, valid_number, clear, is_integer
from game.DataStructure import DataStructure
from game.Board import Board
from game.Logger import Logger

from entity.livingbeing.person.player.Player import Player



class PlayerIM(Player):

    def __init__(self):
        super().__init__()

    # called on set_factory() -> update_subscribers()
    # def update_subscribers(self):
        
        # dar subscribe em building_board_print,
        # para quando o board for montar o seu print, o Player pegar
        # todos os jogadores que estão em partida e inserir
        # na lista da board de coisas para imprimir 
        

    MAX_ENERGY = 30

    def being_move(self, being_id):
        pass


    def player_move(self, player_id):
        # player = self.get_players()[player_id]
        player = self.get_concrete_thing(player_id)
        # execute a function according to the mode of the player
        self.modes_func[player[self.attr_mode]](self.reference(player_id))

    # new_concrete_thing
    def create_player(self, name):
        data : DataStructure = self.get("DataStructure")

        player = self.new_concrete_thing()
        self.update_concrete(player)
        board : Board = self.get("Board")
        
        player[self.attr_name] = name
        player[self.attr_money] = 200
        player[self.attr_energy] = self.MAX_ENERGY
        player[self.attr_max_energy] = self.MAX_ENERGY
        player[self.attr_dice_method] = "DiceRollOrRandom"
        player[self.attr_coord] = board.rc_to_coord(0, 0)
        # self.add_attr_if_not_exists(player, self.attr_dice_method, "DiceRollOrRandom")

        data.keep_concrete_thing(player["id"], player, self.get_category())
    

    def update_concrete(self, player: dict):
        # print_debug("chamadooooooooooooooooooooooo",__name__,line())
        super().update_concrete(player)
        self.add_attr_if_not_exists(player, self.attr_energy, self.MAX_ENERGY)
        self.add_attr_if_not_exists(player, self.attr_max_energy, self.MAX_ENERGY)
        


    def move_on_board(self, params=None):
        player_id = params["id"]
        player = self.get_concrete_thing(player_id)
        name = player["name"]

        while(player_id == self.get("GameManager").turn_of()):
            print_normal(f"\nEscolha uma opção")
            print_normal(f"\tENTER) Jogar dado")
            if("Food" in player["inventory"]):
                print_normal(f"\t{prim_opt.EAT_FOOD}) Comer")
            print_normal(f"\t{prim_opt.PASS_TURN}) Passar vez")
            # print_normal(f"\t{prim_opt.SAVE}) Salvar")
            # print_normal(f"\t{prim_opt.EXIT}) Sair")
            print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e sair para menu da partida")
            option = input_question("\nOpção: ").upper()

            if(option == prim_opt.PASS_TURN):
                # print_normal("Passando vez...  ENTER para confirmar ou outra coisa para cancelar\n")
                print_normal(f"Passando vez de {name}...  \n")
                # if len(input("")) == 0:
                break
            elif(option == prim_opt.ROLL_DICE):
                self.roll_dice_to_move(player_id)
                break
            elif(option == prim_opt.EAT_FOOD):
                if(not self.eat_food(player_id)):
                    a = self.get_concrete_thing(player_id)
                    print_debug(f"O jogador {player_id} morreu comendo",__name__,line())
                    break
                # break
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.get("GameManager").stop()
                self.get("GameManager").save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                input("")
        
    

    def create_players(self):
        clear()
        created_players = 0
        
        while(True):
            print_header("\tCriação ou adicionar jogadores fora da partida\n")
            print_warning("\t\tobs: Aperte ENTER para sair\n")
            players_oom = self.get("GameManager").player_oom.get_players_list()
            print_header("Fora da partida: ")
            self.print_players_list(players_oom)


            print_normal("\nNome do jogador para criá-lo")
            name = input_question("  ou o N° de alguém para adicionar na partida: ")
            if(len(name) == 0):
                break
            if(is_integer(name)):
                self.add_player_on_match(name)
            else:
                clear()
                self.create_player(name)
                created_players += 1
                print_sucess(f"Jogador {name} criado!\n")
        
        self.get("GameManager").save()
        print_sucess(f"Foram criados {created_players} jogadores")
    
    

    
    # def on_school_move(self, params=None):
    #     person = self.get_concrete_thing(params["id"])
    #     name = person["name"]
    #     print_warning(f"Pessoa {name} está na escola")
    


    def gui_output(self, text, color=bcolors.ENDC, end='\n',pause=False):
        print_header(f"{color}{text}{bcolors.ENDC}",end=end)
        if pause:
            input("")

    def gui_input(self, _id=None, function=None, question_id=None, params=None):
        return input_question("")

    # def kill_being(self, being_ref, cause=None):
    #     if not cause:
    #         cause = ''
        # player = self.get_concrete_thing_by_ref(being_ref)
        # self.drop_inventory(being_ref)
        # person = self.get_concrete_thing_by_ref(being_ref)
        # name = person["name"]
        # categ = being_ref["category"]
        # log : Logger = self.get("Logger")
        # log.add(f"[{categ}] {name} morreu! {cause}", color=bcolors.FAIL)
        # data : DataStructure = self.get("DataStructure")
        # self.remove_player(being_ref["id"])
        # try:
        # super().kill_being(being_ref, cause)
        # except:

        # data.data["PlayerOOM"][being_ref["id"]] = player




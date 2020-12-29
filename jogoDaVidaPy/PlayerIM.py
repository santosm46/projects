from Event import Event
from beauty_print import *
from common import *
from Player import Player
from DataStructure import DataStructure
from Board import Board, spot_type
from common import MOCK_ID

class PlayerIM(Player):

    def __init__(self):
        super().__init__()

    # called on set_factory() -> update_subscribers()
    def update_subscribers(self):
        event : Event = self.get("Event")
        # dar subscribe em building_board_print,
        # para quando o board for montar o seu print, o Player pegar
        # todos os jogadores que estão em partida e inserir
        # na lista da board de coisas para imprimir 
        event.subscribe("building_board_print", self.reference(MOCK_ID), "on_building_board_print")



    def player_move(self, player_id):
        # player = self.get_players()[player_id]
        player = self.get_concrete_thing(player_id)
        # execute a function according to the mode of the player
        self.modes_func[player[self.attr_mode]](self.reference(player_id))
 
        # self.get("GameManager").pass_turn()

    def roll_dice_to_move(self, _id: str):
        result = self.roll_dice(_id)
        self.choose_spot_to_move(_id, result)
        

    # new_concrete_thing
    def create_player(self, name):
        data : DataStructure = self.get("DataStructure")

        player = self.new_concrete_thing()
        self.update_concrete(player)
        
        player[self.attr_name] = name
        player[self.attr_dice_method] = "DiceRollOrRandom"
        # self.add_attr_if_not_exists(player, self.attr_dice_method, "DiceRollOrRandom")

        data.keep_concrete_thing(player["id"], player, self.get_category())
    

    def update_concrete(self, player: dict):
        super().update_concrete(player)
        


    def move_on_board(self, params=None):
        player_id = params["id"]
        name = self.get_concrete_thing(player_id)["name"]
        
        while(player_id == self.get("GameManager").turn_of()):
            print_normal(f"\nEscolha uma opção")
            print_normal(f"\tENTER) Jogar dado")
            print_normal(f"\t{prim_opt.PASS_TURN}) Passar vez")
            print_normal(f"\n")
            # print_normal(f"\t{prim_opt.SAVE}) Salvar")
            # print_normal(f"\t{prim_opt.EXIT}) Sair")
            print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e sair para menu da partida")
            option = input_question("\nOpção: ").upper()

            if(option == prim_opt.PASS_TURN):
                # print_normal("Passando vez...  ENTER para confirmar ou outra coisa para cancelar\n")
                print_normal(f"Passando vez de {name}...  \n")
                # if len(input("")) == 0:
                break
            if(option == prim_opt.ROLL_DICE):
                self.roll_dice_to_move(player_id)
                
                break
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.get("GameManager").stop()
                self.get("GameManager").save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                input("")
        
    
    def choose_spot_to_move(self, _id, range_):
        player = self.get_concrete_thing(_id)
        board : Board = self.get("Board")
        valid_spots = board.get_valid_spots_for_range(player["coord"], range_)
        buildings = []
        buildings_list = {}
        if(len(valid_spots) == 0):
            print_normal("Não há lugares para ir")
            return
        event : Event = self.factory.gi("Event")
        event.notify("entity_choosing_spot", self.reference(player["id"]), 
            {"spots":valid_spots, "buildings":buildings, "range":range_, "buildings_list":buildings_list})
        spot = None
        self.get("GameManager").print_game()
        print_sucess(f"Resultado do dado: {range_}")
        print_header("\nLugares disponíveis\n")
        print_normal(", ".join(buildings))
        print_number_list(valid_spots, title="", layed=True)
        while True:
            option = input_question("\n\nDigite a casa ou o valor correspondente: ").upper()
            if option in valid_spots:
                spot = option
                break
            if(valid_number(option, 1, len(valid_spots))):
                spot = valid_spots[int(option)-1]
                break
        place = spot
        if spot in buildings_list:
            place = buildings_list[spot]
        name = player["name"]
        print_normal(f"Movendo {name} para {place}... ", end='')
        board.move_entity_to(reference=self.reference(player["id"]), alphanum=spot)

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
    
    
    
    def on_building_board_print(self, interested=None, event_causer=None, additional=None):
        # pegar lista de id's dos jogadores IM
        players_im : dict = self.get_players()

        category = self.get_category()
        if(category not in additional):
            additional[category] = []

        for player_id, player in players_im.items():
            additional[category].append({
                "image": self.get_image(player_id),
                "coord": player["coord"]
            })

    
    # def on_school_move(self, params=None):
    #     person = self.get_concrete_thing(params["id"])
    #     name = person["name"]
    #     print_warning(f"Pessoa {name} está na escola")
    


    def gui_output(self, text, color=bcolors.ENDC, end='\n',pause=False):
        print_header(f"{color}{text}{bcolors.ENDC}",end=end)
        if pause:
            input("")



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
        self.modes_info["on_board"] = {"func":self.move_on_board}

        


    def set_factory(self, factory):
        super().set_factory(factory)
    
    

    def setup(self, game):
        super().setup(game)
        # dar subscribe em building_board_print,
        # para quando o board for montar o seu print, o Player pegar
        # todos os jogadores que estão em partida e inserir
        # na lista da board de coisas para imprimir 
        # não é necessário verificar se já deu subscribe pois o event já faz isso
        event : Event = self.factory.get_instance("Event")
        event.subscribe("building_board_print", 
            self.reference(MOCK_ID),
            "on_building_board_print")



    def player_move(self):
        player_id = self.game.turn_of()
        player = self.get_players()[player_id]
        if("mode" not in player):
            # because old saves doesn't have "mode"
            player["mode"] = "on_board"
        self.modes_info[player["mode"]]["func"]({"id":player_id})
 
        self.game.pass_turn()

    def roll_dice_for(self, _id: str):
        player = self.get_concrete_thing(_id)
        dice = self.factory.get_instance(player["dice_method"])
        result = dice.roll_dice()
        print_sucess(f"Resultado do dado: {result}")
        self.choose_spot_to_move(player, result)

    # new_concrete_thing
    def create_player(self, name):
        data : DataStructure = self.factory.get_instance("DataStructure")

        concrete_player = self.new_concrete_thing()
        # debug_error(f"concrete_player = {concrete_player}",__name__)

        concrete_player["name"] = name
        concrete_player["dice_method"] = "DiceRollOrRandom"

        data.keep_concrete_thing(concrete_player["id"], concrete_player, self.get_category())

    def move_on_board(self, params=None):
        player_id = params["id"]
        
        while(player_id == self.game.turn_of()):
            print_normal(f"\nEscolha uma opção")
            print_normal(f"\t{prim_opt.PASS_TURN}) Passar vez")
            print_normal(f"\t{prim_opt.ROLL_DICE}) Jogar dado")
            print_normal(f"\n")
            # print_normal(f"\t{prim_opt.SAVE}) Salvar")
            # print_normal(f"\t{prim_opt.EXIT}) Sair")
            print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e sair para menu da partida")
            option = input_question("\nOpção: ").upper()

            if(option == prim_opt.PASS_TURN):
                print_normal("Passando vez...  ENTER para confirmar ou outra coisa para cancelar\n")
                if len(input("")) == 0:
                    break
            if(option == prim_opt.ROLL_DICE):
                self.roll_dice_for(player_id)
                
                break
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.game.stop()
                self.game.save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                input("")
        
    
    def choose_spot_to_move(self, player, range_):
        board : Board = self.factory.get_instance("Board")
        valid_spots = board.get_valid_spots_for_range(player["coord"], range_)
        buildings = []
        if(len(valid_spots) == 0):
            print_normal("Não há lugares para ir")
            return
        event : Event = self.factory.gi("Event")
        event.notify("entity_choosing_spot", 
            self.reference(player["id"]), 
            {"spots":valid_spots, "buildings":buildings, "range":range_})
        spot = None
        self.game.print_game()
        print_header("\nLugares disponíveis\n")
        print_normal(", ".join(buildings), end='')
        print_number_list(valid_spots, title="", layed=True)
        while True:
            option = input_question("\n\nDigite a casa ou o valor correspondente: ").upper()
            if option in valid_spots:
                spot = option
                break
            if(valid_number(option, 1, len(valid_spots))):
                spot = valid_spots[int(option)-1]
                break
        print_normal(f"Movendo para {spot}... ", end='')
        board.move_entity_to(reference=self.reference(player["id"]), alphanum=spot)
        input("[pressione ENTER para continuar] ")

    def create_players(self):
        clear()
        created_players = 0
        
        while(True):
            print_header("\tCriação ou adicionar jogadores fora da partida\n")
            print_warning("\t\tobs: Aperte ENTER para sair\n")
            players_oom = self.game.player_oom.get_players_list()
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
        
        self.game.save()
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

    


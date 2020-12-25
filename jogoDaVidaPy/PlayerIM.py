from beauty_print import *
from common import *
from Player import Player
from DataStructure import DataStructure
import random

class PlayerIM(Player):

    def __init__(self):
        super().__init__()
    

    def player_move(self):
        player_id = self.game.turn_of()
        
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
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.game.stop()
                self.game.save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                cont = input("")
        self.game.pass_turn()

    def roll_dice_for(self, _id: str):
        player = self.get_concrete_thing(_id)
        dice = self.factory.get_instance(player["dice_method"])
        result = dice.roll_dice()
        print_sucess(f"O valor do dado deu: {result}")
        input("")

    # new_concrete_thing
    def create_player(self, name):
        data : DataStructure = self.factory.get_instance("DataStructure")

        concrete_player = self.new_concrete_thing()
        print(concrete_player)

        concrete_player["name"] = name
        concrete_player["dice_method"] = "DiceRollOrRandom"


        data.keep_concrete_thing(concrete_player["id"], concrete_player, self.get_category())
    

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
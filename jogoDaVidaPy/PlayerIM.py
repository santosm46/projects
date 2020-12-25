from beauty_print import *
from common import *
from Player import Player
from DataStructure import DataStructure


class PlayerIM(Player):

    def __init__(self):
        super().__init__()
    

    def player_move(self):
        player_id = self.game.turn_of()
        
        while(player_id == self.game.turn_of()):
            print_normal(f"\nEscolha uma opção")
            print_normal(f"\t{prim_opt.PASS_TURN}) Passar vez")
            print_normal(f"\n")
            # print_normal(f"\t{prim_opt.SAVE}) Salvar")
            # print_normal(f"\t{prim_opt.EXIT}) Sair")
            print_normal(f"\t{prim_opt.SAVE_EXIT}) Salvar e sair para menu da partida")
            option = input_question("\nOpção: ").upper()

            if(option == prim_opt.PASS_TURN):
                print_normal("Passando vez...  ENTER para confirmar ou outra coisa para cancelar\n")
                if len(input("")) == 0:
                    break
            elif(option == prim_opt.SAVE_EXIT):
                print_sucess("Salvando e saindo...")
                self.game.stop()
                self.game.save()
                return
            else:
                print_error(f"Opção ({option}) inválida! pressione ENTER")
                cont = input("")
        self.game.pass_turn()

    # new_concrete_thing
    def create_player(self, name):
        data : DataStructure = self.factory.get_instance("DataStructure")
        new_id = self.game.generate_id()

        concrete_player = {
            "id": new_id,
            "name": name,
            "hp": MAX_HP,
            "max_hp": MAX_HP
        }

        data.keep_concrete_thing(new_id, concrete_player, self.get_category())
    

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
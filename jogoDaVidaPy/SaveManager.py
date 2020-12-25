#file -- SaveManager.py --
from os import truncate
from DataStructure import DataStructure
import json
from common import *
from beauty_print import *
from Thing import Thing

SAVES_PATH = './saves/'

class SaveManager(Thing):

    def __init__(self):
        super().__init__()

    def get_save_by_filename(self, filename):
        try:
            with open(f"{SAVES_PATH}{filename}", 'r+') as json_file:
                data_structure = json.load(json_file)
                return data_structure
        except:
            debug_error(f"Arquivo {filename} não existe!", fname=__name__, enabled=DEBUG_ENABLED)
            return None

    def load_save_to_strucure(self, filename, data_structure : DataStructure) -> bool:
        data = self.get_save_by_filename(filename)

        if(data is not None):
            data_structure.setup(data)
            return True

        return False

    def save_to_file(self, save):
        current_datetime = date_now()
        save[self.get_category()]["concrete_things"]["1"]["last_save_date"] = current_datetime
        filename = save[self.get_category()]["concrete_things"]["1"]["save_filename"]

        with open(f"{SAVES_PATH}{filename}", 'w') as outfile:
            json.dump(save, outfile)

    # def save_all(self, saves):
    #     with open(FILE_NAME, 'w') as outfile:
    #         json.dump(saves, outfile)

    def create_new_save(self):
        def valid_file_name(file_name):
            if(str_to_file_format(file_name) in get_saves_list()):
                print_error(f"Arquivo {file_name} já existe! Digite outra coisa")
                return False
            # implement more
            return True
        
        # criar e salvar uma nova estrutura
        save : DataStructure = self.factory.get_instance("DataStructure")

        clear()

        while True:
            game_name = input_question("Nome da nova partida: (ENTER para cancelar)\n").strip()

            if(len(game_name) == 0):
                return
            if(valid_file_name(game_name)):
                break

        save.new_data_structure()
        
        current_datetime = date_now()

        # dados do save (seria criado por new_concrete_thing)
        save_metadata = {
            "save_name": game_name,
            "save_filename": str_to_file_format(game_name),
            "last_id": 1,
            "turn_of": None,
            "last_save_date": current_datetime,
            "creation_date": current_datetime,
            "game_version": GAME_VERSION,
        }
        # salvando save_metadata na estrutura de dados
        save.data[self.get_category()]["concrete_things"]["1"] = save_metadata

        self.save_to_file(save.data)

        print_sucess(f"Partida \"{game_name}\" criado! Aperte ENTER para continuar.\n")
        cont = input("")

    def valid_save_value(self, value, size):
        if(not is_integer(value)):
            print_error("Digite um número")
            return False
        
        i = int(value)
        if(i < 1 or i > size):
            print_error(f"Digite um valor entre 1 e {size}")
            return False
        
        return True


    def load_save(self, save_filename=None):
        saves_list = get_saves_list()
        # get_save_by_filename

        if(save_filename is not None):
            return self.get_save_by_filename(save_filename)
        
        if(len(saves_list) == 0):
            print_warning("Não há partidas! Aperte ENTER para voltar e crie uma.")
            input("")
            return None

        clear()

        print_header("Partidas")
        for idx in range(len(saves_list)):
            print_normal(f"    {idx+1}) {saves_list[idx]}")


        while True:
            option = input_question("Digite o número da partida: (ENTER p/ cancelar)\n")
            if(len(option) == 0):
                return None
            if(self.valid_save_value(option, len(saves_list))):
                break

        filename = saves_list[int(option)-1]
        # print_normal(f"Você escolheu \"{choice_name}\", pressione ENTER para começar")
        # cont = input("")
        return self.get_save_by_filename(filename)


    def delete_save(self):
        
        clear()

        saves_names = get_saves_list()

        while True:
            if(len(saves_names) == 0):
                print_warning("Não há partidas salvas! Aperte ENTER para voltar.")
                input("")
                return
            
            print_header("Partidas")
            for idx in range(len(saves_names)):
                print_normal(f"    {idx+1}) {saves_names[idx]}")

            while True:
                idx = input_question(f"\nN° da partida que quer {bcolors.FAIL}Deletar{bcolors.OKBLUE} (ENTER para voltar): ")

                if(len(idx) == 0):
                    # print_normal("Deleção cancelada!\n")
                    return
                
                if(self.valid_save_value(idx, len(saves_names))):
                    break

            save_name = saves_names[int(idx)-1]

            sure = input_question(f"\nTem certeza que quer deletar a partida \"{save_name}\"? (S/N): ").upper()
            
            clear()
            if(sure == 'S'):
                os.system(f"rm {SAVES_PATH}{save_name}")
                print_sucess(f"Partida \"{save_name}\" deletada!\n")

            else:
                print_normal("Deleção cancelada!\n")

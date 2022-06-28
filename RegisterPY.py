# ======================= IMPORTS ==============================
import os

# ====================== CONSTANTS ==============================
ALL_REGS_FILE_NAME = 'register_set.bin'
REG_NUM_SIZE = 4
REG_NAME_SIZE = 5
REGISTER_SIZE = REG_NUM_SIZE + REG_NAME_SIZE


# ======================= CLASSES ==============================

# Classe Registrador
class Register:
    def __init__(self, num, name):
        self.num = num
        self.name = name

    def save_in_file(self, file):
        # SALVAR NOME DO REGISTRADOR
        numbin = self.num.to_bytes(REG_NUM_SIZE, byteorder='big', signed=False)
        file.write(numbin)

        # SALVAR NUM DO REGISTRADOR
        name_formated = self.name
        if len(name_formated) < REG_NAME_SIZE:
            filler = '\0' * (REG_NAME_SIZE - len(name_formated))
            name_formated = name_formated + filler
        namebin = name_formated.encode('ascii')
        file.write(namebin)

    def print_register(self):
        print(f'Registrador {self.num}\t{self.name}')


# ======================== FUNCTIONS =============================

def load_register_from_file(file):
    picked_num_bin = file.read(REG_NUM_SIZE)
    picked_num = int.from_bytes(picked_num_bin, byteorder='big', signed=False)

    picked_name_bin = file.read(REG_NAME_SIZE)
    picked_name = picked_name_bin.decode('ascii')
    picked_name = picked_name.replace('\0', '')  # removendo caracteres nulos da string name

    return Register(picked_num, picked_name)


def print_register_file(file_name):
    print(f'=================== ARQUIVO: {file_name} ===================')
    file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    for i in range(0, file_size, REGISTER_SIZE):
        register = load_register_from_file(file)
        register.print_register()
    file.close()


def generate_register_dict(file_name):
    register_set_dict = dict({})

    reg_set_file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)

    for i in range(0, file_size, REGISTER_SIZE):
        register = load_register_from_file(reg_set_file)
        register_set_dict[register.num] = register

    reg_set_file.close()

    return register_set_dict

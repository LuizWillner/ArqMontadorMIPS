# ======================= IMPORTS ==============================

import os


# ====================== CONSTANTS ==============================

KEY_SIZE = 4
NAME_SIZE = 4
INST_TYPE_SIZE = 1
OPCODE_SIZE = 1
INST_FUNCT_SIZE = 1
INSTRUCTION_SIZE = KEY_SIZE + NAME_SIZE + INST_TYPE_SIZE + OPCODE_SIZE + INST_FUNCT_SIZE
ALL_INSTS_FILE_NAME = 'instruction_set.bin'


# ======================= CLASSES ==============================

# Classe Instrução
class Instruction:
    def __init__(self, name, inst_type, opcode, funct=None, key=None):
        self.name = name  # Nome da instrução (ex: ADD)
        self.type = inst_type  # Tipo da instrução (ex: R)
        self.opcode = opcode  # Opcode da instrução (ex: 0)
        self.funct = funct  # Valor do campo funct da instrução (ex: 32)

        # Gerar chave especial de cada instrução, caso não tenha sido passado como parâmetro
        if key is None:
            self.key = generate_key(name)
        else:
            self.key = key

    def save_in_file(self, file):
        # 4 BYTES
        keybin = self.key.to_bytes(KEY_SIZE, byteorder='big', signed=True)
        file.write(keybin)

        # 4 BYTES
        name_formated = self.name
        if len(name_formated) < NAME_SIZE:
            filler = '\0' * (NAME_SIZE - len(name_formated))
            name_formated = name_formated + filler
        namebin = name_formated.encode('ascii')
        file.write(namebin)

        # 1 BYTE
        typebin = self.type.encode('ascii')
        file.write(typebin)

        # 1 BYTE
        opcodebin = self.opcode.to_bytes(OPCODE_SIZE, byteorder='big', signed=True)
        file.write(opcodebin)

        # 1 BYTE
        funct_formated = self.funct
        if funct_formated is None:
            funct_formated = -1
        functbin = funct_formated.to_bytes(INST_FUNCT_SIZE, byteorder='big', signed=True)
        file.write(functbin)

    def print_instruction(self):
        print(f'Instruction {self.key}:', end=' ')
        print(f'name = {self.name} ', end='\t')
        print(f'type = {self.type}', end='\t')
        print(f'opcode = {self.opcode}', end='\t')
        print(f'funct = {self.funct}')


# ======================== FUNCTIONS ===============================

# Função para gerar chave exclusiva associada a uma string
def generate_key(string):
    key = 0
    i = NAME_SIZE - 1
    for char in string:
        key += ord(char) * 10 ** i
        i -= 1
    return key


# Função para usar no parâmetro key do sort e uma lista de instructions de acordo com a chave das instructions
def sort_by_instruction_key(instruction):
    return instruction.key


# Função para carregar uma Instrução do arquivo binário para a memória principal
def load_instruction_from_file(file):
    # ler KEY
    picked_key_bin = file.read(KEY_SIZE)
    picked_key = int.from_bytes(picked_key_bin, byteorder='big', signed=True)

    # ler NAME
    picked_name_bin = file.read(NAME_SIZE)
    picked_name = picked_name_bin.decode('ascii')
    picked_name = picked_name.replace('\0', '')  # removendo caracteres nulos da string name

    # ler TYPE
    picked_type_bin = file.read(1)
    picked_type = picked_type_bin.decode('ascii')

    # ler OPCODE
    picked_opcode_bin = file.read(OPCODE_SIZE)
    picked_opcode = int.from_bytes(picked_opcode_bin, byteorder='big', signed=True)

    # ler FUNCT
    picked_funct_bin = file.read(INST_FUNCT_SIZE)
    picked_funct = int.from_bytes(picked_funct_bin, byteorder='big', signed=True)
    if picked_funct == -1:
        picked_funct = None

    return Instruction(picked_name, picked_type, picked_opcode, picked_funct, picked_key)


def print_instruction_file(file_name):
    print(f'=================== ARQUIVO: {file_name} ===================')
    file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    for i in range(0, file_size, INSTRUCTION_SIZE):
        instruction = load_instruction_from_file(file)
        instruction.print_instruction()
    file.close()


def generate_instruction_dict(file_name):
    instruction_set_dict = dict({})

    inst_set_file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)

    for i in range(0, file_size, INSTRUCTION_SIZE):
        instruction = load_instruction_from_file(inst_set_file)
        instruction_set_dict[instruction.key] = instruction

    inst_set_file.close()

    return instruction_set_dict

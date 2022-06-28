# =========================== IMPORTS ============================

from InstructionPY import *
from RegisterPY import *
import ctypes


# ======================== CONSTANTS =============================

asm_file_name = 'exemplo'


# ======================== FUNCTIONS =============================

def generate_bitfield_list(command_line):
    command_line = command_line.upper()
    command_line = command_line.replace(',', ' ')
    command_line = command_line.replace('\n', '')

    bitfield_list = command_line.split()
    return bitfield_list


def int_to_binarystring(num, bits=16):
    num = int(num)
    if num >= 0:
        string_bin = bin(int(num))
        string_bin = string_bin.replace("0b", "")
        while len(string_bin) != bits:
            if len(string_bin) == bits:
                return string_bin
            string_bin = "0" + string_bin
        return string_bin
    else:
        string_bin = bin(ctypes.c_ushort(num).value)
        string_bin = string_bin.replace("0b", "")
        return string_bin


# ========================== MAIN ================================

# Gerar tabela do conjunto de Instruções
instruction_set_dict = generate_instruction_dict(ALL_INSTS_FILE_NAME)

# Gerar tabela do conjunto de Registradores
register_set_dict = generate_register_dict(ALL_REGS_FILE_NAME)

all_line_lists = []

print("Bem vindo ao Assembler MIPS!")
print('\nInsira o nome do arquivo .asm a ser codificado em binário')
# asm_file_name = input(">> ")
print('>>', asm_file_name)
asm_file_name = asm_file_name + '.asm'

asm_file = open(asm_file_name, "r")

print('\nEscolha uma opção de codificação (digite o número da escolha correspondente)')
print('\n[1] Codificar em .bin\t[2] Codificar em .txt')
code_flag = int(input('>> '))
if code_flag != 1 and code_flag != 2:
    print('\nOpção inválida! Abortando programa...')
    exit(1)

# Gerar matriz com listas de bitfields
for line in asm_file:
    line_list = generate_bitfield_list(line)
    all_line_lists.append(line_list)

for i in range(len(all_line_lists)):
    print(all_line_lists[i])

line_list = all_line_lists[0]
for bitfield in line_list:
    print()
    if bitfield[0] == '$':
        # achar registrador na tabela de registradores
        # processa register
        print('Registrador = ' + bitfield)
        pass
    else:
        try:
            key = generate_key(bitfield)
            instruction = instruction_set_dict[key]
            print('Instrução = ' + instruction.name)
            if instruction.name == 'SLL' or instruction.name == 'SRL':
                # faz algo
                pass
            else:
                opcode_binstring = int_to_binarystring(instruction.opcode, 6)
                print('Opcode em binario =', opcode_binstring)
                # faz outro algo
        except:
            # é uma label
            # processa label
            print('Label = ' + bitfield)
            pass


asm_file.close()

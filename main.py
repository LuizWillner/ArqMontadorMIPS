# =========================== IMPORTS ============================

from InstructionPY import *


# ======================== CONSTANTS =============================

asm_file_name = 'exemplo'


# ======================== FUNCTIONS =============================

def generate_bitfield_list(command_line):
    command_line = command_line.upper()
    command_line = command_line.replace(',', ' ')
    command_line = command_line.replace('\n', '')

    bitfield_list = command_line.split()
    return bitfield_list

# ========================== MAIN ================================

instruction_set_dict = generate_instruction_dict(FILE_NAME)

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

for line in asm_file:
    line_list = generate_bitfield_list(line)
    print(line_list)

asm_file.close()

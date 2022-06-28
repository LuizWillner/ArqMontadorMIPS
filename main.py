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


    # def generate_binary_string_for_instruction(instruction):


# ========================== MAIN ================================

# Gerar tabela do conjunto de Instruções
instruction_set_dict = generate_instruction_dict(ALL_INSTS_FILE_NAME)

# Gerar tabela do conjunto de Registradores
register_set_dict = generate_register_dict(ALL_REGS_FILE_NAME)

all_bitfield_lists = []

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
    all_bitfield_lists.append(line_list)

for i in range(len(all_bitfield_lists)):
    print(all_bitfield_lists[i])


bitfield_list = all_bitfield_lists[0]

i = 0
if ':' in bitfield_list[i]:
    i += 1
    inst_field = bitfield_list[i]
else:
    inst_field = bitfield_list[i]

instruction = instruction_set_dict[generate_key(inst_field)]
print('Instrução =', instruction.name)
opcode_binstring = int_to_binarystring(instruction.opcode, 6)
print('Opcode em binario =', opcode_binstring)
command_bin = opcode_binstring + ' '

# formatar command_bin para tipo R
if instruction.type == 'R':
    i += 1

    # Caso especial do tipo R: instruções SLL e SRL
    if instruction.name == 'SLL' or instruction.name == 'SRL':
        pass

    # Se não for um caso especial
    else:
        while i < len(bitfield_list):
            # Se o item da lista analisado começar com $, este item se trata de um REGISTRADOR
            if bitfield_list[i][0] == '$':
                register = register_set_dict[bitfield_list[i].lower()]
                print('Registrador = ' + register.name)
                regnum_binstring = int_to_binarystring(register.num, 5)
                print('Num do registrador em binário:', regnum_binstring)
                command_bin = command_bin + regnum_binstring + ' '  # adicionando campos dos registradores a cada iteração

            i += 1
        command_bin = command_bin + '00000' + ' '  # adicionando campo do shift ammount
        funct_binstring = int_to_binarystring(instruction.funct, 6)
        command_bin = command_bin + funct_binstring  # adicionando campo do funct


# formatar command_bin para tipo I
elif instruction.type == 'I':
    pass

# formatar command_bin para tipo J
else:
    pass


print('comando binário final =', command_bin)

asm_file.close()

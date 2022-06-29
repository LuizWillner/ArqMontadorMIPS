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

print_instruction_file(ALL_INSTS_FILE_NAME)

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

# Gerar comando em binário para a linha bitfield_list
bitfield_list = all_bitfield_lists[0]

i = 0
if ':' in bitfield_list[i]:
    i += 1
    inst_field = bitfield_list[i]
else:
    inst_field = bitfield_list[i]

instruction = instruction_set_dict[generate_key(inst_field)]
print('Instrução =', instruction.name)
command_bin = int_to_binarystring(instruction.opcode, 6)
print('Opcode em binario =', command_bin)
i += 1

# formatar command_bin para tipo R
if instruction.type == 'R':
    instR_dict = dict({
        'rs': None,
        'rt': None,
        'rd': None,
        'shamt': None,
        'funct': None
    })

    # Caso especial do tipo R: instruções SLL e SRL
    if instruction.name == 'SLL' or instruction.name == 'SRL':
        rd = bitfield_list[i]
        register_d = register_set_dict[rd.lower()]
        # print('Registrador = ' + register_d.name)
        instR_dict['rd'] = int_to_binarystring(register_d.num, 5)
        # print('Num do registrador em binário:', instR_dict['rd'])

        rs = bitfield_list[i+1]
        register_s = register_set_dict[rs.lower()]
        # print('Registrador = ' + register_s.name)
        instR_dict['rs'] = int_to_binarystring(register_s.num, 5)
        # print('Num do registrador em binário:', instR_dict['rs'])

        instR_dict['rt'] = '00000'

        shamt = int(bitfield_list[i+2])
        # print('SHAMT =', shamt)
        instR_dict['shamt'] = int_to_binarystring(shamt, 5)
        # print('SHAMT em binário:', instR_dict['shamt'])

        instR_dict['funct'] = int_to_binarystring(instruction.funct, 6)

    # Caso especial do tipo R: instrução JR
    elif instruction.name == "JR":
        # TODO: [processar]
        pass

    # Se não for um caso especial
    else:
        rd = bitfield_list[i]
        register_d = register_set_dict[rd.lower()]
        # print('Registrador = ' + register_d.name)
        instR_dict['rd'] = int_to_binarystring(register_d.num, 5)
        # print('Num do registrador em binário:', instR_dict['rd'])

        rs = bitfield_list[i+1]
        register_s = register_set_dict[rs.lower()]
        # print('Registrador = ' + register_s.name)
        instR_dict['rs'] = int_to_binarystring(register_s.num, 5)
        # print('Num do registrador em binário:', instR_dict['rs'])

        rt = bitfield_list[i+2]
        register_t = register_set_dict[rt.lower()]
        # print('Registrador = ' + register_t.name)
        instR_dict['rt'] = int_to_binarystring(register_t.num, 5)
        # print('Num do registrador em binário:', instR_dict['rt'])

        instR_dict['shamt'] = '00000'

        instR_dict['funct'] = int_to_binarystring(instruction.funct, 6)

    # Gerando comando em binário do tipo R final seguindo a ordem: opcode - rs - rt - rd - shamt - funct
    command_bin = command_bin + ' ' + instR_dict['rs'] + ' ' + instR_dict['rt'] + ' ' + instR_dict['rd'] + ' ' + instR_dict['shamt'] + ' ' + instR_dict['funct']


# formatar command_bin para tipo I
elif instruction.type == 'I':
    instI_dict = dict({
        'rs': None,
        'rt': None,
        'offset': None
    })

    # TODO: [processar]

    # Gerando comando em binário do tipo I final seguindo a ordem: opcode - rs - rt - offset
    command_bin = command_bin + ' ' + instI_dict['rs'] + ' ' + instI_dict['rt'] + ' ' + instI_dict['offset']


# formatar command_bin para tipo J
else:
    instJ_dict = dict({
        'address': None
    })

    # TODO: processar

    # Gerando comando em binário do tipo J final seguindo a ordem: opcode - address
    command_bin = command_bin + ' ' + instJ_dict['address']


print('comando binário final =', command_bin)

asm_file.close()

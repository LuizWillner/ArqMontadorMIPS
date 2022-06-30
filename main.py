# =========================== IMPORTS ============================

from InstructionPY import *
from RegisterPY import *
import ctypes


# ======================== CONSTANTS =============================

flags_in_file = dict({})


# ======================== FUNCTIONS =============================

def generate_bitfield_list(command_line):
    command_line = command_line.upper()
    command_line = command_line.replace(',', ' ')
    command_line = command_line.replace('\n', '')
    command_line = command_line.replace('(', ' ')
    command_line = command_line.replace(')', '')

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
# print_register_file('register_set.bin')

# print_instruction_file(ALL_INSTS_FILE_NAME)

all_bitfield_lists = []

print("Bem vindo ao Assembler MIPS!")
print('\nInsira o nome do arquivo .asm a ser codificado em binário')
# asm_file_name = input(">> ")
asm_file_name = input(">> ")
asm_file_name = asm_file_name + '.asm'

asm_file = open(asm_file_name, "r")

print('\nEscolha uma opção de codificação (digite o número da escolha correspondente)')
print('\n[1] Codificar em .bin\t[2] Codificar em .txt')
bin_or_txt = int(input('>> '))
if bin_or_txt != 1 and bin_or_txt != 2:
    print('\nOpção inválida! Abortando programa...')
    exit(1)
if bin_or_txt == 2:
    saida_file = open('saida.txt', 'w')
else:
    saida_file = open('saida.bin', 'wb')

# Gerar matriz com listas de bitfields
line = asm_file.readline()
while line:
    line_list = generate_bitfield_list(line)
    if ':' in line_list[0]:  # se tiver ':', é uma flag, então...
        # Adicionar flag no dicionario de flags junto com sua posição no arquivo
        flag_name = line_list[0].replace(':', '')
        flag_pos = asm_file.tell()
        flags_in_file[flag_name] = flag_pos
    all_bitfield_lists.append(line_list)
    line = asm_file.readline()  # passar pra próxima linha

# print(flags_in_file)

# for i in range(len(all_bitfield_lists)):
#     print(all_bitfield_lists[i])


# Gerar comando em binário para a linha de bitfield_list
for bitfield_list in all_bitfield_lists:
    i = 0

    if ':' in bitfield_list[i]:
        i += 1
        inst_field = bitfield_list[i]
    else:
        inst_field = bitfield_list[i]

    instruction = instruction_set_dict[generate_key(inst_field)]
    # ('Instrução =', instruction.name)

    # command_bin pode ser string ou binário dependendo do input do usuário
    if bin_or_txt == 2:
        command_bin = int_to_binarystring(instruction.opcode, 6)
        # print('Opcode em binario =', command_bin)
    else:
        command_bin = instruction.opcode.to_bytes(1, byteorder='big', signed=False)

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
            if bin_or_txt == 2:
                rd = bitfield_list[i]
                register_d = register_set_dict[rd.lower()]
                # print('Registrador = ' + register_d.name)
                instR_dict['rd'] = int_to_binarystring(register_d.num, 5)
                # print('Num do registrador em binário:', instR_dict['rd'])

                rs = bitfield_list[i + 1]
                register_s = register_set_dict[rs.lower()]
                # print('Registrador = ' + register_s.name)
                instR_dict['rs'] = int_to_binarystring(register_s.num, 5)
                # print('Num do registrador em binário:', instR_dict['rs'])

                instR_dict['rt'] = '00000'

                shamt = int(bitfield_list[i + 2])
                # print('SHAMT =', shamt)
                instR_dict['shamt'] = int_to_binarystring(shamt, 5)
                # print('SHAMT em binário:', instR_dict['shamt'])

                instR_dict['funct'] = int_to_binarystring(instruction.funct, 6)

            else:
                rd = bitfield_list[i]
                register_d = register_set_dict[rd.lower()]
                instR_dict['rd'] = register_d.num.to_bytes(1, byteorder='big', signed=False)

                rs = bitfield_list[i + 1]
                register_s = register_set_dict[rs.lower()]
                instR_dict['rs'] = register_s.num.to_bytes(1, byteorder='big', signed=False)

                zero = 0
                instR_dict['rt'] = zero.to_bytes(1, byteorder='big', signed=False)

                shamt = int(bitfield_list[i + 2])
                instR_dict['shamt'] = shamt.to_bytes(1, byteorder='big', signed=False)

                instR_dict['funct'] = instruction.funct.to_bytes(1, byteorder='big', signed=False)

        # Caso especial do tipo R: instrução JR
        elif instruction.name == "JR":
            if bin_or_txt == 2:
                rd = bitfield_list[i]  # nome do registrador
                register_d = register_set_dict[rd.lower()]  # objeto registrador
                instR_dict['rd'] = int_to_binarystring(register_d.num, 5)

                instR_dict['rs'] = '00000'
                instR_dict['rt'] = '00000'
                instR_dict['shamt'] = '00000'

                instR_dict['funct'] = int_to_binarystring(instruction.funct, 6)

            else:
                rd = bitfield_list[i]  # nome do registrador
                register_d = register_set_dict[rd.lower()]  # objeto registrador
                instR_dict['rd'] = register_d.num.to_bytes(1, byteorder="big", signed=False)

                zero = 0
                instR_dict['rs'] = zero.to_bytes(1, byteorder="big", signed=False)
                instR_dict['rt'] = zero.to_bytes(1, byteorder="big", signed=False)
                instR_dict['shamt'] = zero.to_bytes(1, byteorder="big", signed=False)
                instR_dict['funct'] = instruction.funct.to_bytes(1, byteorder="big", signed=False)

        # Se não for um caso especial
        else:
            if bin_or_txt == 2:
                rd = bitfield_list[i]
                register_d = register_set_dict[rd.lower()]
                # print('Registrador = ' + register_d.name)
                instR_dict['rd'] = int_to_binarystring(register_d.num, 5)
                # print('Num do registrador em binário:', instR_dict['rd'])

                rs = bitfield_list[i + 1]
                register_s = register_set_dict[rs.lower()]
                # print('Registrador = ' + register_s.name)
                instR_dict['rs'] = int_to_binarystring(register_s.num, 5)
                # print('Num do registrador em binário:', instR_dict['rs'])

                rt = bitfield_list[i + 2]
                register_t = register_set_dict[rt.lower()]
                # print('Registrador = ' + register_t.name)
                instR_dict['rt'] = int_to_binarystring(register_t.num, 5)
                # print('Num do registrador em binário:', instR_dict['rt'])

                instR_dict['shamt'] = '00000'

                instR_dict['funct'] = int_to_binarystring(instruction.funct, 6)

            else:
                rd = bitfield_list[i]
                register_d = register_set_dict[rd.lower()]
                instR_dict['rd'] = register_d.num.to_bytes(1, byteorder="big", signed=False)

                rs = bitfield_list[i + 1]
                register_s = register_set_dict[rs.lower()]
                instR_dict['rs'] = register_s.num.to_bytes(1, byteorder="big", signed=False)

                rt = bitfield_list[i + 2]
                register_t = register_set_dict[rt.lower()]
                instR_dict['rt'] = register_t.num.to_bytes(1, byteorder="big", signed=False)

                zero = 0
                instR_dict['shamt'] = zero.to_bytes(1, byteorder="big", signed=False)

                instR_dict['funct'] = instruction.funct.to_bytes(1, byteorder="big", signed=False)

        # Salvar no arquivo do tipo correspondente
        if bin_or_txt == 2:
            # Gerando comando em binário do tipo R final seguindo a ordem: opcode - rs - rt - rd - shamt - funct
            command_bin = command_bin + ' ' + instR_dict['rs'] + ' ' + instR_dict['rt'] + ' ' + instR_dict['rd'] + ' ' + instR_dict['shamt'] + ' ' + instR_dict['funct']
            saida_file.write(command_bin+'\n')
        else:
            saida_file.write(command_bin)
            saida_file.write(instR_dict['rs'])
            saida_file.write(instR_dict['rt'])
            saida_file.write(instR_dict['rd'])
            saida_file.write(instR_dict['shamt'])
            saida_file.write(instR_dict['funct'])

    # formatar command_bin para tipo I
    elif instruction.type == 'I':
        instI_dict = dict({
            'rs': None,
            'rt': None,
            'offset': None
        })

        # Caso especial do tipo I: instruções BEQ e BNE
        if instruction.name == 'BEQ' or instruction.name == 'BNE':
            if bin_or_txt == 2:
                rs = bitfield_list[i]
                register_s = register_set_dict[rs.lower()]
                # print('Registrador = ' + register_s.name)
                instI_dict['rs'] = int_to_binarystring(register_s.num, 5)
                # print('Num do registrador em binário:', instI_dict['rs'])

                rt = bitfield_list[i + 1]
                register_t = register_set_dict[rt.lower()]
                # print('Registrador = ' + register_t.name)
                instI_dict['rt'] = int_to_binarystring(register_t.num, 5)
                # print('Num do registrador em binário:', instI_dict['rt'])

                flag = bitfield_list[i + 2]
                offset = flags_in_file[flag]
                instI_dict['offset'] = int_to_binarystring(offset, 16)

            else:
                rs = bitfield_list[i]
                register_s = register_set_dict[rs.lower()]
                instI_dict['rs'] = register_s.num.to_bytes(1, byteorder='big', signed=False)

                rt = bitfield_list[i + 1]
                register_t = register_set_dict[rt.lower()]
                instI_dict['rt'] = register_t.num.to_bytes(1, byteorder='big', signed=False)

                flag = bitfield_list[i + 2]
                offset = flags_in_file[flag]
                instI_dict['offset'] = offset.to_bytes(2, byteorder='big', signed=True)

        elif instruction.name == 'LW' or instruction.name == 'SW':
            if bin_or_txt == 2:
                rt = bitfield_list[i]
                register_t = register_set_dict[rt.lower()]
                # print('Registrador = ' + register_t.name)
                instI_dict['rt'] = int_to_binarystring(register_t.num, 5)
                # print ('Num do registrador em binário:', instI_dict['rt'])

                offset = int(bitfield_list[i + 1])
                instI_dict['offset'] = int_to_binarystring(offset, 16)

                rs = bitfield_list[i + 2]
                register_s = register_set_dict[rs.lower()]
                # print('Registrador = ' + register_s.name)
                instI_dict['rs'] = int_to_binarystring(register_s.num, 5)
                # ('Num do registrador em binário:', instI_dict['rs'])
            else:
                rt = bitfield_list[i]
                register_t = register_set_dict[rt.lower()]
                instI_dict['rt'] = register_t.num.to_bytes(1, byteorder='big', signed=False)

                offset = int(bitfield_list[i + 1])
                instI_dict['offset'] = offset.to_bytes(2, byteorder='big', signed=True)

                rs = bitfield_list[i + 2]
                register_s = register_set_dict[rs.lower()]
                instI_dict['rs'] = register_s.num.to_bytes(1, byteorder='big', signed=False)

        else:
            if bin_or_txt == 2:
                rs = bitfield_list[i]
                register_s = register_set_dict[rs.lower()]
                # print('Registrador = ' + register_s.name)
                instI_dict['rs'] = int_to_binarystring(register_s.num, 5)
                # print('Num do registrador em binário:', instI_dict['rs'])

                rt = bitfield_list[i + 1]
                register_t = register_set_dict[rt.lower()]
                # print('Registrador = ' + register_t.name)
                instI_dict['rt'] = int_to_binarystring(register_t.num, 5)
                # print('Num do registrador em binário:', instI_dict['rt'])

                offset = int(bitfield_list[i + 2])
                instI_dict['offset'] = int_to_binarystring(offset, 16)

            else:
                rs = bitfield_list[i]
                register_s = register_set_dict[rs.lower()]
                instI_dict['rs'] = register_s.num.to_bytes(1, byteorder='big', signed=False)

                rt = bitfield_list[i + 1]
                register_t = register_set_dict[rt.lower()]
                instI_dict['rt'] = register_t.num.to_bytes(1, byteorder='big', signed=False)

                offset = int(bitfield_list[i + 2])
                instI_dict['offset'] = offset.to_bytes(2, byteorder='big', signed=True)

        # Salvar no arquivo do tipo correspondente
        if bin_or_txt == 2:
            # Gerando comando em binário do tipo I final seguindo a ordem: opcode - rs - rt - offset
            command_bin = command_bin + ' ' + instI_dict['rs'] + ' ' + instI_dict['rt'] + ' ' + instI_dict['offset']
            saida_file.write(command_bin+'\n')
        else:
            saida_file.write(command_bin)
            saida_file.write(instI_dict['rs'])
            saida_file.write(instI_dict['rt'])
            saida_file.write(instI_dict['offset'])

    # formatar command_bin para tipo J
    else:
        instJ_dict = dict({
            'address': None
        })

        # Salvar no arquivo do tipo correspondente
        if bin_or_txt == 2:
            flag = bitfield_list[i]
            address = flags_in_file[flag]
            instJ_dict['address'] = int_to_binarystring(address, 26)

            # Gerando comando em binário do tipo J final seguindo a ordem: opcode - address
            command_bin = command_bin + ' ' + instJ_dict['address']
            saida_file.write(command_bin+'\n')
        else:
            flag = bitfield_list[i]
            address = flags_in_file[flag]
            instJ_dict['address'] = address.to_bytes(4, byteorder='big', signed=True)

            saida_file.write(command_bin)
            saida_file.write(instJ_dict['address'])

    # print('comando binário final =', command_bin)

saida_file.close()
asm_file.close()

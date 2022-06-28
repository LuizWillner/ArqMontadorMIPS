# ======================= IMPORTS ==============================

from InstructionPY import *


# ========================= MAIN ========================

all_instructions = []

# Pegar input do usuário para:
# a) Nome da instrução (máximo de 4 chars)
# b) Tipo da instrução (R, I, J)
# c) Opcode que codificará a instrução em binário
# d) Campo funct, caso seja utilizado numa instrução do tipo R

inst_name = input('Digite o nome da instrução (digite "fim" para encerrar entrada): ')
if len(inst_name) > NAME_SIZE or len(inst_name) == 0:
    print("Nome da instrução é muito longo ou nulo! Finalizando programa...")
    exit(1)

while inst_name.upper() != 'FIM':

    inst_type = input('Digite seu tipo: ')
    if inst_type.upper() != 'R' and inst_type.upper() != 'I' and inst_type.upper() != 'J':
        print('Tipo da instrução é inválido (diferente de R, I e J)! Finalizando programa...')
        exit(1)
    inst_opcode = int(input('Digite seu opcode: '))
    inst_funct = input('Digite o funct (digite "none" se não houver): ')

    # Se NONE foi dado como entrada para funct, não passar ele como parâmetro ao criar objeto Instrução
    if inst_funct.upper() == 'NONE':
        instruction = Instruction(inst_name.upper(), inst_type.upper(), inst_opcode)

    # Senão, transformar o valor em inteiro e passar como parâmtro para construtor de Instrução
    else:
        inst_funct = int(inst_funct)
        instruction = Instruction(inst_name.upper(), inst_type.upper(), inst_opcode, inst_funct)

    all_instructions.append(instruction)

    inst_name = input('Digite o nome da instrução (digite "fim" para encerrar entrada): ')

# Ordenar lista criada com todas as instruções de acordo com o valor da chave de cada Instrução
all_instructions.sort(key=sort_by_instruction_key)

# Escrever conteúdo da lista num arquivo binário
file = open(ALL_INSTS_FILE_NAME, 'wb')
for instruction in all_instructions:
    instruction.save_in_file(file)
file.close()

# Printar conteúdo do arquivo binário gerado
print()
print_instruction_file(ALL_INSTS_FILE_NAME)

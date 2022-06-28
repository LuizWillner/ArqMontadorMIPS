import pickle
import sys


class Instruction:
    def __init__(self, name, type, opcode, funct=None):
        self.name = name
        self.type = type
        self.opcode = opcode
        self.funct = funct

try:
    arq = open("teste.bin", 'wb')
except:
    print('Erro ao abrir arquivo')

add_inst = Instruction('ADD', 'R', 0, 32)
addi_inst = Instruction('ADDI', 'I', 8)
and_inst = Instruction('AND', 'R', 0, 36)



# num = 8
# outro_num = 3
# char = 'R\0'
# string = 'ADD\0'
# ultimo_num = 19
#
# SIZE_OF_REG = sys.getsizeof(num)
# print('SIZE_OF_REG =', SIZE_OF_REG)
# print()
#
# pickle.dump(num, arq)
# pickle.dump(outro_num, arq)
# pickle.dump(char, arq)
# pickle.dump(string, arq)
# pickle.dump(ultimo_num, arq)
#
# arq.close()
#
#
# try:
#     arq = open("teste.bin", 'rb')
# except:
#     print('Erro ao abrir arquivo')
#
#
# all_content = arq.read()
# print('all_content =', all_content)
# print()
# arq.seek(0)
#
# # num_bin = arq.read(SIZE_OF_REG)
# # print('num_bin =', num_bin)
# # bin_to_dec = pickle.loads(num_bin)
# # print('bin_to_dec =', bin_to_dec)
# # print()
# # arq.seek(0)
#
# num2 = pickle.load(arq)
# outro_num2 = pickle.load(arq)
# char2 = pickle.load(arq)
# string2 = pickle.load(arq)
# ultimo_num2 = pickle.load(arq)
#
# print('num2 =', num2)
# print('outro_num2 =', outro_num2)
# print('char2 =', char2)
# print('string2 =', string2)
# print('ultimo_num2 =', ultimo_num2)
# print()
#
# i = 5 + 5 + 17 + 19
# arq.seek(i)
# print(f'Conteudo [{i}] =', pickle.load(arq))

arq.close()

# TAMANHO DE DIFERENTES TIPOS EM ARQS BINÁRIOS USANDO PICKLE
#  int = 5 bytes
#  string[tam = x chars] = 15 + x bytes
#  string[tam = 4] = 15 + 4 = 19 bytes

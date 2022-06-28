# ======================= IMPORTS ==============================
from RegisterPY import *


# ========================= MAIN ========================

quant_registers = int(input('Digite a quantidade de registradores do processador: '))
all_registers = []

for reg_id in range(quant_registers):
    print(f'Insira o nome do registrador {reg_id} (sem o $): ', end='')
    reg_name = input()
    reg_name = '$' + reg_name.lower()
    register = Register(reg_id, reg_name)
    all_registers.append(register)

file = open(ALL_REGS_FILE_NAME, "wb")
for register in all_registers:
    register.save_in_file(file)
file.close()

print()
print_register_file(ALL_REGS_FILE_NAME)

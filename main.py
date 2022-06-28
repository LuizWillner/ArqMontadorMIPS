# =========================== IMPORTS ============================

from InstructionPY import *


# ======================== CONSTANTS =============================

ASM_FILE_NAME = 'exemplo.asm'

# ======================== FUNCTIONS =============================


# ========================== MAIN ================================

instruction_set_dict = generate_instruction_dict(FILE_NAME)

asm_file = open(ASM_FILE_NAME, "r")
asm_file.close()

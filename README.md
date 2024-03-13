# ArqMontadorMIPS
Trabalho da disciplina de Arquitetura de Computadores | Universidade Federal Fluminense | 2022.1

## Objetivo
Elaborar um programa que simule o processo de tradução de um arquivo assembly (MIPS) para código binário.

###
### Como utilizar o codificador
1) Rode o _main.py_ para codificar em binário um arquivo .asm
2) Insira o nome do arquivo Assembly a ser codificado SEM A EXTENSÃO
3) Escolha se deseja gerar como saída um arquivo binário ou um txt para visualizar o código em binário. 
O nome desse arquivo será _saida.bin_ ou _saida.txt_

###
### Descrição dos scripts auxiliares

#### InstructionSetGenerator.py
O _InstructionSetGenerator.py_ gera um arquivo binário de nome padrão _instruction_set.bin_ com diversas instruções e suas
informações (nome, tipo, opcode e funct) a partir de um input do usuário. O input utilizado
como base foi gerado baseado na tabela fornecida pela descrição do problema
que especificada quais instruções deveriam ser codificadas

#### InstructionPY.py
Trata-se de um arquivo que contém a classe Instrução, seus atributos, métodos e algumas
funções auxiliares

#### RegisterSetGenerator.py
O _RegisterSetGenerator.py_ gera um arquvo binário de nome padrão _register_set.bin_ com o conjunto de registradores disponíveis
fornecido pelo input do usuário, incluindo informações como seus nomes e números. O input utilizado
como base foi gerado baseado na tabela fornecida pela descrição do problema
que especificada quais instruções deveriam ser codificadas

#### Register.py
Arquivo que contém a classe Registrador, seus atributos, métodos e algumas funções auxiliares

###
### Descrição de outros arquivos

#### exemplo.asm
Consiste no programa assembly fornecido como exemplo pelo exercício

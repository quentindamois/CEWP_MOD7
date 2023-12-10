from Memory import *
from Codeparser import *
import re


def line_distinction(file_content):
    res = []
    for i in range(len(file_content)):
        res.append(file_content[0 + i * 32 : 32 + i * 32])
    return res[:]


def bin_part(file_content):
    parsed_line = []
    file_content = file_content.split("\n")
    if (len(file_content) < 2):
        file_content = line_distinction(file_content)[:]
    return file_content[:]



def reg_init():
    for i in range(0,4):
        register("t" + str(i), '{0:02b}'.format(i))


def init_inst():
    #this function is used to initialised all of the instruction
    LDA()
    STR()
    PUSH()
    POP()
    AND()
    OR()
    NOT()
    ADD()
    SUB()
    DIV()
    MUL()
    MOD()
    INC()
    DEC()
    BEQ()
    BNE()
    BBG()
    BSM()
    JMP()
    HLT()



def instruction_parsing(content_ling): #unused
    res = []
    set_instruction = set(instruction.intruction_dict.keys())
    for l in range(len(content_ling)):
        if(content_ling[l][:5] in set_instruction):
            res.append(instruction.intruction_dict[content_ling[l][:5]].bin_parser(content_ling[l])[:])
        else:
            res.append([content_ling[l][:5], content_ling[l][5:7], content_ling[l][7:]])
    return res [:]






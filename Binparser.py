from Memory import *
import re

def get_code():
    file = open("demofile.txt","r") #we open the file to read it
    res = file.read()
    file.close()
    return res[:]

def line_distinction(file_content):
    res = []
    for i in range(len(file_content)):
        res.append(file_content[0 + i * 32 : 32 + i * 32])
    return res[:]


def bin_part(file_content):
    parsed_line = []
    file_content = file_content.spli("\n")
    if (len(file_content) < 2):
        file_content = line_distinction(file_content)[:]
    for l in file_content:
        parsed_line.append(l[:5])
        i = 5
        while(i < len(l[5:])):
            parsed_line[-1].append(l[i: i + 2])
            if (l[i: i + 2] == "10"):
                parsed_line[-1].append(l[i + 2 : i + 4])
                i = i + 4
            else:
                parsed_line[-1].append(l[i + 2 : i + 9])
                i = i + 9
    return parsed_line

def label_creator(parsed_line):
    dict_label = []
    i = 0
    while i < len(parsed_line):
        set_op_code = set(instruction.intruction_dict.keys())
        if(not(set_op_code.__contains__(parsed_line[i][0]))):
            dict_label[parsed_line[i][1] + parsed_line[i][2]] = parsed_line[i][3] + parsed_line[i][4]
            parsed_line.remove(parsed_line[i])


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


def main(): #TODO complete the bin conversion
    essaie = runner()
    label = {}
    reg_init()
    init_inst()
    parsed_line = [["00111","10","00","11","000000000000000000001"],["00111","10","00","11","000000000000000000010"], ["10011","00","0000000","00","0000000000000000"]]
    runner.execute(essaie, parsed_line, label)

main()
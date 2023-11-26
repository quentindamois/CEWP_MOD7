from Memory import *
import re

def get_code():#TODO: create the fonction that get the file in the first place
    print("not completed yet")

def part_separation(file_content):
    #the purpose of this function is to seperate the part were we initialise the variable and the parte were we have code
    separated_category = file_content.split("#")[1:] #Supposed to be cleaner
    res = []
    for i in range(0, len(separated_category)):
        res.append(separated_category[i][1:])
    return res

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




def empty(content):
    res = []
    for p in range(0,len(content)):
        temp_part = []
        for l in range(0, content[p]):
            if(len(re.findall("\s", content[p][l])) != len(content[p][l])):
                temp_part.append(content[p][l][:])
        res.append(temp_part[:])
    return res


def next_label(list_lign):
    #to find the next line that is not a label
    set_instru = set(instruction.intruction_dict.keys())
    if (set_instru.__contains__(list_lign[0])):
        return 1
    return next_label(list_lign[1:]) + 1

def tag_finder(instruction_label, label_ref):
    lign_instruction = []
    index_mem = len(memory.name_binary)
    #we condiser a labe the first caracter of every as long as it is not the name of instruction
    set_instru = set(instruction.intruction_dict.keys())
    #we have two cases : it is a label, it is an instruction
    for i in range(0, len(instruction_label)):
        if (set_instru.__contains__(instruction_label[i][0])): #we make the distinction between the line about the code and the one about the instruction, in order to do so we look to see if the instruction given is referenced in the dictionnary
            lign_instruction.append(instruction_label[i][:]) #we had the [:] at the end because we need to make a deep copy
        else: #if it is not we will look create a new label
            label(instruction_label[0], '{0:07b}'.__format__(index_mem), next_label(instruction_label[i:])) #we initialise the new label
            label_ref['{0:07b}'.__format__(index_mem)] = next_label(instruction_label[i:]) #wa add the bin name as the key and the line corresponding as a value
    return lign_instruction[:] #we return the list of line with only execution

def reg_init():
    for i in range(0,4):
        register("t" + str(i), '{0:07b}'.__format__(bin(i)))

def code_to_bin(file_content): #TODO: change the name of the fonction
    label_dict = {}
    instruction_convertion = {"LDA":"00000", "STR":"00001", "PUSH":"00010", "POP":"00011", "AND":"00100", "OR":"00101", "NOT":"00110", "ADD":"00111", "SUB":"01000", "DIV":"01001", "MUL":"01010", "MOD":"01011", "INC":"01100", "DEC":"01101", "BEQ":"01110", "BNE":"01111", "BBG":"10000", "BSM":"10001", "JMP":"10010", "HLT":"10011"}
    effective_line = {}
    reg_init()
    #we need to differciented the data and the code
    hierchised_line = part_separation(file_content)
    for p in range(0, len(hierchised_line)):
        hierchised_line[p] = hierchised_line[p].split("\n")[1:]
    clean_line = empty(hierchised_line)
    #once we have the different kind
    #we are assigning a binary code for each
    num_var = 4
    for l in clean_line[0]:
        temp_l = l.split(" ")
        #we create a variable by giving it a name wichi is a number in bit and giving it a value which is made by the user
        variable(temp_l[1], '{0:07b}'.__format__(num_var), temp_l[0])
        num_var += 1
    #we have to seperate the line with the tag and the line without

    init_inst() #initialisation of the instrucition
    #Now we parse the code part
    line_code = tag_finder(clean_line[1], label_dict)[:]
    set_instru = set(instruction_convertion.keys())
    for l in line_code:
        if(set_instru.__contains__(l[0])):
            line_code.append([instruction.intruction_dict[l[0]]])
            for p in range(1, len(l)):
                if (len(re.findall("\d",l[p][0])) != len(l[p])): #if the is one character that mean it is a variable
                    line_code[-1].append(memory.memory_address[memory.name_binary[l[p]]].to_binary())
                else: # if there is only number that me it is a constant
                    line_code[-1].append("11" + '{0:07b}'.__format__(bin(int(l[p]))))
            #we create a list of list
            #each element of the first list is a line with the binary number seperated for execution
    #now we need to pass the information we parsed to the runner class
    runner.execute(line_code, label_dict)
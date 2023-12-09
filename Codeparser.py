from Memory import *
import re

def get_code():
    file = open("essaiefile.txt.txt","r") #we open the file to read it
    res = file.read()
    file.close()
    return res

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
        for l in range(0, len(content[p])):
            if(len(re.findall("\s", content[p][l])) != len(content[p][l])):
                temp_part.append(content[p][l][:])
        res.append(temp_part[:])
    return res


def next_label(list_lign): #unused
    #to find the next line that is not a label
    set_instru = set(instruction.intruction_dict.keys())
    print(f"the size of the list {len(list_lign)}")
    if (len(list_lign) <= 0 or set_instru.__contains__(list_lign[0])):
        return 1
    return next_label(list_lign[1:]) + 1

def tag_finder(instruction_label, label_ref): #unused
    lign_instruction = []
    index_mem = len(memory.name_binary)
    #we condiser a labe the first caracter of every as long as it is not the name of instruction
    set_instru = set(instruction.intruction_dict.keys())
    #we have two cases : it is a label, it is an instruction
    for i in range(0, len(instruction_label)):
        if (set_instru.__contains__(instruction_label[i][0])): #we make the distinction between the line about the code and the one about the instruction, in order to do so we look to see if the instruction given is referenced in the dictionnary
            lign_instruction.append(instruction_label[i][:]) #we had the [:] at the end because we need to make a deep copy
        else: #if it is not we will look create a new label
            label(instruction_label[0], '{0:07b}'.format(index_mem), next_label(instruction_label[i:])) #we initialise the new label
            label_ref['{0:07b}'.format(index_mem)] = next_label(instruction_label[i:]) #wa add the bin name as the key and the line corresponding as a value
    return lign_instruction[:] #we return the list of line with only execution

def find_label(label_asked, code_content):
    i = 0
    while(not(label_asked in code_content[i])):
        i += 1
    return i

def tag_parser(code_content):
    line_label = re.findall(".+:", "\n".join(code_content))[:]
    for i in range(0,len(line_label)):
        tag_name = re.sub("\s", "", line_label[i])
        tag_name = tag_name.split(":")[0]
        label(find_label(line_label[i], code_content), tag_name, '{0:07b}'.format(i))

def reg_init():
    for i in range(0,4):
        register("t" + str(i), '{0:07b}'.format(i))

def code_parser(code_part): #complete the fonnction so that it result in a string similar to the one previusly found in the pseudo_binary file
    bin_file_content = ""

    instruction_convertion = {"LDA": "00000", "STR": "00001", "PUSH": "00010", "POP": "00011", "AND": "00100","OR": "00101", "NOT": "00110", "ADD": "00111", "SUB": "01000", "DIV": "01001","MUL": "01010", "MOD": "01011", "INC": "01100", "DEC": "01101", "BEQ": "01110","BNE": "01111", "BBG": "10000", "BSM": "10001", "JMP": "10010", "HLT": "10011"}
    for i in range(0, len(code_part)):
        line_i = re.split("\s+", code_part[i])[:]
        line_i = line_i[:] if line_i[0] != '' else line_i[1:]
        if (line_i[0] in instruction_convertion.keys()):

            bin_file_content += instruction.intruction_dict[instruction_convertion[line_i[0]]].bin_writer(line_i) #this is tha line that convertert a line whith an instruction to a a binary line
        elif (re.findall(".+:", code_part[i])):
            tag_designed = re.sub("\s", "", code_part[i])
            bin_file_content += ("11111" + memory.memory_address[memory.binary_name[tag_designed.split(":")[0]]].to_binary(25) + "\n") #this is the line where we parse the line with tag
            memory.memory_address[memory.binary_name[tag_designed.split(":")[0]]].value = i #actualise the value to make sure that the label doesn't point to a line
        #if it is not identifired as line for instruction or a line were a tag is located
    return bin_file_content[:-1]

def comment_remover(code):
    for i in range(0, 2):
        for j in range(0, len(code[i])):
            code[i][j] = code[i][j].split("!")[0][:]
    return code[:]



def init_and_code_to_bin():
    reg_init()
    #we need to differciented the data and the code
    seperated_line = re.split("#DATA|#CODE", get_code())[1:]
    for p in range(0, len(seperated_line)):
        seperated_line[p] = seperated_line[p].split("\n")[:]
    clean_line = empty(seperated_line)
    clean_line = comment_remover(clean_line)
    clean_line = empty(clean_line)
    #once we have the different kind
    #we are assigning a binary code for each
    num_var = 0
    for l in clean_line[0]:
        temp_l = l.split(" ")
        #we create a variable by giving it a name wichi is a number in bit and giving it a value which is made by the user
        variable(temp_l[1], temp_l[0], '{0:07b}'.format(num_var))
        num_var += 1
    #we have to seperate the line with the tag and the line without

    init_inst() #initialisation of the instrucition
    #Now we parse the code part
    #line_code = tag_finder(clean_line[1], label_dict)[:]
    tag_parser(clean_line[1][:])
    res = code_parser(clean_line[1][:])
    return res



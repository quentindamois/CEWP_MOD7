import random

#this is the objected oriented part of the programm were the programm is run once it is parsed
#this is justed a library and the relant object are used when necessary in the main file

def binstr_to_bin(number):
    res = 0
    for i in range(len(number)):
        if number[-(i + 1)] == '1':
           res += 2**i
    return res

def check_arg(type_arg, arg, op_code, number):
    if (op_code != "10011" and type_arg != "11"):
        if(number == 1 and(15  < binstr_to_bin(op_code) or 19 > binstr_to_bin(op_code))):
            return memory.memory_address[arg]
        return memory.memory_address.values
    elif (type_arg == "11"):
        return binstr_to_bin(arg)
    return 0

class memory:
    #this the class memory this class is an interface like class used for the parameter class as a mean to have a static method for the variable
    memory_address = {}
    total_size = 0
    name_binary = {}
    binary_name = {}

class stack:
    stack_content = []
    max_size = 4096
    current_size = 0

class parameter(memory):
    #this is class is used as parant class to create the commun part between the regeteri and the variable
    def __init__(self, value, name, var_code):
        super().__init__()
        self.value = value
        self.name = name #probaby change to being a binary code specific to a variable or a register
        self.address = memory.total_size #i don t really know what to do with it since it may not benecessary for the first part
        memory.memory_address[var_code] = self
        memory.total_size = memory.total_size + self.__sizeof__()
        memory.name_binary[var_code] = name
        memory.binary_name[name] = var_code
    def to_binary(self):
        #DONE: implement the function to every class
        print("not implemented")


class register(parameter):
    #this the register class, unlike the variable there initial value is set on zero
    def __init__(self, name, var_code):
        super().__init__(0, name, var_code)
    def to_binary(self):
        return "10" + memory.name_binary[self.name]


class variable(parameter):
    #pretty much a anoter name for parameter
    #it is used to differentiate the register object and the variable
    def __init__(self, value, name, var_code):
        super().__init__(value, name, var_code)
    def to_binary(self):
        return "01" + memory.name_binary[self.name]

class label(parameter):
    def __init__(self, value, name, var_code):
        super().__init__(value, name, var_code)

    def to_binary(self):
        return "00" + memory.name_binary[self.name]
class instruction:
    #this a parent class to the 20 instruction requiered for the completion of part 1
    intruction_dict = {} # this variable is a dictionari used to stored the on object of the different instruction and the OP code
    #the op code is used as key in the dictionnary
    def __init__(self, op_code):

        self.op_code = op_code
        instruction.intruction_dict[op_code] = self
    #this the base version of the function that is overidden by every subclass
    #DONE: change the parameter of the base version of execute_instruction in the parent class
    def execute_instruction(self, reg_dest, value_source, tag_dictionnary):
        print("No specified instruction inputed")
    def param_selection(self, parsed_list):
        print("No specified instruction")
    def bin_parser(self, lign):
        print("no instruction implemtented yet")




class runner:
    #the runner class is used to instancied an object tha will execute each line of code

    def execute(self,parsed): #the line_tag store the tag in the code
        #parsed is the binary seperated in chunck of relevant information
        #for example the first block is always the op code of the instruction
        #new take for the line navigatio
        #uncomplete is used as a condition for navigating
        index_ligne = 0 #index_lign is used to chose wich line need to be executed
        print("it work in the beginning")
        while 0 <= index_ligne: #DONE: change the condition because the instruction for the end is not always the last
            set_instruction = set(instruction.intruction_dict.keys())
            if (parsed[index_ligne][0] in set_instruction):
                temp_rec = instruction.intruction_dict[parsed[index_ligne][0]].param_selection(parsed[index_ligne][1:])
            else:
                temp_rec = 0
            index_ligne  = temp_rec if temp_rec != 0  else index_ligne + 1
        return 0

#in each instruction we use the parant initialisation with the op code specific to that instruction
#DONE: remove the conver to bin
#1
class LDA(instruction):
    def __init__(self):
        super().__init__("00000")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]

#2
class STR(instruction):
    def __init__(self):
        super().__init__("00001")
    def execute_instruction(self, var_dest, value_source, param_trash):
        var_dest.value = value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#3
class PUSH(instruction):
    def __init__(self):
        super().__init__("00010")
    def execute_instruction(self, value_source, param_trash_0, param_trash_1):
        if(stack.current_size + value_source.sizeof <= stack.current_size):
            stack.stack_content.append(value_source)
            stack.current_size += value_source.sizeof
            return 0
    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
#4
class POP(instruction):
    def __init__(self):
        super().__init__("00011")
    def execute_instruction(self, value_source, param_trash_0, param_trash_1):
        if(0 < stack.current_size):
            res = stack.stack_content.pop()
            stack.current_size -= res.sizeof
            value_source.value = res
            return 0
    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
#5
class AND(instruction):
    def __init__(self):
        super().__init__("00100")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value & value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#6
class OR(instruction):
    def __init__(self):
        super().__init__("00101")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value | value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#7
class NOT(instruction):
    def __init__(self):
        super().__init__("00110")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = ~reg_dest.value
        return 0
    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
#8
class ADD(instruction):
    def __init__(self):
        super().__init__("00111")
    def execute_instruction(self, reg_dest, value_source, param_trah):
        reg_dest.value = reg_dest.value + value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        print(res)
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#9
class SUB(instruction):
    def __init__(self):
        super().__init__("01000")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value - value_source
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#10
class DIV(instruction):
    def __init__(self):
        super().__init__("01001")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source // reg_dest.value
        return 0
    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#11
class MUL(instruction):
    def __init__(self):
        super().__init__("01010")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value * value_source
        return 0


    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value,
                                     0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]), 0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#12
class MOD(instruction):
    def __init__(self):
        super().__init__("01011")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source % reg_dest.value
        return 0

    def param_selection(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], memory.memory_address[parsed_list[3]].value,
                                     0)
        else:
            res = self.execute_instruction(memory.memory_address[parsed_list[1]], binstr_to_bin(parsed_list[3]), 0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
#13
class INC(instruction):
    def __init__(self):
        super().__init__("01100")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value += 1
        return 0
    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[2:4])
        res.append(lign[4:])
        return res[:]
#14
class DEC(instruction):
    def __init__(self):
        super().__init__("01101")
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value -= 1
        return 0

    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
#15
class BEQ(instruction):
    def __init__(self):
        super().__init__("01110")
    def execute_instruction(self, first_argument, second_argument, target_label):
        if (first_argument == second_argument):
            return target_label.value
        return 0
    def param_selection(self, parsed_list):
        first_param = memory.memory_address[parsed_list[1]].value if parsed_list[0] != "11" else binstr_to_bin(parsed_list[1])
        second_param = memory.memory_address[parsed_list[3]].value if parsed_list[2] != "11" else binstr_to_bin(parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[parsed_list[5]])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
#16
class BNE(instruction):
    def __init__(self):
        super().__init__("01111")
    def execute_instruction(self, first_argument, second_argument, target_label):
        if (first_argument != second_argument):
            return target_label.value
        return 0

    def param_selection(self, parsed_list):
        first_param = memory.memory_address[parsed_list[1]].value if parsed_list[0] != "11" else binstr_to_bin(
            parsed_list[1])
        second_param = memory.memory_address[parsed_list[3]].value if parsed_list[2] != "11" else binstr_to_bin(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[parsed_list[5]])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
#17
class BBG(instruction):
    def __init__(self):
        super().__init__("10000")
    def execute_instruction(self, first_agument, seconde_argumet, target_label):
        if (first_agument > seconde_argumet):
            return target_label.value
        return 0

    def param_selection(self, parsed_list):
        first_param = memory.memory_address[parsed_list[1]].value if parsed_list[0] != "11" else binstr_to_bin(
            parsed_list[1])
        second_param = memory.memory_address[parsed_list[3]].value if parsed_list[2] != "11" else binstr_to_bin(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[parsed_list[5]])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
#18
class BSM(instruction):
    def __init__(self):
        super().__init__("10001")
    def execute_instruction(self, first_argument, seconde_argument, target_label):
        if (first_argument < seconde_argument):
            return target_label.value
        return 0

    def param_selection(self, parsed_list):
        first_param = memory.memory_address[parsed_list[1]].value if parsed_list[0] != "11" else binstr_to_bin(
            parsed_list[1])
        second_param = memory.memory_address[parsed_list[3]].value if parsed_list[2] != "11" else binstr_to_bin(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[parsed_list[5]])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
#19
class JMP(instruction):
    def __init__(self):
        super().__init__("10010")
    def execute_instruction(self, target_label, param_trash_0, param_trash_1):
        return target_label.value
    def param_selection(self, parsed_list):
        return self.execute_instruction(memory.memory_address[parsed_list[1]], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
#20
class HLT(instruction):
    print("quit command")
    def __init__(self):
        super().__init__("10011")
    def execute_instruction(self, param_trash_0, param_trash_1, param_trash_2): #DONE: rewrite the function
        return -1
    def param_selection(self, parsed_list):
        return self.execute_instruction(0, 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        return res[:]
import random
import re


#this is the objected oriented part of the programm were the programm is run once it is parsed
#this is justed a library and the relant object are used when necessary in the main file


def binstr_to_bin_neg(number):
    res = 0
    for i in range(len(number) - 1):
        if number[-(i + 1)] == '1':
            res += 2 ** i
    if (number[0] == "1"):
        res *= -1
    return res
def binstr_to_bin(number):
    res = 0
    for i in range(len(number)):
        if number[-(i + 1)] == '1':
           res += 2**i
    return res

def rm_last_bit(binary):
    n = 0
    while(binary[n] != "1" and n + 1 < len(binary)):
        n += 1
    return binary[n:]

def memory_displayer():
    print("____________________________________")
    for i in memory.memory_address.values():
        print(f"{i.name} = {i.value}")
    print("____________________________________")

def memory_string():
    res = "____________________________________\n"
    for i in memory.memory_address.values():
         res += f"{i.name} = {i.value}\n"
    res += "____________________________________\n"
    return res

def check_arg(type_arg, arg, op_code, number): #this function is probably useless
    if (op_code != "10011" and type_arg != "11"):
        if(number == 1 and(15  < binstr_to_bin(op_code) or 19 > binstr_to_bin(op_code))):
            return memory.memory_address[arg]
        return memory.memory_address.values
    elif (type_arg == "11"):
        return binstr_to_bin_neg(arg)
    return 0

def reset_stack_and_memory():
    memory.memory_address = {}
    memory.total_size = 0
    memory.name_binary = {}
    memory.binary_name = {}
    stack.stack_content = []
    stack.max_size = 0
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
    def __init__(self, value, name, var_code, type):
        super().__init__()
        self.type = type
        self.value = int(value)
        self.var_code = var_code
        self.name = name
        memory.memory_address[ (type, rm_last_bit(var_code))] = self
        memory.total_size = memory.total_size + self.__sizeof__()
        memory.binary_name[name] = (self.type, rm_last_bit(var_code))
    def to_binary(self, n):
        #to reference a parameter in binary we first add its type then the var_code with a varying amount of bit
        template_format = '{0:0'+ str(n) + 'b}'
        return self.type + template_format.format(binstr_to_bin(self.var_code))


class register(parameter):
    #this the register class, unlike the variable there initial value is set on zero
    def __init__(self, name, var_code):
        super().__init__(0, name, var_code, "10")


class variable(parameter):
    #pretty much a anoter name for parameter
    #it is used to differentiate the register object and the variable
    def __init__(self, value, name, var_code):
        super().__init__(value, name, var_code, "01")

class label(parameter):
    def __init__(self, value, name, var_code):
        super().__init__(value, name, var_code, "00")
class instruction:
    #this a parent class to the 20 instruction requiered for the completion of part 1
    intruction_dict = {} # this variable is a dictionari used to stored the on object of the different instruction and the OP code
    #the op code is used as key in the dictionnary
    def __init__(self, op_code, name, allowed):
        self.op_code = op_code
        self.name = name
        self.allowed = allowed[:]
        instruction.intruction_dict[op_code] = self
    #this the base version of the function that is overidden by every subclass
    #DONE: change the parameter of the base version of execute_instruction in the parent class
    def execute_instruction(self, reg_dest, value_source, tag_dictionnary):
        print("No specified instruction inputed")
    def param_selection(self, parsed_list):
        print("No specified instruction")
    def bin_parser(self, lign):
        print("no instruction implemtented yet")
    def line_displayer(self, arg_list):
        res = f"{self.name}"
        for i in arg_list:
            res += f" {i}"
        return res
    def bin_writer(self, lines, param_len):
        res = self.op_code
        template_format = 0
        print(lines)
        for i in range(0, len(param_len)):
            if(len(re.findall("\d|-",lines[i + 1])) == len(lines[ 1 + i])):
                template_format = '{0:0' + str(param_len[i]) + 'b}'
                if(re.search("-", lines[i + 1])):
                    temp = template_format.format(int(lines[i + 1][1:]))
                    if (len(temp) > param_len[i]):
                        temp = temp[-param_len:]
                    temp = "1" + temp[1:]
                    res += "11" + temp
                else:
                    temp = template_format.format(int(lines[i + 1]))
                    if (len(temp) > param_len[i]):
                        temp = temp[-param_len:]
                    temp = "0" + temp[1:]
                    res += "11" + temp
            else:
                print("aaaaaaaa")
                print(memory.memory_address)
                print(memory.binary_name)
                temp = memory.memory_address[memory.binary_name[lines[i + 1]]].to_binary(param_len[i])
                if (len(temp) - 2 > param_len[i]):
                    temp = temp[:2] + temp[-param_len[1]:]
                res += temp
        res += "\n"
        return res
    def param_type_check(self, lines):
        #the lines doesn't contain the op code for the instruction
        for i in range(0, len(self.allowed)):
            if (not(lines[2 * i] in self.allowed[i])):
                raise SyntaxError(self.line_displayer(lines) + f": Wrong type for the argument {i + 1}.")





#in each instruction we use the parant initialisation with the op code specific to that instruction
#DONE: remove the conver to bin
#1
class LDA(instruction):
    def __init__(self):
        super().__init__("00000", "LDA", [["10"],["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].value, 0)
            #self.line_displayer("LDA", [memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name,
            #                               memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
            #self.line_displayer("LDA", [memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin(parsed_list[3]))])
        return res
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 16])
#2
class STR(instruction):
    def __init__(self):
        super().__init__("00001", "STR", [["01"], ["10", "11"]])
    def execute_instruction(self, var_dest, value_source, param_trash):
        var_dest.value = value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
            #self.line_displayer("STR", [memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].name])
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
            #self.line_displayer("STR", [memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name,
            #                            str(binstr_to_bin(parsed_list[3]))])
        return res


    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:])
        return res[:]
    def bin_writer(self, lines):
        return super().bin_writer(lines, [7, 16])

    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
#3
class PUSH(instruction):
    def __init__(self):
        super().__init__("00010", "PUSH", [["10","01","11"]])
    def execute_instruction(self, value_source, param_trash_0, param_trash_1):
        if(stack.current_size + value_source.__sizeof__() <= stack.max_size):
            stack.stack_content.append(value_source)
            stack.current_size += value_source.__sizeof__()
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        #self.line_displayer("PUSH")
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].value, 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#4
class POP(instruction):
    def __init__(self):
        super().__init__("00011", "POP", [["10"]])
    def execute_instruction(self, value_source, param_trash_0, param_trash_1):
        if(0 < stack.current_size):
            res = stack.stack_content.pop()
            stack.current_size -= res.__sizeof__()
            value_source.value = res
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#5
class AND(instruction):
    def __init__(self):
        super().__init__("00100", "AND", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value & value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
#6
class OR(instruction):
    def __init__(self):
        super().__init__("00101", "OR", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value | value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#7
class NOT(instruction):
    def __init__(self):
        super().__init__("00110", "NOT", [["10"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = ~reg_dest.value
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#8
class ADD(instruction):
    def __init__(self):
        super().__init__("00111", "ADD", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trah):
        reg_dest.value = reg_dest.value + value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#9
class SUB(instruction):
    def __init__(self):
        super().__init__("01000", "SUB", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value - value_source
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#10
class DIV(instruction):
    def __init__(self):
        super().__init__("01001", "DIV", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source // reg_dest.value
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value, 0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]),0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#11
class MUL(instruction):
    def __init__(self):
        super().__init__("01010", "MUL", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = reg_dest.value * value_source
        return -2


    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value,
                                     0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]), 0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#12
class MOD(instruction):
    def __init__(self):
        super().__init__("01011", "MOD", [["10"], ["10", "01", "11"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value = value_source % reg_dest.value
        return -2

    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        if (parsed_list[2] != "11"):
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value,
                                     0)
        else:
            res = self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], binstr_to_bin_neg(parsed_list[3]), 0)
        return res

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:9])
        res.append(lign[9:11])
        res.append(lign[11:])
        return res[:]
    def line_displayer(self, parsed_list):
        if (parsed_list[2] != "11"):
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, memory.memory_address[parsed_list[2], rm_last_bit(parsed_list[3])].name])
        else:
            res = super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name, str(binstr_to_bin_neg(parsed_list[3]))])
        return res
    def bin_writer(self, lines):
        return super().bin_writer(lines, [2, 26])
#13
class INC(instruction):
    def __init__(self):
        super().__init__("01100", "INC", [["10"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value += 1
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#14
class DEC(instruction):
    def __init__(self):
        super().__init__("01101", "DEC", [["10"]])
    def execute_instruction(self, reg_dest, value_source, param_trash):
        reg_dest.value -= 1
        return -2

    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#15
class BEQ(instruction):
    def __init__(self):
        super().__init__("01110", "BEQ", [["10", "01", "11"], ["10", "01", "11"], ["00"]])
    def execute_instruction(self, first_argument, second_argument, target_label):
        if (first_argument == second_argument):
            return target_label.value
        return -2
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].value if parsed_list[0] != "11" else binstr_to_bin_neg(parsed_list[1])
        second_param = memory.memory_address[ (parsed_list[2], rm_last_bit(parsed_list[3]))].value if parsed_list[2] != "11" else binstr_to_bin_neg(parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
    def line_displayer(self, parsed_list):
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name if parsed_list[0] != "11" else str(binstr_to_bin_neg(parsed_list[1]))
        second_param = memory.memory_address[ (parsed_list[2], rm_last_bit(parsed_list[3]))].name if parsed_list[2] != "11" else str(binstr_to_bin_neg(parsed_list[3]))
        return super().line_displayer([first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [7,7,7])
#16
class BNE(instruction):
    def __init__(self):
        super().__init__("01111", "BNE", [["10", "01", "11"], ["10", "01", "11"], ["00"]])
    def execute_instruction(self, first_argument, second_argument, target_label):
        if (first_argument != second_argument):
            return target_label.value
        return -2

    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].value if parsed_list[0] != "11" else binstr_to_bin_neg(
            parsed_list[1])
        second_param = memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value if parsed_list[2] != "11" else binstr_to_bin_neg(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
    def line_displayer(self, parsed_list):
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name if parsed_list[0] != "11" else str(binstr_to_bin_neg(parsed_list[1]))
        second_param = memory.memory_address[ (parsed_list[2], rm_last_bit(parsed_list[3]))].name if parsed_list[2] != "11" else str(binstr_to_bin_neg(parsed_list[3]))
        return super().line_displayer([first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [7,7,7])
#17
class BBG(instruction):
    def __init__(self):
        super().__init__("10000", "BBG", [["10", "01", "11"], ["10", "01", "11"], ["00"]])
    def execute_instruction(self, first_agument, seconde_argumet, target_label):
        if (first_agument > seconde_argumet):
            return target_label.value
        return -2

    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].value if parsed_list[0] != "11" else binstr_to_bin_neg(
            parsed_list[1])
        second_param = memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value if parsed_list[2] != "11" else binstr_to_bin_neg(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
    def line_displayer(self, parsed_list):
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name if parsed_list[0] != "11" else str(binstr_to_bin_neg(parsed_list[1]))
        second_param = memory.memory_address[ (parsed_list[2], rm_last_bit(parsed_list[3]))].name if parsed_list[2] != "11" else str(binstr_to_bin_neg(parsed_list[3]))
        return super().line_displayer([first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [7,7,7])
#18
class BSM(instruction):
    def __init__(self):
        super().__init__("10001", "BSM", [["10", "01", "11"], ["10", "01", "11"], ["00"]])
    def execute_instruction(self, first_argument, seconde_argument, target_label):
        if (first_argument < seconde_argument):
            return target_label.value
        return -2

    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].value if parsed_list[0] != "11" else binstr_to_bin_neg(
            parsed_list[1])
        second_param = memory.memory_address[(parsed_list[2], rm_last_bit(parsed_list[3]))].value if parsed_list[2] != "11" else binstr_to_bin_neg(
            parsed_list[3])
        return self.execute_instruction(first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))])
    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:14])
        res.append(lign[14:16])
        res.append(lign[16:23])
        res.append(lign[23:25])
        res.append(lign[25:])
        return res[:]
    def line_displayer(self, parsed_list):
        first_param = memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name if parsed_list[0] != "11" else str(binstr_to_bin_neg(parsed_list[1]))
        second_param = memory.memory_address[ (parsed_list[2], rm_last_bit(parsed_list[3]))].name if parsed_list[2] != "11" else str(binstr_to_bin_neg(parsed_list[3]))
        return super().line_displayer([first_param, second_param, memory.memory_address[(parsed_list[4], rm_last_bit(parsed_list[5]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [7,7,7])
#19
class JMP(instruction):
    def __init__(self):
        super().__init__("10010", "JMP", [["00"]])
    def execute_instruction(self, target_label, param_trash_0, param_trash_1):
        return target_label.value
    def param_selection(self, parsed_list):
        self.param_type_check(parsed_list)
        return self.execute_instruction(memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))], 0, 0)

    def bin_parser(self, lign):
        res = [lign[:5]]
        res.append(lign[5:7])
        res.append(lign[7:])
        return res[:]
    def line_displayer(self, parsed_list):
        return super().line_displayer([memory.memory_address[(parsed_list[0], rm_last_bit(parsed_list[1]))].name])
    def bin_writer(self, lines):
        return super().bin_writer(lines, [25,])
#20
class HLT(instruction):
    def __init__(self):
        super().__init__("10011", "HLT", [])
    def execute_instruction(self, param_trash_0, param_trash_1, param_trash_2): #DONE: rewrite the function
        return -1
    def param_selection(self, parsed_list=0):
        return self.execute_instruction(0, 0, 0)
    def bin_parser(self, lign):
        res = [lign[:5]]
        return res[:]
    def line_displayer(self, parsed_list=0):
        return super().line_displayer([])
    def bin_writer(self, lines):
        return super().bin_writer(lines, list())
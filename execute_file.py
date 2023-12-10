from Memory import *
from Binparser import *
from Codeparser import *

class runner:
    #the runner class is used to instancied an object tha will execute each line of code
    def __init__(self, file_name):
        self.parsed = instruction_parsing(bin_part(init_and_code_to_bin(file_name)))
        self.index_ligne = 0
        self.text = ""
    def change(self, file_name):
        self.parsed = instruction_parsing(bin_part(init_and_code_to_bin(file_name)))
        self.index_ligne = 0
    def show_line(self):
        res = ""
        index = 0
        for l in self.parsed:
            i = self.parsed.index(l)
            if (self.index_ligne == index):
                res += "->"
            if (l[0] != "11111"):
                res += "\t" + instruction.intruction_dict[l[0]].line_displayer(l[1:]) + "\n"
            else:
                 res += "\t" + memory.memory_address[l[1], rm_last_bit(l[2])].name + ":\n"

            print(f"i = {i}")
            index += 1
        return res

    def execute_step(self):  # the line_tag store the tag in the code
        # parsed is the binary seperated in chunck of relevant information
        # for example the first block is always the op code of the instruction
        # new take for the line navigatio
        # uncomplete is used as a condition for navigating
        ##index_lign is used to chose wich line need to be executed
        if 0 <= self.index_ligne:  # DONE: change the condition because the instruction for the end is not always the last
            set_instruction = set(instruction.intruction_dict.keys())
            #memory_displayer()
            if (self.parsed[self.index_ligne][0] in set_instruction):
                #print(self.parsed[self.index_ligne])
                temp_rec = instruction.intruction_dict[self.parsed[self.index_ligne][0]].param_selection(
                    self.parsed[self.index_ligne][1:])
                #print(instruction.intruction_dict[self.parsed[self.index_ligne][0]].line_displayer(self.parsed[self.index_ligne][1:]))
            else:
                temp_rec = -2
            self.index_ligne = temp_rec if temp_rec != -2 else self.index_ligne + 1
        #memory_displayer()
        #print(memory.memory_address)
        return 0
    def execute_full(self): #the line_tag store the tag in the code
        #parsed is the binary seperated in chunck of relevant information
        #for example the first block is always the op code of the instruction
        #new take for the line navigatio
        #uncomplete is used as a condition for navigating
        ##index_lign is used to chose wich line need to be executed
        while 0 <= self.index_ligne: #DONE: change the condition because the instruction for the end is not always the last
            set_instruction = set(instruction.intruction_dict.keys())
            memory_displayer()
            if (self.parsed[self.index_ligne][0] in set_instruction):
                print(self.parsed[self.index_ligne])
                temp_rec = instruction.intruction_dict[self.parsed[self.index_ligne][0]].param_selection(self.parsed[self.index_ligne][1:])
                print(instruction.intruction_dict[self.parsed[self.index_ligne][0]].line_displayer(self.parsed[self.index_ligne][1:]))
            else:
                temp_rec = -2
            self.index_ligne  = temp_rec if temp_rec != -2  else self.index_ligne + 1
        memory_displayer()
        print(memory.memory_address)
        return 0

def main():
    execution_object = runner("essaiefile.txt.txt")
    user_choice = 1
    while(execution_object.index_ligne >= 0 and user_choice in {1, 2, 3}):
        user_choice = int(input("Enter one to execute one step and 2 to execute from current line to the end, endter 3 to relof the code and 4 to execute completely the code:"))
        if(user_choice == 1):
            execution_object.execute_step()
        elif(user_choice == 2):
            execution_object.execute_full()
        elif(user_choice == 3):
            execution_object = runner("essaiefile.txt.txt")
        elif(user_choice == 4):
            runner("essaiefile.txt.txt").execute_full()





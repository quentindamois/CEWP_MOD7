from Memory import *
from Binparser import *
from Codeparser import *

class runner:
    #the runner class is used to instancied an object tha will execute each line of code
    def __init__(self):
        self.parsed = instruction_parsing(bin_part(init_and_code_to_bin()))
        self.index_ligne = 0

    def execute_step(self):  # the line_tag store the tag in the code
        # parsed is the binary seperated in chunck of relevant information
        # for example the first block is always the op code of the instruction
        # new take for the line navigatio
        # uncomplete is used as a condition for navigating
        ##index_lign is used to chose wich line need to be executed
        if 0 <= self.index_ligne:  # DONE: change the condition because the instruction for the end is not always the last
            set_instruction = set(instruction.intruction_dict.keys())
            memory_displayer()
            if (self.parsed[self.index_ligne][0] in set_instruction):
                print(self.parsed[self.index_ligne])
                temp_rec = instruction.intruction_dict[self.parsed[self.index_ligne][0]].param_selection(
                    self.parsed[self.index_ligne][1:])
                print(instruction.intruction_dict[self.parsed[self.index_ligne][0]].line_displayer(
                    self.parsed[self.index_ligne][1:]))
            else:
                temp_rec = -2
            self.index_ligne = temp_rec if temp_rec != -2 else self.index_ligne + 1
        memory_displayer()
        print(memory.memory_address)
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


essaie = runner()
essaie.execute_step()
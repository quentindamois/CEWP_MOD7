import tkinter

import Memory
from execute_file import *
def actulise():
    label_var["text"] = Memory.memory_string() + f"PC = {main_runner[0].index_ligne}"
    label_stack["text"] = "stack:\n" + Memory.string_stack()
    label_code["text"] = main_runner[0].show_line()
def one_step():
    main_runner[0].execute_step()
    actulise()

def until_end():
    main_runner[0].execute_full()
    actulise()

def reset_execution():
    reset_stack_and_memory()
    print(file_name)
    main_runner[0].change(file_name[0])

    print(f"the programme is now {main_runner[0].index_ligne}")
    actulise()

def change_file(tet):
    file_name[0] = file_entry.get()
    reset_execution()


if __name__ == '__main__':
    file_name = ["essaiefile.txt.txt"]
    main_runner = [runner(file_name[0])]
    window = tkinter.Tk()
    window.title("simulator")
    window.geometry('440x325')
    label_var = tkinter.Label(window, text="non initialised")
    label_var.grid(column=0, row=0)
    label_code = tkinter.Label(window, text="non initialised")
    label_code.grid(column=2, row=0)
    label_stack = tkinter.Label(window, text="non initialised")
    label_stack.grid(column=1, row=0)
    btn_step = tkinter.Button(window, text="execute on step", command=one_step)
    btn_step.grid(column=0, row=1)
    btn_end = tkinter.Button(window, text="excute until the end", command=until_end)
    btn_end.grid(column=1, row=1)
    btn_reset = tkinter.Button(window, text="reset the execution", command=reset_execution)
    btn_reset.grid(column=2, row=1)
    label_indication = tkinter.Label(window, text="enter the file name with .txt at the end")
    label_indication.grid(column=1, row=2)
    file_entry = tkinter.Entry(window)
    file_entry.grid(column=1, row=3)
    file_entry.bind("<Return>", change_file)
    actulise()
    window.mainloop()

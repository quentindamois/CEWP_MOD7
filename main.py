import tkinter
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import Memory
from execute_file import *
def actulise():
    label_var.delete('1.0', 'end')
    label_var.insert("1.0", Memory.memory_string() + f"PC = {main_runner[0].index_ligne}")
    label_stack.delete('1.0', 'end')
    label_stack.insert("1.0", "stack:\n" + Memory.string_stack())
    label_code.delete('1.0', 'end')
    label_code.insert("1.0", main_runner[0].show_line())
def one_step():
    main_runner[0].execute_step()
    actulise()

def until_end():
    main_runner[0].execute_full()
    actulise()

def reset_execution():
    reset_stack_and_memory()
    main_runner[0].change(file_name[0])
    actulise()

def change_file(tet):
    file_name[0] = file_entry.get()
    reset_execution()


if __name__ == '__main__':
    file_name = ["test_program.txt"]
    main_runner = [runner(file_name[0])]
    window = tkinter.Tk()
    window.title("simulator")
    window.geometry('745x245')
    label_var = tkinter.Text(window, height=10, width=35)
    label_var.grid(column=0, row=0, padx=0, ipadx=0, sticky=tk.EW)
    label_code = tkinter.Text(window, height=10, width=35)
    label_code.grid(column=4, row=0, sticky=tk.EW)
    label_stack = tkinter.Text(window, height=10, width=10)
    label_stack.grid(column=2, row=0, sticky=tk.EW)
    btn_step = tkinter.Button(window, text="execute one step", command=one_step)
    btn_step.grid(column=0, row=1)
    btn_end = tkinter.Button(window, text="excute until the end", command=until_end)
    btn_end.grid(column=2, row=1)
    btn_reset = tkinter.Button(window, text="reset the execution", command=reset_execution)
    btn_reset.grid(column=4, row=1)
    label_indication = tkinter.Label(window, text="enter the path to the file with .txt at the end")
    label_indication.grid(column=0, row=2)
    file_entry = tkinter.Entry(window)
    file_entry.grid(column=0, row=3)
    file_entry.bind("<Return>", change_file)
    scrollbar_var = tkinter.Scrollbar(window, orient='vertical', command=label_var.yview)
    scrollbar_var.grid(row=0, column=1, sticky=tk.NS)
    label_var['yscrollcommand'] = scrollbar_var.set
    scrollbar_stack = tkinter.Scrollbar(window, orient='vertical', command=label_stack.yview)
    scrollbar_stack.grid(row=0, column=3, sticky=tk.NS)
    label_var['yscrollcommand'] = scrollbar_var.set
    scrollbar_code = tkinter.Scrollbar(window, orient='vertical', command=label_code.yview)
    scrollbar_code.grid(row=0, column=5, sticky=tk.NS)
    label_var['yscrollcommand'] = scrollbar_var.set
    actulise()
    window.mainloop()

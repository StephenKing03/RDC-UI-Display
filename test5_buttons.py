import tkinter as tk
from tkinter import ttk

window = tk.Tk()

def button_func():
    print('Button pressed')
    print('checkbox, state:', check_var.get())
button_string = tk.StringVar(value = " StringVar button")
button = ttk.Button(master = window, text = 'simple Button', command = button_func)
button.pack()

#checkbutton
check_var = tk.IntVar()
check = ttk.Checkbutton(window, text = 'Checkbutton', command = (lambda: print('Checkbutton state:', check.instate(['selected']))), variable = check_var) #onvalue = 1, offvalue = 0 (those are params)
check.pack()

window.mainloop()

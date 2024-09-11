import tkinter as tk
from tkinter import ttk

def button_func():
    

    #update label
    #lable.config(text = 'updated')
    lable['text'] = entry.get()

#window
window = tk.Tk()

#widgets

lable = ttk.Label(master = window, text =' JOO')
lable.pack()

entry = ttk.Entry(master = window)
entry.pack()
button = ttk.Button(master = window, text = 'The Button', command = button_func)
button.pack()

window.mainloop()
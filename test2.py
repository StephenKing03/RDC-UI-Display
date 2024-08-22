import tkinter as tk
from tkinter import ttk


def button_func():
    print('Button pressed')

#create a window

window = tk.Tk()
window.title('Window and Widgets')
window.geometry('800x500')

#ttk widgets
label = ttk.Label(master = window, text = 'Hello, World!', font = ('Calibri', 15))
label.pack()

#widgets
tk.Text(master = window).pack()



#ttk entry
entry = ttk.Entry(master = window, width = 20).pack()

#ttk button
button = ttk.Button(master = window, text = 'Submit', command = button_func).pack()

#run

window.mainloop()

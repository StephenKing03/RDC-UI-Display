import tkinter as tk
from tkinter import ttk
#window
window = tk.Tk()
window.title('Tkinter Variables')

string_var = tk.StringVar()

label = ttk.Label(master = window, text = 'label',textvariable = string_var)
entry = ttk.Entry(master = window, textvariable = string_var )
button = ttk.Button(master = window, text = 'Submit', command = lambda: print(string_var.get()))

label.pack()
entry.pack()

window.mainloop()
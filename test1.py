import tkinter as tk
from tkinter import ttk

#window
window = tk.Tk()
window.title('Robolympics Match Display')
window.geometry('800x600')

#title
title_label = ttk.Label(master = window, text='Robolympics Match Display', font=('Calibri', 20))
title_label.pack()

#input field
input_frame = ttk.Frame(master=window)
entry = ttk.Entry(master=input_frame, width=10)
button = ttk.Button(master=input_frame, text='Submit')

entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')

input_frame.pack()

#output


#run
window.mainloop()
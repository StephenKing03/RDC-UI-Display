import tkinter as tk
from tkinter import ttk

window = tk.Tk()
def get_pos(event):
    print(f'x:{event.x}, y:{event.y}')


text = tk.Text(window)
text.pack()

entry = ttk.Entry(window)
entry.pack()

btn = ttk.Button(window, text = 'A button')
btn.pack

 #events

window.bind('<Alt-KeyPress-a>', lambda event: print('Alt + a pressed'))
text.bind('<Motion>', get_pos)
entry.bind('<FocusIn>', lambda event: print('Entry focused'))
window.mainloop()
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    #main setup
    def __int__(self,title):
        super().__init__()
        self.title(title)
        self.geometry('300x300')
        self.minsize(200,300)

        #self.menu = Menu(self)
        print('welcome')
        self.mainloop()
        print('hi')

print('tjese')
App('Class based try','(200,300)')
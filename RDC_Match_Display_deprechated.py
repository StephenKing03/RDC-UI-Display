import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from  PIL import Image, ImageTk
import os
import Settings


match_settings = None
redcolor = '#ff9028'
bluecolor = '#08cdf9'
scaling_unit_height = 1
scaling_unit_width = 1
scaling_unit = 1
groundcolor = '#574f4e'
transparent_grey = '#808080'
greencolor = '#038024'

#main window for the match - controller display 
class Controller(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("RDC Match Display")
        self.geometry("800x600")

        global match_settings
        match_settings = Settings.MatchSettings()

        #define a grid
        self.columnconfigure(0, weight = 2, uniform = 'b')
        self.columnconfigure(1, weight = 2, uniform = 'b')

        self.rowconfigure(0, weight = 75)
        self.rowconfigure(1, weight = 25)
        self.rowconfigure(2, weight = 25,)

        #define the frames
        self.Settings = SettingsDisplay(self)
        self.Settings.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        #define all the buttons to control match
        self.Button_frame = ctk.CTkFrame(self, fg_color = groundcolor)
        self.Button_frame.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        self.InitDisplay = ctk.CTkButton(self.Button_frame, text = "Init Display", fg_color = '#870065', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, command = self.start_display)
        self.InitDisplay.pack(expand = True, fill = 'both', side = 'left', padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        self.StartMatch = ctk.CTkButton(self.Button_frame, text = "Start Match", fg_color = 'green', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.StartMatch.pack(expand = True, fill = 'both', side = 'left', padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        self.ConfirmScore = ctk.CTkButton(self.Button_frame, text = "Confirm Score", fg_color = 'blue', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.ConfirmScore.pack(expand = True, fill = 'both', side = 'left', padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        self.ResetScore = ctk.CTkButton(self.Button_frame, text = "Reset Score", fg_color = 'red', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, command = match_settings.reset_match)
        self.ResetScore.pack(expand = True, fill = 'both', side = 'left', padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        
        #load two frames for both teams' scores
        self.Scoring_blue = Scoring(self, bluecolor)
        self.Scoring_blue.grid(row = 2, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        self.Scoring_red = Scoring(self, redcolor)
        self.Scoring_red.grid(row = 2, column = 1, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

    #start the display for the teams
    def start_display(self):
        print("Display Started")
        self.team_display = Display(self)
        
        self.team_display.mainloop()

    def start_match(self):

        update_matchtimer()
        
        def update_matchtimer(self):
            global match_settings
            current_time = self.current_time.get()

            #update refill timer
            if current_time > match_settings.firstball_drop:
                match_settings.refill_time.set(int(current_time - self.firstball_drop))
                match_settings.event_trigger.set("waiting_firstdrop")
            elif current_time > match_settings.secondball_drop:
                match_settings.refill_time.set(int(current_time - match_settings.firstball_drop))
                match_settings.event_trigger.set("waiting_seconddrop")
            elif current_time > match_settings.thirdball_drop:
                match_settings.refill_time.set(int(current_time - self.thirdball_drop))
                match_settings.event_trigger.set("waiting_thirddrop")
            elif current_time > match_settings.endgame_duration:
                match_settings.refill_time.set(int(current_time - self.endgame_duration))
                match_settings.event_trigger.set("waiting_endgame")
            else:
                match_settings.refill_time.set(-1)
                match_settings.event_trigger.set("waiting_endgame")
                
            #advance the matchtimer
            if current_time > 0:
                match_settings.current_time.set(current_time -1)
                match_settings._instance.after(1000, match_settings.update_matchtimer) #initiate the next instance
            else:
                #trigger match over!
                pass 

    '''define functions that act on certain timed events, like ball drop and add functions in update_matchtimer function'''

    


#all the settings (may replace settings.json)
class SettingsDisplay(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.add_teamnames()

    def add_teamnames(self):
        
        global match_settings 
        #teamnames
        team1_1_entry = ctk.CTkEntry(self, placeholder_text = "Blue 1 ", textvariable= match_settings.teamblue_1_name, fg_color = bluecolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        team1_2_entry = ctk.CTkEntry(self, placeholder_text = "Blue 2 ", textvariable= match_settings.teamblue_2_name, fg_color = bluecolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        team2_1_entry = ctk.CTkEntry(self, placeholder_text = "Red 1 ", textvariable= match_settings.teamred_1_name, fg_color = redcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        team2_2_entry = ctk.CTkEntry(self, placeholder_text = "Red 2 ",textvariable= match_settings.teamred_2_name, fg_color = redcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)

        team1_1_entry.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        team1_2_entry.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        team2_1_entry.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        team2_2_entry.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        '''
        #settings for total time
        time_display = labeled_box(self, ":Total Time", "120s")
        time_display.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        #time for refill
        refill_display = labeled_box(self, ":Refill Time", "30s")
        refill_display.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        #other crazy setting
        other_display = labeled_box(self, ":This is a very long long label:", "30s")
        other_display.pack(side = 'top', fill = tk.BOTH, expand = True, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        pass
        '''

#scoring for both teams
class Scoring(ctk.CTkFrame):
    def __init__(self, master, color):
        super().__init__(master, fg_color = color)
        self.color = color

        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 1, uniform = 'a')

        self.rowconfigure(0, weight = 1, uniform = 'b')
        self.rowconfigure(1, weight = 1, uniform = 'b')

        self.Frame_goals = ctk.CTkFrame(self, fg_color = 'grey')
        self.Frame_goals.pack(side= 'left', fill = tk.BOTH, expand = False, padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        self.Frame_other = ctk.CTkFrame(self, fg_color = 'grey')
        self.Frame_other.pack(side = 'left', fill = tk.BOTH, expand = False, padx = 10 * scaling_unit, pady = 10 * scaling_unit)

        #actually create the interfaces
        self.create_goals()
        self.create_other()

    def create_goals(self):

        global match_settings
        #define grid
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 1, uniform = 'a')
        self.columnconfigure(2, weight = 1, uniform = 'a')

        self.rowconfigure(0, weight = 1, uniform = 'b')
        self.rowconfigure(1, weight = 1, uniform = 'b')
        self.rowconfigure(2, weight = 1, uniform = 'b')
        self.rowconfigure(3, weight = 1, uniform = 'b')

        
        #define points labels
        self.highgoal_label = ctk.CTkLabel(self.Frame_goals, textvariable = match_settings.teamblue_highgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.midgoal_label = ctk.CTkLabel(self.Frame_goals, textvariable = match_settings.teamblue_midgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.lowgoal_label = ctk.CTkLabel(self.Frame_goals, textvariable = match_settings.teamblue_lowgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)

        self.highgoal_label.grid(row = 1, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.midgoal_label.grid(row = 2, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.lowgoal_label.grid(row = 3, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        #define plus_buttons
        self.highgoal_button_p = ctk.CTkButton(self.Frame_goals, text = "+", fg_color = 'green', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.increment_score(match_settings.teamblue_highgoal))
        self.midgoal_button_p = ctk.CTkButton(self.Frame_goals, text = "+", fg_color = 'green', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.increment_score(match_settings.teamblue_midgoal))
        self.lowgoal_button_p = ctk.CTkButton(self.Frame_goals, text = "+", fg_color = 'green', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.increment_score(match_settings.teamblue_lowgoal))

        self.highgoal_button_p.grid(row = 1, column = 1, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.midgoal_button_p.grid(row = 2, column = 1, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.lowgoal_button_p.grid(row = 3, column = 1, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        #define_minus_buttons   
        self.highgoal_button_m = ctk.CTkButton(self.Frame_goals, text = "-", fg_color = 'red', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.decrement_score(match_settings.teamblue_highgoal))
        self.midgoal_button_m = ctk.CTkButton(self.Frame_goals, text = "-", fg_color = 'red', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.decrement_score(match_settings.teamblue_midgoal))
        self.lowgoal_button_m = ctk.CTkButton(self.Frame_goals, text = "-", fg_color = 'red', font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.decrement_score(match_settings.teamblue_lowgoal))

        self.highgoal_button_m.grid(row = 1, column = 2, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.midgoal_button_m.grid(row = 2, column = 2, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.lowgoal_button_m.grid(row = 3, column = 2, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        self.total_name_label = ctk.CTkLabel(self.Frame_goals, text = "Total:", fg_color = 'grey', font = ('Helvetica', 10 * scaling_unit, 'bold'), corner_radius = 15)
        self.total_name_label.grid(row = 4, column = 0, columnspan = 1, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        self.total_score_label = ctk.CTkLabel(self.Frame_goals, textvariable = match_settings.blue_total_score, fg_color = self.color, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)    
        self.total_score_label.grid(row = 4, column = 1, columnspan = 2, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5 * scaling_unit)




    #create all the other opportunities for points inclduing parking and penalty
    def create_other(self):

        global match_settings

        #define grid
        self.columnconfigure(0, weight = 10, uniform = 'a')
        self.columnconfigure(1, weight = 1, uniform = 'a')
        self.columnconfigure(2, weight = 1, uniform = 'a')

        self.rowconfigure(0, weight = 1, uniform = 'b')
        self.rowconfigure(1, weight = 1, uniform = 'b')
        self.rowconfigure(2, weight = 2, uniform = 'b')
        self.rowconfigure(3, weight = 2, uniform = 'b')

        #define dropdown menu with 3 states of climbing and a label for robot 1
        self.climbing_label_1 = ctk.CTkLabel(self.Frame_other, text = "Robot 1", fg_color = groundcolor, font = ('Helvetica', 10 * scaling_unit,), corner_radius = 0)
        self.climbing_label_1.grid(row = 1, column = 0, columnspan = 1, sticky = 'nsew', padx = 0 * scaling_unit, pady = 5 * scaling_unit)

        
        self.climbing_dropdown_1 = ctk.CTkOptionMenu(self.Frame_other, variable = match_settings.robotblue1_park, values = ["not parked", "low park", "high park"])
        self.climbing_dropdown_1.grid(row=1, column=1, columnspan=2, sticky='nsew', padx=0 * scaling_unit, pady=5 * scaling_unit)

        #define dropdown menu with 3 states of climbing and a label for robot 2
        self.climbing_label_2 = ctk.CTkLabel(self.Frame_other, text = "Robot 1", fg_color = groundcolor, font = ('Helvetica', 10 * scaling_unit,), corner_radius = 0)
        self.climbing_label_2.grid(row = 2, column = 0, columnspan = 1, sticky = 'nsew', padx = 0 * scaling_unit, pady = 5 * scaling_unit)

        self.climbing_dropdown_2 = ctk.CTkOptionMenu(self.Frame_other, variable = match_settings.robotblue2_park , values = ["not parked", "low park", "high park"])
        self.climbing_dropdown_2.grid(row=2, column=1, columnspan=2, sticky='nsew', padx=0 * scaling_unit, pady=5 * scaling_unit)


        #create penalty points in the form of a label, where the amount of current penalty points is displayed and four buttons where one can add and remove two different amounts of points
        self.penalty_label = ctk.CTkLabel(self.Frame_other, textvariable = match_settings.teamblue_penalty, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'))
        self.penalty_label.grid(row = 4, column = 0, sticky = 'nsew', padx = 0 * scaling_unit, pady = 1 * scaling_unit)

        self.penalty_text_label = ctk.CTkLabel(self.Frame_other, text = "Penalty Points:", fg_color = groundcolor, font = ('Helvetica', 8 * scaling_unit, 'bold'))
        self.penalty_text_label.grid(row = 3, column = 0, sticky = 'nsew', padx =0 * scaling_unit, pady = 1 * scaling_unit)

        self.penalty_button_p1 = ctk.CTkButton(self.Frame_other, text = "+small", fg_color = 'green', font = ('Helvetica', 10 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.small_penalty(match_settings.teamblue_penalty))
        self.penalty_button_p2 = ctk.CTkButton(self.Frame_other, text = "+big", fg_color = 'green', font = ('Helvetica', 10 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.big_penalty(match_settings.teamblue_penalty))
        self.penalty_button_m1 = ctk.CTkButton(self.Frame_other, text = "-small", fg_color = 'red', font = ('Helvetica', 10 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.small_penalty(match_settings.teamblue_penalty, False))
        self.penalty_button_m2 = ctk.CTkButton(self.Frame_other, text = "-big", fg_color = 'red', font = ('Helvetica', 10 * scaling_unit, 'bold'), corner_radius = 15, width = 10, command = lambda: match_settings.big_penalty(match_settings.teamblue_penalty, False))

        self.penalty_button_p1.grid(row = 3, column = 1, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.penalty_button_p2.grid(row = 4, column = 1, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.penalty_button_m1.grid(row = 3, column = 2, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)
        self.penalty_button_m2.grid(row = 4, column = 2, sticky = 'ns', padx = 5 * scaling_unit, pady = 5 * scaling_unit)

#use for in display, e.g. for settings
class labeled_box(ctk.CTkFrame):
    def __init__(self, master, labeltext, boxtext):
        super().__init__(master)

        
        self.box = ctk.CTkEntry(self, placeholder_text = boxtext, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 50)
        self.box.pack(side = 'left', fill = tk.BOTH, expand = False, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

        self.label = ctk.CTkLabel(self, text = labeltext, fg_color = "transparent", font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15, width = 60)
        self.label.pack(side = 'left', fill = tk.BOTH, expand = False, padx = 5 * scaling_unit, pady = 5 * scaling_unit)

'''#main window for the team display '''
class Display(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("RDC Match Display")
        self.geometry("800x600")
        #self.style = ttk.Style()
        #self.style.theme_use("bootstrap")
        #self.create_widgets()
        self.match_settings = match_settings

        #define a grid
        self.columnconfigure(0, weight = 3, uniform = 'b')
        self.columnconfigure(1, weight = 2, uniform = 'b')
        self.columnconfigure(2, weight = 3, uniform = 'b')

        self.rowconfigure(0, weight = 75)
        self.rowconfigure(1, weight = 25)
        
        #define the frames
        self.blue_console = TeamConsole(self, bluecolor)
        self.blue_console.grid(row = 0, column = 0, sticky = 'nsew')

        self.middle_console = MiddleConsole(self)
        self.middle_console.grid(row = 0, column = 1, sticky = 'nsew')

        self.red_console = TeamConsole(self, redcolor)
        self.red_console.grid(row = 0, column = 2, sticky = 'nsew')
        
        self.match_status_console = MatchStatusConsole(self)
        self.match_status_console.grid(row = 1, column = 0, columnspan = 3, sticky = 'nsew')

        #close the app on escape
        self.bind("<Escape>", lambda event: self.destroy())

class MatchStatusConsole(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color = 'grey')
        self.create_widgets()

    def create_widgets(self):

        global match_settings

        #define grid
        self.columnconfigure(0, weight = 3, uniform = 'c')
        self.columnconfigure(1, weight = 3, uniform = 'c')
        self.columnconfigure(2, weight = 3, uniform = 'c')
        
        
        self.rowconfigure(0, weight = 1, uniform = 'd') #progress bar
        self.rowconfigure(1, weight = 2, uniform = 'd')
        self.rowconfigure(2, weight = 2, uniform = 'd')

        #progress bar
        self.progress = ctk.CTkProgressBar(self, mode = 'determinate')
        self.progress.grid(row = 0, column = 0, columnspan = 3, sticky = 'nsew')

        #points display
        self.pointsFrame = ctk.CTkFrame(self, fg_color = 'black')
        self.pointsFrame.grid(row = 1, column = 1, rowspan = 2, sticky = 'nsew')

        points_blue_label = ctk.CTkLabel(self.pointsFrame, textvariable = match_settings.blue_total_score, fg_color = bluecolor, font = ('Helvetica', 60 * scaling_unit_height, 'bold'), )
        points_red_label = ctk.CTkLabel(self.pointsFrame, text = "15", fg_color = redcolor, font = ('Helvetica', 60 * scaling_unit_height, 'bold'), )
        
        points_blue_label.pack(side = tk.LEFT, fill = "both", expand = True)
        points_red_label.pack(side = tk.RIGHT, fill = "both", expand = True)

        
        #team names
        name_height = scaling_unit_height * 50
        name_width = scaling_unit_width  * 250
        self.team1_1 = ctk.CTkLabel(self, textvariable = match_settings.teamblue_1_name, fg_color = groundcolor, font = ('Helvetica', 15 * scaling_unit, 'bold'), width = name_width, height = name_height,padx = 5*scaling_unit, pady = 5 * scaling_unit, anchor = 'w')
        self.team1_1.grid(row = 1, column = 0, sticky = 'ew')
        
        self.team1_2 = ctk.CTkLabel(self, textvariable = match_settings.teamblue_2_name, fg_color = groundcolor, font = ('Helvetica', 15 * scaling_unit, 'bold'), width = name_width, height = name_height,padx = 5*scaling_unit, pady = 10 * scaling_unit, anchor = 'w')
        self.team1_2.grid(row = 2, column = 0, sticky = 'ew')

        self.team2_1 = ctk.CTkLabel(self, textvariable = match_settings.teamred_1_name, fg_color = groundcolor, font = ('Helvetica', 15 * scaling_unit, 'bold'), width = name_width, height = name_height,padx = 5*scaling_unit, pady = 5 * scaling_unit, anchor = 'e')
        self.team2_1.grid(row = 1, column = 2, sticky = 'ew')
        
        self.team2_2 = ctk.CTkLabel(self, textvariable = match_settings.teamred_2_name, fg_color = groundcolor, font = ('Helvetica', 15 * scaling_unit, 'bold'), width = name_width, height = name_height,padx = 5*scaling_unit, pady = 10 * scaling_unit, anchor = 'e')
        self.team2_2.grid(row = 2, column = 2, sticky = 'ew')
        
class MiddleConsole(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color = groundcolor)
        self.create_widgets()

    def create_widgets(self):

        global match_settings
        #define grid

        self.columnconfigure(0, weight = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)


        #refill_timer frame
        self.refill_timer_frame = ctk.CTkFrame(self, fg_color = groundcolor)
        self.refill_timer_frame.pack(fill = tk.X, expand = False)

        self.refill_timer_label = ctk.CTkLabel(self.refill_timer_frame, text = "Nachschub in: ", fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'))
        self.refill_timer_label.pack(fill = tk.X, expand = True)
        
        self.refill_timer_time = ctk.CTkLabel(self.refill_timer_frame, textvariable = match_settings.refill_time, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'))
        self.refill_timer_time.pack()

        self.refill_endgame_label = ctk.CTkLabel(self.refill_timer_frame, text = "Finale Phase!", fg_color = "green", font = ('Helvetica', 20 * scaling_unit, 'bold'))
        #not packed here

        self.refill_progress = ctk.CTkProgressBar(self, mode = 'determinate')   
        self.refill_progress.pack(fill = tk.X, expand = False)

        #timer display
        self.timer = ctk.CTkLabel(self, text = "00:00", fg_color = 'black', font = ('Helvetica', 60 * scaling_unit, 'bold'))
        self.timer.pack(fill = tk.BOTH, expand = True)

        def on_change_to_endgame(self):
            if match_settings.event_trigger == "wait endgame":
                self.refill.timer_label.configure(text = "Finale Phase in: ")
            elif match_settings.event_trigger == "endgame":
                self.refill.timer_label.configure(text = "Finale Phase! ")
                self.refill_timer_label.pack_forget()
                self.refill_timer_time.pack_forget()
                self.refill_endgame_label.pack()


    def animate_endgame(self):
        pass

class TeamConsole(ctk.CTkFrame):
    def __init__(self, master,color):
        super().__init__(master, fg_color = color)
        self.create_widgets(color)
        self.init_color = color

    def create_widgets(self, color):

        global match_settings
        #create grid
        self.init_color = color
        self.columnconfigure(0, weight = 3, uniform = 1)
        self.columnconfigure(1, weight = 5, uniform = 1)

        self.rowconfigure(0, weight = 2, uniform = 'a')
        self.rowconfigure(1, weight = 2, uniform = 'a')
        self.rowconfigure(2, weight = 2, uniform = 'a')
        self.rowconfigure(3, weight = 3, uniform = 'a')
        #import the image for the goal
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        image_path = os.path.join(script_dir, "GoalZeichnung.png")
        self.resized_image = Image.open(image_path).resize((100, 100))
        

        self.image_canvas = tk.Canvas(self, background = groundcolor)
        self.image_canvas.grid(row = 0, column = 1, rowspan = 3, sticky = 'nsew', padx = 5 * scaling_unit, pady = 25 * scaling_unit)

         # Bind the configure event to resize the image
        self.image_canvas.bind('<Configure>', self.resize_image)
        
        #import labels for scores:
        self.highgoal_label = ctk.CTkLabel(self, textvariable = match_settings.teamblue_highgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.midgoal_label = ctk.CTkLabel(self,textvariable = match_settings.teamblue_midgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        self.lowgoal_label = ctk.CTkLabel(self, textvariable = match_settings.teamblue_lowgoal, fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)

        self.highgoal_label.grid(row = 0, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 25 * scaling_unit)
        self.midgoal_label.grid(row = 1, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 25 * scaling_unit)
        self.lowgoal_label.grid(row = 2, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 25 * scaling_unit)

        class parking_display(ctk.CTkFrame):
            def __init__(self, master, variable = None):
                super().__init__(master, border_color = "black", border_width= 5, fg_color = groundcolor)

                self.tkvariable = variable

                self.rowconfigure((0,1,2), weight = 1, uniform = 'f')
                self.columnconfigure(0, weight = 1, uniform = 'g')
                self.parkingindicator = ctk.CTkLabel(self, text = " -P-", bg_color= "transparent", fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
                self.parkingindicator.grid(row = 0, column = 0, sticky = 'nsew', padx = 5 * scaling_unit, pady = 5* scaling_unit)

                self.parkingindicator_high = ctk.CTkLabel(self, text = "H", bg_color= "transparent", fg_color = transparent_grey, font = ('Helvetica', 20 * scaling_unit), corner_radius = 8)          
                self.parkingindicator_high.grid(row = 1, column = 0, sticky = 'nsew', padx = 15 * scaling_unit, pady = 7 * scaling_unit)

                self.parkingindicator_low = ctk.CTkLabel(self, text = "L", bg_color= "transparent", fg_color = transparent_grey, font = ('Helvetica', 20 * scaling_unit), corner_radius = 8)
                self.parkingindicator_low.grid(row = 2, column = 0, sticky = 'nsew', padx = 15 * scaling_unit, pady = 7 * scaling_unit)

                # Trace the variable to call update_parking whenever it changes
                if variable is not None:
                    variable.trace_add("write", lambda *args: self.update_parking())

            def update_parking(self):
                if(self.tkvariable.get() == "not parked"):
                    self.parkingindicator_low.configure(fg_color = transparent_grey)
                    self.parkingindicator_high.configure(fg_color = transparent_grey)
                elif(self.tkvariable.get() == "low park"):
                    self.parkingindicator_low.configure(fg_color = greencolor)
                    self.parkingindicator_high.configure(fg_color = transparent_grey)
                elif(self.tkvariable.get() == "high park"):
                    self.parkingindicator_low.configure(fg_color = transparent_grey)
                    self.parkingindicator_high.configure(fg_color = greencolor)
                else:
                    print("Error occured")
        
        bottom_frame = tk.Frame(self,background = self.init_color)
        bottom_frame.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew')

        bottom_frame.grid_columnconfigure((1,2), weight = 1, uniform = 'h')
        bottom_frame.grid_rowconfigure(1, weight = 1, uniform = 'h')

        self.park1 = parking_display(bottom_frame, match_settings.robotblue1_park).grid(row = 0, column = 1, sticky = 'nsew', padx = 25 * scaling_unit)
        self.park2 = parking_display(bottom_frame,match_settings.robotblue2_park).grid(row = 0, column = 2, sticky = 'nsew', padx = 25 * scaling_unit)

        #self.penalty_frame = ctk.CTkLabel(bottom_frame, text = "0", fg_color = groundcolor, font = ('Helvetica', 20 * scaling_unit, 'bold'), corner_radius = 15)
        
    
    def resize_image(self, event):
        # Get the new size of the frame
        new_width = int(event.width)
        new_height = event.height

        # Resize the image to fit the frame
        resized_image = self.resized_image.resize((new_width, new_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # Update the label's image
        self.image_canvas.create_image(0, 0, image=self.image_tk, anchor='nw')        
        


controller = Controller()
controller.mainloop()

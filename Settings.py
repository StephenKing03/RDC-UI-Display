import tkinter as tk

#this is the class for all the match settings and tkinter variables that are imported everywhere
#singleton class to store all the settings that can be set in the controller and displayed in the display

class MatchSettings:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MatchSettings, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):

        self.pointslow = 5
        self.pointsmid = 7
        self.pointshigh = 10
        self.pointsparkhigh = 15
        self.pointsparklow = 6
        self.smallpenalty = 15
        self.bigpenalty = 30

        #all the settings that can be changed for the match, times are at which time this happens
        self.total_matchtime = 60
        self.endgame_duration = self.total_matchtime - 50
        self.firstball_drop = self.total_matchtime - 10
        self.secondball_drop = self.total_matchtime - 20
        self.thirdball_drop = self.total_matchtime - 40

        self.event_trigger = tk.StringVar(value = "nothing")
        self.match_stopped = tk.BooleanVar(value = False)

        self.current_time = tk.DoubleVar(value = self.total_matchtime)
        self.refill_time = tk.DoubleVar(value = self.firstball_drop - self.total_matchtime)

        self.teamblue_1_name = tk.StringVar(value ='b1')
        self.teamblue_2_name = tk.StringVar(value = 'b2')
        self.teamred_1_name = tk.StringVar(value = 'r1')
        self.teamred_2_name = tk.StringVar(value = 'r2')

        #all the scoring communication using tkinter variables ( they are continuously updated while the mainloop() runs )
        self.teamred_highgoal = tk.IntVar(value = 0)
        self.teamred_midgoal = tk.IntVar(value = 0)
        self.teamred_lowgoal = tk.IntVar(value = 0)
        self.robotred1_park = tk.StringVar(value = "not parked")
        self.robotred2_park = tk.StringVar(value = "not parked")
        self.teamred_penalty = tk.IntVar(value = 0)

        self.teamblue_highgoal = tk.IntVar(value = 0)
        self.teamblue_midgoal = tk.IntVar(value = 0)
        self.teamblue_lowgoal = tk.IntVar(value = 0)
        self.robotblue1_park = tk.StringVar(value = "not parked")
        self.robotblue2_park = tk.StringVar(value = "not parked")
        self.teamblue_penalty = tk.IntVar(value = 0)

        self.blue_total_score = tk.IntVar(value = 0)
        self.red_total_score = tk.IntVar(value = 0)

         # Trace changes to individual variables to update the total score
        self.teamblue_highgoal.trace_add("write", self.update_blue_total_score)
        self.teamblue_midgoal.trace_add("write", self.update_blue_total_score)
        self.teamblue_lowgoal.trace_add("write", self.update_blue_total_score)
        self.robotblue1_park.trace_add("write", self.update_blue_total_score)
        self.robotblue2_park.trace_add("write", self.update_blue_total_score)
        self.teamblue_penalty.trace_add("write", self.update_blue_total_score)



    def update_blue_total_score(self, *args):
        total = (self.teamblue_highgoal.get()*self.pointshigh +
                    self.teamblue_midgoal.get()*self.pointsmid +
                    self.teamblue_lowgoal.get()*self.pointslow)
        
        if(self.robotblue1_park.get() == "high park"):
            total += self.pointsparkhigh
        elif(self.robotblue1_park.get() == "low park"):
            total += self.pointsparklow

        total += self.teamblue_penalty.get()

        self.blue_total_score.set(total)
        

    #easy match reset for the next match
    def reset_match(self):

        self.teamred_highgoal.set(0)
        self.teamred_midgoal.set(0)
        self.teamred_lowgoal.set(0)
        self.robotred1_park.set(value = "not parked")
        self.robotred2_park.set(value = "not parked")
        self.teamred_penalty.set(0)

        self.teamblue_highgoal.set(0)
        self.teamblue_midgoal.set(0)
        self.teamblue_lowgoal.set(0)
        self.robotblue1_park.set(value = "not parked")
        self.robotblue2_park.set(value = "not parked")
        self.teamblue_penalty.set(0)

        self.current_time.set(value = self.total_matchtime)
        self.refill_time.set(value =  self.total_matchtime  - self.firstball_drop)
        self.event_trigger.set(value = "reset match")
        self.match_stopped.set(True)

    def increment_score(self, variable):
        variable.set( variable.get() + 1)
        print("incremented score")

    def decrement_score(self,variable):
        variable.set(variable.get() - 1)
        print("decremented score")

    def small_penalty(self, variable, add = True):

        if(add):
            print("added small penalty")
            variable.set(variable.get() + self.smallpenalty)
        else:
            print("subtracted small penalty")
            variable.set(variable.get() - self.smallpenalty)

    def big_penalty(self, variable, add = True):

        if(add):
            print("added big penalty")
            variable.set(variable.get() + self.bigpenalty)
        else:
            print("subtracted big penalty")
            variable.set(variable.get() - self.bigpenalty)

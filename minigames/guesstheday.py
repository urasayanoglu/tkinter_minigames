
# File       :  guesstheday.py
# Authors    :  Sebastian Sopola, Uras Ayanoglu, Jerry Karkainen
# Description:  This game is memory game. It is played to check if user gets day's weekday correct.


# Import necessary libaries
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, date 
import random
from minigames.game_components import GamePlay, Player
from minigames.playerdatabase import UserDataBase


# This class handles game interaction
class GuessTheDay(tk.Frame, GamePlay):

    # Establishing parameters
    def __init__(self,parent,player_info, status):
        self.parent = parent
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        '''initializes Window's attributes'''
        super().__init__(master=parent)
        self.title = "Guess The Day"
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.today = datetime.now().weekday()
        self.days = []
        self.attempt = 0
        self._status = ("passed", "failed", "follow")
        self.hints = [f"Yesterday was the {self.today}. day of the week", f"Today is the {self.today + 1}. day of the week", f"8 days later, it will be {self.weekdays[(self.today +1)]}"] 
        self.player_info = player_info  # current player name
        self.database = UserDataBase()  # database object 
        
        
        game_label = ttk.Label(self, text=self.title, font=("Helvetica", 40))
        game_label.grid(row=0, column=0, columnspan=5, sticky=tk.NSEW)
        
        # Buttons for the days of the week
        day_options = self.pick()
        day1_button = ttk.Button(self, text=day_options[0], command=lambda: self.game_play(day_options[0]))
        day1_button.grid(row=1, column=1, pady=3, sticky=tk.NSEW)

        day2_button = ttk.Button(self, text=day_options[1], command=lambda: self.game_play(day_options[1]))
        day2_button.grid(row=1, column=2, pady=3, sticky=tk.NSEW)

        day3_button = ttk.Button(self, text=day_options[2], command=lambda: self.game_play(day_options[2]))
        day3_button.grid(row=1, column=3, pady=3, sticky=tk.NSEW)

        day4_button = ttk.Button(self, text=day_options[3], command=lambda: self.game_play(day_options[3]))
        day4_button.grid(row=1, column=4, pady=3, sticky=tk.NSEW)


        # Button for closing the game
        close_button = ttk.Button(self, text='Quit', command=self.__close)
        close_button.grid(row=5, column=4, columnspan=5, sticky=tk.NSEW) 

        self.database.see_database()

        
        # check variable to store information: was player cleared to play GuessTheDay game
        self.status = status
        print(self.status)
        self.play_Or_Not(status)
        

    def play_Or_Not(self,status):
        '''
        function to be called first when game object is made to determine is player allowed to play or not ( 1 game a day )
        '''
        print(status)
        if ( status == True ):

            pass
        else:
            self.parent.destroy()



    def pick(self):
        # randomly generate three wrong weekdays
        if not self.days:
            while len(self.days) <= 2:
                wrong_day = random.randint(0,6)
                if wrong_day != self.today and self.weekdays[wrong_day] not in self.days:
                    self.days.append(self.weekdays[wrong_day])

            self.days.insert(random.randint(0,3), self.weekdays[self.today])

            return self.days


    def check(self, answer):
        # Check user answer
        if answer == self.weekdays[self.today]:
            print("True") # This print statement is for testing purposes only to check if the function works
            return True
        else:
            self.attempt += 1
            print("False") # This print statement is for testing purposes only to check if the function works
            return False

    def hint(self):
        print(random.choice(self.hints))


    def show(self):
        # Show 4 weekdays to choose one
        for i in range(4):
            print(f"{i}. {self.days[i]}")


    def restart(self):
        # restart the game 
        self.attempt = 0
        self.days = []


    def __close(self):
        '''asking if closing is intended'''
        if messagebox.askyesno("Close", "Do you want to close the Guess the Day game?"):
            self.parent.destroy()
            
    def game_play(self, guess):
        self.attempt += 1
        if self.attempt < 2:
            if guess == self.weekdays[self.today]:
                print(self._status[0]) # This should be added to the database to be followed up by nursing home personnel
                ttk.tkinter.messagebox.showinfo(title="Correct!", message="You guessed the day corret!\nThanks for playing.\nHave a nice day!")
                self.parent.destroy()
                self.database.add_score(self._status[0],date.today(),self.player_info)
                self.database.see_database()        # coding purposes only
                
            else:
                print(self.attempt)
                self.hint()
                ttk.tkinter.messagebox.showinfo(title="hint", message=random.choice(self.hints))
        elif self.attempt == 2 and guess == self.weekdays[self.today]:
            ttk.tkinter.messagebox.showinfo(title="Correct!", message="You guessed the day corret!\nThanks for playing.\nHave a nice day!")
            self.parent.destroy()
            self.database.add_score(self._status[0],date.today(),self.player_info)
            self.database.see_database()        # coding purposes only
        else:
            ttk.tkinter.messagebox.showinfo(title="Good Bye!", message="Thanks for playing.\nHave a nice day!")
            self.parent.destroy()
            self.database.add_score(self._status[1],date.today(),self.player_info)
            self.database.see_database()        # coding purposes only
        
    
    # End of user code

if __name__ == "__main__":
    app = GuessTheDay()
    app.mainloop()


# Start of user code -> functions/methods for memorygame package

# End of user code

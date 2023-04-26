# File          doubledice.py
# Authors    :  Sebastian Sopola, Uras Ayanoglu, Jerry Karkainen
# Description:  This is a dice game called that checks player guess if it is less, equal or greater than 7 against outcomes of the dice.
# --------------------------------------------------------------------------------------------------------------------------------------

# Import necessary libaries
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image,ImageTk
from pathlib import Path
import random
from minigames.game_components import GamePlay, Player
from minigames.playerdatabase import UserDataBase
# --------------------------------------------------------------------------------------------------------------------------------------

class DoubleDice(tk.Frame, GamePlay, Player):
    def __init__(self, parent, player_info):
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        '''initializes Window's attributes'''
        super().__init__(master=parent)
        self.parent = parent
        self.title = "Double Dice"
        self.dice1 = 0
        self.dice2 = 0
        self.both_dice = (self.dice1, self.dice2)
        self.dice_dots = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        self.dice_sum = 0
        self.bet_value = 0
        self.player_guess = tk.StringVar()
        self.win = False
        self.game_round_result = None 
        self.initial_points = 100
        self.player_points = 100

        # current user playing the game
        self.player_info = player_info

        # database object
        self.database = UserDataBase() 

        # player information of current user
        self.player_information = self.database.find_player(self.player_info)

        # function to determine does game open new session or run old if it was not finished
        self.check_game_state()


        self.rules = """
        Double Dice Game Rules:

        - Double dice, is a game that is played with two dice. Player starts the game with 100 points. 
        At the beginning of the game, two dice are thrown but are not shown to the player.  
        After the dice are thrown, the player needs to place their bet which is always between 1 and 100 points. 
        
        - Then the player is asked if the sum of the dice is less, equal, or bigger than 7. 
        After being asked, the player makes their guess by selecting one of the options listed, "less", "equal" or "greater".
        
        1. If the player's guess and the sum are in the same range, the player gets its bet * 100 points.
        (e.g., player guesses "less" and the sum of the dice comes under 7.) 
        
        2. If the player guesses "equal", and the sum of the dice is 7 then the player gets its bet * 1000 points 
        but if the sum of the dice is not 7, then the player loses its bet * 100 points. 
        
        3. If the sum of the dice and the player's guess are in opposite ranges, then the player loses its bet * 10.  
        (e.g., player guesses "less" and the sum of the dice come over 7.)

        - Overall points for the game cannot be negative and in case this happens the points are set to zero. 
        The points are saved for each game.
        
        """  

        # Display Game Title 
        game_label = ttk.Label(self, text=self.title, font=("Helvetica", 40))
        game_label.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

        # Label that shows the points
        self.points_label = ttk.Label(self, text=f"Points: {self.player_points}")
        self.points_label.grid(row=0, column=4, sticky=tk.NE)

        # Display Dice
        self.dice_label = ttk.Label(self, font=("Helvetica", 100))
        self.dice_label.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)

        # Display Result
        self.result_label = ttk.Label(self, font=("Helvetica", 40))
        self.result_label.grid(row=1, column=3, columnspan=3, sticky=tk.NSEW)
        
        # Spinbox for setting the points
        self.points_slider = ttk.Spinbox(self, from_=1, to=100)
        self.points_slider.grid(row=3, column=1, columnspan=2, sticky=tk.NSEW)

        # Buttons for the bet, less, equal and greater options
        
        bet_button = ttk.Button(self, text='Bet', command=self.bet)
        bet_button.grid(row=3, column=3, sticky=tk.NSEW)

                
        #style = ttk.Style()
        #style.configure("TRadiobutton", background=self.cget("background"), foreground=self.cget("foreground"), indicatorsize=15)

        #less_button = ttk.Button(self, text='Less', command=self.run) 
        #less_button.grid(row=3, column=1, sticky=tk.NSEW)
        less_button = ttk.Radiobutton(self, text='Less', variable=self.player_guess, value='less', command=self.game_play)
        less_button.grid(row=4, column=1, sticky=tk.NSEW)

        #equal_button = ttk.Button(self, text='Equal', command=self.run)
        #equal_button.grid(row=3, column=2, sticky=tk.NSEW)
        equal_button = ttk.Radiobutton(self, text='Equal', variable=self.player_guess, value='equal', command=self.game_play)
        equal_button.grid(row=4, column=2, sticky=tk.NSEW)

        #greater_button = ttk.Button(self, text='Greater', command=self.run)
        #greater_button.grid(row=3, column=3, sticky=tk.NSEW)
        greater_button = ttk.Radiobutton(self, text='Greater', variable=self.player_guess, value='greater', command=self.game_play)
        greater_button.grid(row=4, column=3, sticky=tk.NSEW)


        # Pop up window for the rules
        rules_button = ttk.Button(self, text='Rules', command=self.show_rules)
        rules_button.grid(row=5, column=4, sticky=tk.NSEW)

        # Close button 
        close_button = ttk.Button(self, text='Quit', command=self.__close)
        close_button.grid(row=6, column=4, sticky=tk.NSEW)

    def check_game_state(self):
        '''
        function to check whether to start new game session or continue an old one
        '''

        print(self.player_information)
        
        # in case player lost the game last time game, points being 0 then
        if self.player_information[6] == None or self.player_information[6] <= 0:   
            self.restart()
        
        # in case user was left with some points when player closed the game
        elif ( self.player_information[6]  > 0):
            
            # ask to start new session or continue with an old one
            return_box = tk.messagebox.askquestion('Start playing', 'Would you like to continue with old session [YES] or start a new?[NO]')
            if return_box == 'yes':
                self.player_points = self.player_information[6]
                print(f"player_points are now {self.player_points}")
            else:
                self.restart()





    # End of user code
    def throw(self):
        # Start of user code protected zone for throw function body

        dice_dots = {1: '\u2680', 2: '\u2681', 3: '\u2682', 4: '\u2683', 5: '\u2684', 6: '\u2685'}
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.both_dice = (self.dice1, self.dice2)
        
        self.dice_label.configure(text=f'{dice_dots[self.dice1]}  {dice_dots[self.dice2]}')
        self.dice_label.grid()
        
        return self.both_dice
        # End of user code
    def points_label_change(self):
        # Start of user code protected zone for points_label_change function body
        self.points_label.configure(text=f"Points: {self.player_points}")
        self.points_label.grid()
        # End of user code

    def bet(self):
        # Start of user code protected zone for bet function body
        self.bet_value = self.points_slider.get()

        try:
            not (1 <= int(self.bet_value) <= 100)
            if (int(self.bet_value) > self.player_points):
                ttk.tkinter.messagebox.showinfo(title="Bet value ", message="You can't bet more than your balance!") 
                raise ValueError 
        except ValueError:
            ttk.tkinter.messagebox.showinfo(title="Wrong type or Wrong Interval!", message="Please place a bet between 1 and 100 points")
        else:
            self.bet_value = int(self.bet_value)
            ttk.tkinter.messagebox.showinfo(title="Less, Equal or Greater", message=f"Now you should click one of the options below\n'Less, Equal or Greater'")
        print(self.bet_value)
        return self.bet_value

        # End of user code

    def sum(self):
        # Start of user code protected zone for sum function body
        self.dice_sum = self.both_dice[0] + self.both_dice[1]
        return self.dice_sum
        # End of user code

    def result(self):
        self.bet_value = int(self.points_slider.get())
        # Start of user code protected zone for result function body
        if self.dice_sum == 7:
            if self.player_guess.get() == 'equal':
                self.game_round_result = "You win!"
                self.win = True
                self.player_points += (self.bet_value * 1000 - self.bet_value)
                
            else:
                self.game_round_result = "You lose!"
                self.win = False
                self.player_points -= (self.bet_value * 10 + self.bet_value)

        elif self.dice_sum < 7:
            if self.player_guess.get() == 'less':
                self.game_round_result = "You win!"
                self.win = True
                self.player_points += (self.bet_value * 100 - self.bet_value)

            else:
                self.game_round_result = "You lose!"
                self.win = False
                self.player_points -= (self.bet_value * 10 + self.bet_value)

        elif self.dice_sum > 7:
            if self.player_guess.get() == 'greater':
                self.game_round_result = "You win!"
                self.win = True
                self.player_points += (self.bet_value * 100 - self.bet_value)
            else:
                self.game_round_result = "You lose!"
                self.win = False
                self.player_points -= (self.bet_value * 10 + self.bet_value)
        
        return self.win
        # End of user code

    def restart(self):
        # Start of user code protected zone for restart function body
        self.dice1 = 0
        self.dice2 = 0
        self.both_dice = (self.dice1, self.dice2)
        self.dice_sum = 0
        self.bet_value = 0
        self.player_guess = tk.StringVar()
        self.player_points = self.initial_points


        # End of user code

    def game_play(self):
        self.throw() # returns game.both_dice --> tuple (dice1, dice2)
        self.sum() # returns the sum of the dices --> int value
        self.result()
        self.result_label.configure(text=f"{self.game_round_result}")
        self.result_label.grid()
        self.points_label_change()
        self.update()
        if self.player_points <= 0:

            # save player points to database
            self.database.add_double_dice_score(self.player_points, self.player_info)

            msg_box = messagebox.showinfo('Info screen', message=f"Your overall points are negative now. We're setting points back to 0.")
            exit_box = tk.messagebox.askquestion('Exit Application', 'Would you like to play again?')
            if exit_box == 'yes':
                tk.messagebox.showinfo('Info screen', 'You will now return back to the game and you can place a new bet. Good luck!')
                self.restart()
                self.points_label_change()
            else:

                # save player points to database
                self.database.add_double_dice_score(self.player_points, self.player_info)

                self.parent.destroy()
    
    def __close(self):
        '''asking if closing is intended'''
        if messagebox.askyesno("Close", "Do you want to close the Double Dice game?"):
            
            # update current points to database upon closing the game
            self.database.add_double_dice_score(self.player_points, self.player_info)
            self.database.see_database()
            
            self.parent.destroy()

    def show_rules(self):
        """Shows the rules of the game"""
        rules = ttk.tkinter.messagebox.showinfo(title="Rules", message=self.rules)
        return rules
        
    # Start of user code -> methods for DoubleDice class

    # End of user code

if __name__ == "__main__":
    app = DoubleDice()
    app.mainloop()

# Start of user code -> functions/methods for minigames lab1 Double dice package

# End of user code


# File       :  fivedice.py
# Authors    :  Sebastian Sopola, Uras Ayanoglu, Jerry Karkainen
# Description:  This is game where you play with 5 dices
# --------------------------------------------------------------------------------------------------------------------------------------

# Import necessary libraries.
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image,ImageTk
from pathlib import Path
from random import randint
from minigames.game_components import GamePlay, Player
from minigames.playerdatabase import UserDataBase
# --------------------------------------------------------------------------------------------------------------------------------------

class FiveDice(tk.Frame, GamePlay, Player):
    def __init__(self, parent, player_info):
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()

        '''initializes Window's attributes'''
        super().__init__(master=parent)
        self.parent = parent
        self.title = "5-Dice"
        self.dice_faces = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        self.bet_value = 0
        self.player_points = 100
        self.dice = [0, 0, 0, 0, 0]
        self.matching_faces = 0
        self.initial_pot = 0

        # current user playing the game
        self.player_info = player_info

        # database object
        self.database = UserDataBase()  

        # player information of current user
        self.player_information = self.database.find_player(self.player_info)

        # function to determine does game open new session or run old if it was not finished
        self.check_game_state()


        self.rules = """
        5-Dice Game Rules:

        5-Dice, is a game that is played with 5 dices. Player starts the game with 100 points.
        At the beginning of the game, the player needs to place their bet which is always between 1 and 100 points.
        Then five dice are thrown and game will check how many of the dice have the same faces. 
 
        1. If 2 same faces come, player wins 2 * the bet s/he placed,
        2. If 3 same faces come, player wins 30 * the bet s/he placed, 
        3. If 4 same faces come, player wins 400 * the bet s/he placed,
        4. If all of the dice have same faces, player wins 5000 * the bet s/he placed.

        - Overall points for the game cannot be negative and in case this happens the points are set to zero. 
        And the game ends.
        - If the player wants to continue playing, they can restart the game by pressing the restart button.
        - If the player wants to quit the game, they can press the quit button.
        - The points are saved for each game. 
        """

        
        game_label = ttk.Label(self, text=self.title, font=("Helvetica", 40))
        game_label.grid(row=0, column=0, sticky=tk.NSEW)


        # Text box for bet amount
        bet_label = ttk.Label(self, text='Your Bet:')
        bet_label.grid(row=3, column=0, sticky=tk.E)
        self.bet_entry = ttk.Entry(self, width=10)
        self.bet_entry.grid(row=3, column=1, sticky=tk.NSEW)

        # Player Points Label
        self.points_label = ttk.Label(self, text=f"Points: {self.player_points}")
        self.points_label.grid(row=0, column=7, sticky=tk.NE)
        
        # dice frame
        dice_label_frame = ttk.LabelFrame(self)
        self.dice_labels = []
        for i in range(5):
            dice_label = ttk.Label(dice_label_frame, font=("Helvetica", 100))
            dice_label.pack(side=tk.LEFT)
            self.dice_labels.append(dice_label)
        dice_label_frame.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW)

        self.winning_label = ttk.Label(self, text="", font=("Helvetica 20"))
        self.winning_label.grid(row=2, column=0, sticky=tk.NSEW)
    

        # Buttons for betting and continuing the game

        bet_button = ttk.Button(self, text="Bet", command=self.game_play)
        bet_button.grid(row=4, column=0,sticky=tk.NSEW)

        #continue_button = ttk.Button(self, text="Continue")
        #continue_button.grid(row=4, column=1, sticky=tk.NSEW)

        # Pop up window for the rules
        rules_button = ttk.Button(self, text='Rules', command=self.show_rules)
        rules_button.grid(row=5, column=4, sticky=tk.NSEW)
        
        # Quit button
        close_button = ttk.Button(self, text='Quit', command=self.__close)
        close_button.grid(row=6, column=4, sticky=tk.NSEW)

    def check_game_state(self):
        '''
        function to check whether to start new game session or continue an old one
        '''

        print(self.player_information)
        
        # in case player lost the game last time game, points being 0 then
        if self.player_information[7] == None or self.player_information[7] <= 0:   
            self.player_points = 100
            self.points_label = ttk.Label(self, text=f"Points: {self.player_points}")
            self.points_label.grid(row=0, column=7, sticky=tk.NE)
            
        
        # in case user was left with some points when player closed the game
        elif ( self.player_information[7]  > 0):
            
            # ask to start new session or continue with an old one
            return_box = tk.messagebox.askquestion('Start playing', 'Would you like to continue with old session [YES] or start a new?[NO]')
            if return_box == 'yes':
                self.player_points = self.player_information[7]
                print(f"player_points are now {self.player_points}")
            else:
                self.player_points = 100
                self.points_label = ttk.Label(self, text=f"Points: {self.player_points}")
                self.points_label.grid(row=0, column=7, sticky=tk.NE)
                



        

    def throw(self):
        for i in range(0, len(self.dice)):
            self.dice[i] = self.dice_faces[randint(0, 5)]
        self.update_dice_labels()

    def game_play(self):

        self.bet_value = self.bet_entry.get()

        if not (self.bet_value.strip().isnumeric() and 1 <= int(self.bet_value.strip()) <= 100):

            # save player points to database
            self.database.add_five_dice_score(self.player_points, self.player_info)

            ttk.tkinter.messagebox.showinfo(title="Wrong input ", message="Please use just a numbers\nand place a bet between 1-100")
        elif int(self.bet_value) > self.player_points:

            # save player points to database
            self.database.add_five_dice_score(self.player_points, self.player_info)

            ttk.tkinter.messagebox.showinfo(title="Bet value ", message="You can't bet more than your balance!")
        else:

            # save player points to database
            self.database.add_five_dice_score(self.player_points, self.player_info)

            self.throw()
            self.match()
            self.calc_points()
            self.change_points()
            if self.player_points == 0:
                self.restart()
        
        

    
    def match(self):
        self.matching_faces = 0
        for item in self.dice:
            if self.dice.count(item) > self.matching_faces:
                self.matching_faces = self.dice.count(item)
            else:
                continue
        return self.matching_faces


    def calc_points(self):
        self.initial_pot = 0
        match self.matching_faces:
            case 1:
                self.initial_pot -= int(self.bet_value)
            case 2:
                self.initial_pot = 2*int(self.bet_value)
            case 3:
                self.initial_pot = 30*int(self.bet_value)
            case 4:
                self.initial_pot = 400*int(self.bet_value)
            case 5:
                self.initial_pot = 5000*int(self.bet_value)
        return self.initial_pot

    def change_points(self):
        if self.initial_pot < 0:   
            self.winning_label.config(text = f"You lost {abs(self.initial_pot)} points!")
            self.player_points += self.initial_pot
            self.points_label.config(text = f"Points: {self.player_points}")
        else:
            self.winning_label.config(text = f"You won {self.initial_pot} points!")
            self.player_points += self.initial_pot - int(self.bet_value)
            self.points_label.config(text = f"Points: {self.player_points}")

    def restart(self):
        if messagebox.askyesno("Restart", "You dont have points anymore\nDo you want to play again?"):
            self.player_points = 100
            self.points_label.config(text = f"Points: {self.player_points}")
            
        else:
            self.parent.destroy()

    def __close(self):
        '''asking if closing is intended'''
        if messagebox.askyesno("Close", "Do you want to close the Five Dice game?"):

            # update current points to database upon closing the game
            self.database.add_five_dice_score(self.player_points,self.player_info)  # where to put this and what is the score
            self.database.see_database()

            self.parent.destroy()

    def show_rules(self):
        rules = ttk.tkinter.messagebox.showinfo(title="Rules", message=self.rules)
        return rules

    def update_dice_labels(self):
        for i in range(5):
            self.dice_labels[i].config(text=str(self.dice[i]), foreground="black")




if __name__ == "__main__":
    app = FiveDice()
    app.mainloop()


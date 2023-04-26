from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image,ImageTk
from pathlib import Path
import random
from minigames.game_components import GamePlay, Player
from minigames.playerdatabase import UserDataBase


class GuessTheNumber(tk.Frame, GamePlay):
    '''
    Game used to guess a number or numbers from a given set of numbers
    e.g. guess one number between 1..9 or bet if a sum of two dices is less, equsl or bigger than 7
    generated numbers can be unique or not.
    '''
    def __init__(self, parent, player_info):
        '''
        parameters:
            title : str, the name of the game
            numrange : range e.g. range(0, 10)
            numofnums : int, how many numbers are generated
            unique: bool, are the generated numbers unique
        '''
        '''initializes Window's attributes'''
        self.close_screen = parent
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        super().__init__(master=parent)
        self.parent = parent
        self.title = "Guess the Number"
        game_rules = messagebox.showinfo('Rules', message="Guess a number between 0 and 100")
        self.numrange = range(0,101)
        self.unique = True        
        self.numofnums = 1
        self.__magic = random.choices(self.numrange, k=self.numofnums) #@ver3 sample changed to choice allowing generation eith replacement
        self.__magic = random.choices(self.numrange, k=self.numofnums)        
        self.guesses = {'correct':set(), 'wrong':set()} # all the guesses, wrong and correct

        # current user playing the game
        self.player_info = player_info

        # database object
        self.database = UserDataBase()  

        # player information of current user
        self.player_information = self.database.find_player(self.player_info)

        # function to determine does game open new session or run old if it was not finished
        self.check_game_state()


        self.rules = """
        Guess the Number Game Rules:
        
        - Guess the Number, is a game that is played with a number between 0 and 100.   
        At the beginning of the game, a number is generated but is not shown to the player.
        After the number is generated, the player needs to enter a number to guess the generated number.

        - If the player's guess is greater than the generated number, s/he will get a hint as Too high!,
        and the player needs to enter another number to guess the generated number based on the information given.

        - If the player's guess is less than the generated number, s/he will get a hint as Too low!, 
        and the player needs to enter another number to guess the generated number based on the information given.

        - If the player's guess is equal to the generated number, s/he will get a message stating that:
        Player's guess (the number s/he entered) is correct, and the player guessed it with only n amount of guesses.
        The game ends.

        - If the player wants to continue to play the game, s/he can click on the Restart button to restart the game.
        The game will generate a new number and the player can start to guess the new number.

        """
        
        # Create text label for the game
        game_label = ttk.Label(self, text=self.title, font=("Helvetica", 40))
        game_label.grid(row=0, column=0, columnspan=5, sticky=tk.NSEW)

        # Closing the game button
        close_button = ttk.Button(self, text='Quit', command=self.__close)
        close_button.grid(row=5, column=4, sticky=tk.NSEW)


        # Text box for guessing the number
        guess_label = ttk.Label(self, text='Your Guess:')
        guess_label.grid(row=2, column=0, sticky=tk.NSEW)
        self.guess_entry = ttk.Spinbox(self, from_=1, to=100) #ttk.Entry(self, width=10)
        self.guess_entry.grid(row=2, column=1, sticky=tk.NSEW)

        # Pop up window for the rules
        rules_button = ttk.Button(self, text='Rules', command=self.show_rules)
        rules_button.grid(row=4, column=4, sticky=tk.NSEW)

        # Create enter button to chech input of textbox
        enter_button = ttk.Button(self, text="Enter", command=self.game_play)
        enter_button.grid(row=2, column=2, sticky=tk.NSEW)

    @property
    def magic(self):
        return self.__magic

    @magic.setter
    def magic(self, value):
        raise ValueError('magic can not be set')
       
    @property
    def numofnums(self)->int:
        return self.__numofnums
    
    @numofnums.setter
    def numofnums(self, num:int)->None:
        print(num, len(self.numrange))
        if self.unique and 1 <= num < len(self.numrange):
            self.__numofnums = num
        elif not self.unique:
            self.__numofnums = num
        else:
            raise ValueError('the number of numbers to generate < range and > 0')
        

    def check_game_state(self):
        '''
        function to check whether to start new game session or continue an old one
        '''
        print(self.player_information)
        
        # in case player did not finish the game
        if self.player_information[3] == 0:
            self.magic[0] = self.player_information[4]                                              # original number to be guessed
            self.guesses = {'correct': set(), 'wrong': set(range(self.player_information[5]-1))}    # original amounts of attempts
            

        # in case player did finish the game
        else:
            self.restart()




    
    def check(self, num:int)->bool:
        '''
        checks if the num is in correct numbers
        
        parameters:
            num: int, integer user guessed
            
        return:
            bool, True if numofnums > 1 and guess is in magic  or
                    num < magic[0] if numofnums = 1
            
        '''
        if num in self.__magic:
            self.guesses['correct'].add(num)
            return True
        else:
            self.guesses['wrong'].add(num)
            return False


    def checksum(self, num):
        '''
        returns the result of sustraction
        of sum of magic numbers and given numner
        '''

        return sum(self.__magic) - num                       
    
    def isover(self):
        '''
        Checks if the game is over
        return:
            True if all the numbers are correctly guessed
        '''
        return self.guesses['correct'] == set(self.__magic)
    
    def restart(self) -> None:
        '''
        re-initializes the game to start a new
        '''
        self.__magic = random.sample(self.numrange, self.numofnums)  
        self.guesses = {'correct':set(), 'wrong':set()} # all the guesses, wrong and correct

    def __close(self):
        '''asking if closing is intended'''
        if messagebox.askyesno("Close", "Do you want to close the Guess The Number game?"):

            # add the number to be guessed 
            self.database.add_guess_the_number_score(self.magic[0],self.player_info)

            # add the number of attempts user has made
            self.database.add_guess_the_number_player_attempts(len(self.guesses['correct'])+len(self.guesses['wrong']), self.player_info)

            # store 1 ( True ) for current game state because player guess was correct 
            self.database.add_guess_the_number_game_state(0,self.player_info)

            # see database immidiately after to cofirm correct save
            self.database.see_database()

            # destroy game window
            self.parent.destroy()

    def show_rules(self):
        rules = ttk.tkinter.messagebox.showinfo(title="Rules", message=self.rules)
        return rules
    
    
    """ User guesses random generated number """
    def game_play(self):
        self.player_guess = int(self.guess_entry.get())
        self.game_result = self.check(self.player_guess)
        if ( self.game_result == True ):

            # add the number to be guessed 
            self.database.add_guess_the_number_score(self.magic[0],self.player_info)

            # add the number of attempts user has made
            self.database.add_guess_the_number_player_attempts(len(self.guesses['correct']) + len(self.guesses['wrong']), self.player_info)

            # store 1 ( True ) for current game state because player guess was correct 
            self.database.add_guess_the_number_game_state(1,self.player_info)

            # see database immidiately after to cofirm correct save
            self.database.see_database()     


            msg_box = messagebox.showinfo('Info screen', message=f"You guess it right! ({self.player_guess}) with only {len(self.guesses['correct']) + len(self.guesses['wrong'])} guesses!")
            exit_box = tk.messagebox.askquestion('Exit Application', 'Would you like to play again?')
            if exit_box == 'yes':
                tk.messagebox.showinfo('Info screen', 'You will now return to the game and you can guess new number. Good luck!')
                self.restart()
            else:
                self.close_screen.destroy()
        elif ( self.game_result != True and  int(self.player_guess) > self.magic[0] ):

            # add the number to be guessed 
            self.database.add_guess_the_number_score(self.magic[0],self.player_info)

            # add the number of attempts user has made
            self.database.add_guess_the_number_player_attempts(len(self.guesses['correct']) + len(self.guesses['wrong']), self.player_info)

            # store 1 ( True ) for current game state because player guess was correct 
            self.database.add_guess_the_number_game_state(0,self.player_info)

            # see database immidiately after to cofirm correct save
            self.database.see_database() 

            messagebox.showinfo('Info Screen', message="Too high!")
        elif ( self.game_result != True and  int(self.player_guess) < self.magic[0] ):

            # add the number to be guessed 
            self.database.add_guess_the_number_score(self.magic[0],self.player_info)

            # add the number of attempts user has made
            self.database.add_guess_the_number_player_attempts(len(self.guesses['correct']) + len(self.guesses['wrong']), self.player_info)

            # store 1 ( True ) for current game state because player guess was correct 
            self.database.add_guess_the_number_game_state(0,self.player_info)

            # see database immidiately after to cofirm correct save
            self.database.see_database()

            messagebox.showinfo('Info Screen', message="Too low!")


if __name__ == "__main__":
    app = GuessTheNumber()
    app.mainloop()
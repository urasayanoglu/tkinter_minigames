from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk #basic Tk widgets are overridden
from tkinter import simpledialog
from PIL import Image,ImageTk
from pathlib import Path
from datetime import date 




from minigames.doubledice import DoubleDice
from minigames.fivedice import FiveDice
from minigames.guessthenumber import GuessTheNumber
from minigames.guesstheday import GuessTheDay
from minigames.game_components import Player
from minigames.playerdatabase import UserDataBase

#  import the module (folder e.g. src) your frames are in
#  and from the module import the frame class 
#  e.g. only.py in src module is imported
#  from src.only import Only
   
class AppWithWindows(tk.Tk):
    '''
        tkinter window that demostrates how to
        - create and show other windows
    '''
    mode = False
    frames = 'Guess The Day', 'Five Dice', 'Double Dice', 'Guess The Number'

  
    

    def __init__(self):
        super().__init__()

        #  root window, 
        self.title('MiniGames version 1.4')

        #  window size
        self.geometry("%dx%d" % (self.winfo_screenwidth()*1//2,\
                                 self.winfo_screenheight()*1//2))        

        #  bind closing from the cross to closing method
        self.protocol('WM_DELETE_WINDOW', self.__close)

        label = ttk.Label(self, text="Mini Games", font=("Helvetica", 40))
        label.grid(row=0, column=0, columnspan=5)

        # today's sate variable to determine is user allowed to play today or not
        self.today = date.today()
        
        self.player_info = None
        self.database = UserDataBase()
        self.database.create_database()

        # create a pop up window to ask for player name
        self.__createLayout()
        self.player_login()

    # register a player
    def player_login(self):
            
        self.player_info = simpledialog.askstring("Input", "Welcome to MiniGames. Please enter your name.")

        while self.player_info == "" or self.player_info == None:
            self.player_info = simpledialog.askstring("Input", "Welcome to MiniGames. Please enter your name.")

        else:
            messagebox.showinfo(title='Welcome', message=f'Hi, Welcome {self.player_info}')
            self.database.add_player(self.player_info, None, date.today(),None,None,None,None,None)
            current_player = Player() # I keep this just in case we need to have a player class used in the game!
            current_player.player_name = self.player_info
            self.database.see_database()

                
    def __close(self, e=None):
        '''asking if closing is intended'''
        if messagebox.askyesno("Close", "Do you want to close the program?"):
            self.destroy()
            

    def __createLayout(self):
        '''
        draws UI items that are visible all the time
        - menubar
        - menu with buttons (row 0)
        '''
        #  create menubar with menus File and Select frame 
        self.menubar = tk.Menu(self)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Close game", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label='Close', command=self.__close)

        framemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Select game", menu=framemenu)
        for i, item in enumerate(AppWithWindows.frames):                        
            framemenu.add_command(label=item, command=lambda i=i+1: self.select(i))    # i=1+1 is my modification..... previusly i=i                                        

        self.config(menu=self.menubar)
        
        #  create menu with buttons to the upper part of the window    
        upperframe = ttk.Frame(self) 
        for i, item in enumerate(AppWithWindows.frames):
            ttk.Button(upperframe, text=item, command=lambda i=i+1: self.select(i)).grid(row=i, column=0, padx=10, pady=3, sticky=tk.NSEW)   # i=1+1 is my modification
        upperframe.grid(row=2, column=0, columnspan=5, sticky=tk.N )                                                                         # previusly i=i
        self.columnconfigure(0, weight=1) 

        lowerframe = ttk.Frame(self)
        ttk.Button(lowerframe, text='Quit', command=self.__close).grid(row=0, column=0, padx=10, pady=3, sticky=tk.E)
        lowerframe.grid(row=3, column=4, columnspan=5, sticky=tk.E)

   
		
    #  self.select()
              
    def __home(self, parent):
        '''
        creates "empty" frame
        '''
        f = ttk.Frame(parent)
        # Display image on a Label widget as background
        self.img = ImageTk.PhotoImage(Image.open('frames/5SRYZ.png').resize((parent.winfo_width()*3//5,\
                                                                      parent.winfo_height()*4//5)))
        label = ttk.Label(f, image=self.img)
        label.grid(row=0, column=0, sticky=tk.NSEW)
        return f
        
    def select(self, selection=0):
        '''
        menu and button selection, which window to show
        '''
        window = tk.Toplevel(self)
        window.geometry("%dx%d" % (self.winfo_screenwidth()*3//5,\
                                 self.winfo_screenheight()*3//5))
        window.update()
        match selection:
            case 1:
                '''
                Decision formula to decide has player clearance to play GuessTheDay today or not
                '''
                pelaaja = self.database.find_player(self.player_info)

                # Check has player played at all, if not: play
                if ( pelaaja[1] is None ):
                    home = GuessTheDay(window, self.player_info, status=True)   
                    window.title('Guess The Day')
                    
                # check has player played, if yes and date played is today's date: don't allow game play 
                elif ( pelaaja[1] is not None and self.today.strftime("%Y-%m-%d") == pelaaja[2] ):
                    messagebox.showinfo('Info','You have allready reached the number of games per day(1 pc)')
                    home = GuessTheDay(window, self.player_info, status=False)
                    window.title('Guess The Day')

                # in case player has played and date played is not today's date: play
                else:
                     home = GuessTheDay(window, self.player_info, status=True)
                     window.title('Guess The Day')
                
            case  2:
                # pass current user to FiveDice game object
                home = FiveDice(window, self.player_info)
                window.title('Five Dice')
            case  3:
                # pass current user to DoubleDice game object
                home = DoubleDice(window, self.player_info)
                window.title('Double Dice')
            case  4:
                # pass current user to GuessTheNumber game object 
                home = GuessTheNumber(window, self.player_info)
                window.title('Guess The Number')
            case _:
                home = self.__home(window)

        
        home.pack(expand=True)
        home.grab_set() # grab the focus to the new window from the main window    

if __name__ == "__main__":
    app = AppWithWindows()
    app.mainloop()
    

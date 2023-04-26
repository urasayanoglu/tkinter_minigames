# File: playerdatabase.py
# Author(s): Sebastian Sopola, Uras, Jerry Kärkäinen
# Description: This file is sqlite3 database for games' collection and has functionality for adding userdata including name and game data. Create database. Add new player and see if player exists in the database

import sqlite3

class UserDataBase(object):
    '''
    class UserDataBase to store user name and game data. You can create database. Add new player and see if player exists in the database
    '''
    def __init__(self) -> None:
        # nothing to add here, we only want to use this
        pass

   
    def create_database(self):
        '''
        function to create the database
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                (name TEXT UNIQUE, score INT, day DATE, GTN_state INT, GTN_score INT,GTN_attempts INT, DD_score INT, FV_score INT)''')                            
            connection.commit()


  
    def add_player(self,name,score,day,GTN_state,GTN_score,GTN_attempts,DD_score,FV_score):                                                                    
        '''
        function to add a new player to the database
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            # in case player appears in the database, continue without actions and no duplicates are created
            try:
                cursor.execute('''INSERT INTO players (name,score,day,GTN_state,GTN_score,GTN_attempts,DD_score,FV_score) values(?,?,?,?,?,?,?,?)''',
                                                                                             (name,score,day,GTN_state,GTN_score,GTN_attempts,DD_score,FV_score))       
                connection.commit() 
                
            except:
                pass



    def find_player(self, name):
        '''
        function to check and output if some specific player is in the database
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM players WHERE name=?",(name,))
            # fetch the results and print them
            result = cursor.fetchone()

        if result:
            return result 
      
    def clean_database(self):
        '''
        function to swipe clean database when wanted to
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS players''')
            connection.commit()

    def see_database(self):
        '''
        function to print out entire database
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM players''')

            result  = cursor.fetchall()
            print(result)


    def add_score(self,score,day,name):
        '''
        function to add player score
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set score=?, day=? WHERE name=?''',(score,day,name))
            connection.commit()

    def add_guess_the_number_score(self, score,name):
        '''
        function to add guess the number score
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set GTN_score=? WHERE name=?''',(score,name) )
            connection.commit()


    def add_guess_the_number_game_state(self,game_state,name):
        '''
        function to update game state of Guess The number for current user
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set GTN_state=? WHERE name=?''',(game_state,name))
            connection.commit()

    def add_guess_the_number_player_attempts(self,player_attempts,name):
        '''
        function to add player attempts to database
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set GTN_attempts=? WHERE name=?''',(player_attempts,name))
            connection.commit()

    
    def add_double_dice_score(self,score,name):
        '''
        function to add final double dice score
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set DD_score=? WHERE name=?''',(score,name))
            connection.commit()

    def add_five_dice_score(self,score,name):
        '''
        function to add final five dice score
        '''
        with sqlite3.connect('gamedata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE players set FV_score=? WHERE name=?''',(score,name))
            connection.commit()
    



""" TEST CODES TO CHECK DATABASE FUNCTIONALITY """

"""
databaseObject = UserDataBase()
databaseObject.create_database()       


# get player name + add player to database
#player_name = input("Enter player name: ")
#databaseObject.add_player(player_name, 20)

# see what's inside database
#databaseObject.find_player(player_name, 30)

# print out entire database
#databaseObject.see_database()

# clear entire database
databaseObject.clean_database()

# create database again
databaseObject.create_database()

# print out again entire database
databaseObject.see_database()
"""





















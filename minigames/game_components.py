from abc import ABC, abstractmethod

class GamePlay(ABC):
    """Abstract class for game play"""

    @abstractmethod
    def game_play(self):
        pass

    @abstractmethod
    def restart(self):
        pass

   
    
class Player:
    """A basic player class for minigames"""

    player_count = 0

    def __init__(self, player_name=None):
        self.player_name = player_name
        self.player_points = 0
        self.player_count += 1
        self.player_id = self.player_count + 1


    

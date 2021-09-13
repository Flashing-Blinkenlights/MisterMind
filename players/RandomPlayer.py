from . import Player

from random import shuffle
from random import choice

class RandomPlayer(Player):
    """
        Returns a random combination
    """

    def turn(self, state):
        if self.singles: return(shuffle(self.colours)[:self.pins])
        else:   return(tuple([choice(self.colours) for i in range(self.pins)]))

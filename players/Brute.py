from . import Player

from random import shuffle

class Brute(Player):
    """
        Greedily finds the self.colours, then randomises
    """

    def newGame(self, colours, pins, rounds, singles, mode):
        super().newGame(colours, pins, rounds, singles, mode)

        self.counter = 0
        self.change = 0

    def turn(self, state):
        return(tuple(self.deduct(state)))

    def deduct(self, state):

        if len(state) > 0 and self.counter < self.pins:
            self.counter += state[-1][1][0]

        if self.counter < self.pins:
            return self.pins*[self.colours[len(state)]]
        elif self.change == 0: self.change = len(state)

        pool = []

        for turn in state[:self.change]:
            if turn[1][0] > 0:
                pool += turn[1][0]*[turn[0][0]]

        for turn in state:
            if pool == list(turn[0]):
                shuffle(pool)

        ## TODO: Improve efficiency

        return pool

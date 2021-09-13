from os import scandir

class Player():
    """
        Receives current state of game and returns play for state
    """

    def __init__(self, name, pcolour, presenter):

        self.name = name
        self.presenter = presenter(pcolour)
        self.colours = []
        self.pins = 0
        self.rounds = 0
        self.singles = False
        self.mode = "casual"

    def newGame(self, colours, pins, rounds, singles, mode):
        self.colours = colours
        self.pins = pins
        self.rounds = rounds
        self.singles = singles
        self.mode = mode

    def turn(self, state):
        self.presenter.printboard(state, self.pins, self.rounds)
        return(self.presenter.choice(self.name, len(state), self.colours))

    def warn(self, msg):
        self.presenter.warn(self.name, msg)

    def show(self, state):
        self.presenter.printboard(state, self.pins, self.rounds)

__all__ = []
with scandir("/".join(__file__.split("/")[:-1])) as dirs:
    for entry in dirs:
        if entry.name[-3:] == ".py" and entry.name not in __file__:
	           __all__.append(entry.name[:-3])

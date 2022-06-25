from players import Player
from players import *
from presenters import BasePresenter
from presenters import *
from random import choice as choose

COLOURS = ["r", "o", "y", "g", "b"]

class RefereeWarning(Exception):
    def __init__(self, message):
        super().__init__("\n\nGame aborted:\n" + message)

class Referee():

    def __init__(self, colours, pins, rounds, players):

        self.__solution = []
        self.colours = colours
        self.pins = pins
        self.rounds = rounds

        self.singles = False    # only one of each colour permitted
        self.mode = "casual"    # casual, race, elimination

        self.players = {}
        self.ranking = []

        self.safeMode = False

        for player in players:
            if isinstance(player, Player):
                self.players[player] = [[], None]   # True = wins, False = loses
            else:
                msg = "You have been disqualified for not inheriting the Player class."
                try:
                    player.warn(msg)
                except: pass
                if self.safeMode: raise RefereeWarning(str(type(player)) + ": " + msg)

    def setSafeMode(self, state): self.safeMode = state

    def newGame(self):
        self.__solution = tuple([choose(self.colours) for i in range(self.pins)])
        for player, state in self.players.items():
            self.players[player] = [[], None]
            player.newGame(self.colours, self.pins, self.rounds, self.singles, self.mode)

    def setRules(self, colours, pins, rounds, singles=False, mode="casual"):
        self.pins = pins
        self.rounds = rounds
        self.singles = singles
        self.mode = mode

    def game(self, games=1):
        for game in range(games):
            self.newGame()
            for round in range(self.rounds):
                for player, status in self.players.items():
                    if status[1] == None:
                        guess = player.turn(status[0])

                        if len(guess) != self.pins:
                            msg = "Expected {} pins, received {}!".format(self.pins, len(guess))
                            player.warn(msg)
                            if self.safeMode: raise RefereeWarning(player.name + ": " + msg)
                            if len(guess) > self.pins:
                                guess = guess[:self.pins]
                        for pin in guess:
                            if pin not in self.colours:
                                msg = "Colour '{}' is not supported!\n".format(pin)
                                player.warn(msg)
                                if self.safeMode: raise RefereeWarning(player.name + ": " + msg)

                        score = self.check(player, guess)
                        if score[0] == self.pins:
                            status[1] = True
                            self.ranking.append((round+1, player.name))
                        status[0].append((guess, score))
            self.ranking.sort()
            for stats in self.ranking:
                print("\t{} rounds: {}".format(stats[1], stats[0]))
            for player, stats in self.players.items():
                player.show(stats[0])
                if stats[1]: player.warn("You won in " + str(len(stats[0])) + " rounds!")
                else: player.warn("You ran out of turns. Better luck next time!")


    def check(self, player, guess):
        guess = list(guess)
        score = [0, 0]  # blacks, whites
        win = None
        solution = list(self.__solution)

        for position, pin in enumerate(guess):
            if pin == solution[position]:
                score[0] += 1
                guess[position] = "*"
                solution[position] = "°"
        for position, pin in enumerate(guess):
            if pin in solution:
                score[1] += 1
                solution[solution.index(pin)] = "°"
                guess[position] = "*"

        return tuple(score)



if __name__ == "__main__":

    playerclasses = [Player] + Player.__subclasses__()

    presenter = TPresenter.TPresenter("black")

    try:
        players = []
        # for player in playerclasses:
        #     players += [player(player.__name__,
        #                  choose(list(presenter.TCOLOURS.keys())),
        #                  TPresenter.TPresenter)]


        while True:
            name = input("Player name:\t")
            colour = input("Player colour:\t")
            players += [Player(name, colour, TPresenter.TPresenter)]
            if input("Add another player? (y/n) > ").strip().lower()[:1] == "n":
                break

        referee = Referee(COLOURS, 4, 9, 2*players[:])

        while True:
            referee.game()
            if input("Play again? (y/n) > ").strip().lower()[:1] == "n":
                break
    except KeyboardInterrupt:
        pass

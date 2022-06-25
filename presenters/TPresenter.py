from . import BasePresenter
import os

class TPresenter(BasePresenter):
    """
        Displays information of the game in a terminal
    """

    def __init__(self, pcolour):
        self.pcolour = pcolour


        self.SYMBOLS = {"pin": ("■", "□", "×"),
                    "score": ("●", "○", "•"),
                    "filler": ("▁", "═", "▔")}

        self.DISPKEY = {"r": "red",
        "o": "orange",
        "y": "yellow",
        "g": "green",
        "b": "blue",
        "x": "black",
        "w": "white"}

        self.TCOLOURS = {"black":    "\033[§8;2;000;000;000m",    #or use framed character
                    "grey":     "\033[§8;2;128;128;128m",
                    "white":    "\033[§8;2;255;255;255m",
                    "pink":     "\033[§8;2;255;192;203m",
                    "red":      "\033[§8;2;255;000;000m",
                    "orange":   "\033[§8;2;255;165;000m",
                    "yellow":   "\033[§8;2;255;255;000m",
                    "darkgreen":"\033[§8;2;000;128;000m",
                    "green":    "\033[§8;2;000;255;000m",
                    "blue":     "\033[§8;2;135;206;235m",
                    "darkblue": "\033[§8;2;000;000;255m",
                    "magenta":  "\033[§8;2;255;000;255m",
                    "brown":    "\033[§8;2;139;069;019m",
                    "CLR":      "\033[0m"}  # § is replaced by 3(text) or 4(background)

    def choice(self, name, round, colours):

        palette = ""
        for colour in colours:
            colour = self.TCOLOURS[self.DISPKEY[colour]].replace("§", "3") + colour
            palette += colour
        palette += self.TCOLOURS["CLR"]

        prompt = self.TCOLOURS[self.pcolour].replace("§", "3") \
                + "\tRound {} for {}: > {}\n\t> ".format(round+1, name, palette)

        result = tuple("".join(input(prompt).lower().split()))
        os.system('cls' if os.name == 'nt' else 'clear')

        return result

    def printboard(self, state, pins, rounds):

        plays = [rounds*[0] for i in range(pins)]
        scores = [rounds*[0] for i in range(pins)]

        for x, row in enumerate(state):
            for y, pin in enumerate(row[0]):
                plays[y][x] = pin
            for y, pin in enumerate(scores):
                if row[1][0] > y:
                    pin[x] = "x"
                elif row[1][1] > y-row[1][0]:
                    pin[x] = "w"

        filler = self.TCOLOURS[self.pcolour].replace("§", "3") + " " + (2*rounds)*" "

        self.printrow(self.TCOLOURS["CLR"] + filler.replace(" ", self.SYMBOLS["filler"][0]))

        for row in plays:
            toprint = " "
            for pin in row:
                if pin == 0:
                    toprint += "b" + self.SYMBOLS["pin"][2] + " "
                else:
                    toprint += pin + self.SYMBOLS["pin"][0] + " "
            self.printrow(toprint)

        self.printrow(filler.replace(" ", self.SYMBOLS["filler"][1]))

        for row in scores:
            toprint = " "
            for pin in row:
                if pin == 0:
                    toprint += "b" + self.SYMBOLS["score"][2] + " "
                else:
                    toprint += pin + self.SYMBOLS["score"][0] + " "
            self.printrow(toprint)

        self.printrow(self.TCOLOURS["CLR"] + filler.replace(" ", self.SYMBOLS["filler"][2]))

    def printrow(self, mid):

        beg = "\t"+self.TCOLOURS["brown"].replace("§", "4")
        end = self.TCOLOURS["CLR"]

        for key, colour in self.DISPKEY.items():
            mid = mid.replace(key, self.TCOLOURS[colour]).replace("§", "3")

        print(beg + mid + end)

    def warn(self, name, msg):
        msg = (self.TCOLOURS[self.pcolour].replace("§", "3")
                + "\033[1m\t@" + name + ":\033[5m\t" + msg + "CLR")
        for key, colour in self.TCOLOURS.items():
            msg = msg.replace(key, colour)
        print(msg.replace("§", "3"))

import sys
import os
import random
import re

class Die(object):

    def __init__(self, sides=6):
        self.sides = sides
        self.__face = None

    def roll(self):
        self.__face = random.randint(1, 6)

    def clear(self):
        self.__face = None

    def get_face(self):
        return self.__face

    def __str__(self):
        if self.__face:
            return "Value: " + str(self.__face)
        else:
            return "Die not thrown"


class Hand(object):

    def __init__(self, dice=5, sides=6):
        self.dice = dice
        self.hand = []
        for x in range(dice):
            self.hand.append(Die(sides))
        
    def throw(self):
        print("\nRolling dice...")
        for die in self.hand:
            die.roll()

    def clear(self):
        for die in self.hand:
            die.clear()

    def re_roll(self):
        rolls = 0
        while rolls < 2:
            try:
                reroll = input("\n which dice do you want to re-roll "
                               "(keep camma for seperation or 'all'), or 0 to continue: ")

                if reroll.lower() == "all":
                    reroll = list(range(1, 6))
                else:

                    reroll = reroll.replace(" ", "")  
                    reroll = re.sub('[^0-9,]', '', reroll)  
                    reroll = reroll.split(",")  
                    reroll = list(map(int, reroll))  
            except ValueError:
                print("You entered something other than a number.")
                print("Please try again")
                continue

            if [x for x in reroll if x > self.dice]:
                print("You only have 5 dice!")
                continue

            if not reroll or 0 in reroll:
                break
            else:
                for i in reroll:
                    self.hand[i-1].roll()
                self.show_hand()
                rolls += 1

    def get_hand(self):
        faces = []
        for face in self.hand:
            faces.append(face.get_face())
        return faces

    def show_hand(self):
        for idx, val in enumerate(self.hand):
            print("die " + str(idx + 1) + " has value " + str(val.get_face()))


class Rules(object):

    def __init__(self):
        self.rules_map = {
            1: self.aces,
            2: self.twos,
            3: self.threes,
            4: self.fours,
            5: self.fives,
            6: self.sixes,
            7: self.three_of_a_kind,
            8: self.four_of_a_kind,
            9: self.full_house,
            10: self.small_straight,
            11: self.large_straight,
            12: self.yahtzee,
            13: self.chance,
        }

    def aces(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 1):
            sum += face
        return sum

    def twos(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 2):
            sum += face
        return sum

    def threes(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 3):
            sum += face
        return sum

    def fours(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 4):
            sum += face
        return sum

    def fives(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 5):
            sum += face
        return sum

    def sixes(self, hand):
        sum = 0
        for face in (x for x in hand.get_hand() if x == 6):
            sum += face
        return sum

    def three_of_a_kind(self, hand):
        for i in hand.get_hand():
            if hand.get_hand().count(i) >= 3:
                return sum(hand.get_hand())
        return 0

    def four_of_a_kind(self, hand):
        for i in hand.get_hand():
            if hand.get_hand().count(i) >= 4:
                return sum(hand.get_hand())
        return 0

    def full_house(self, hand):
        for i in hand.get_hand():
            x = hand.get_hand().count(i)
            if x == 3:
                for i in hand.get_hand():
                    y = hand.get_hand().count(i)
                    if y == 2 and x != y:
                        return 25
        return 0

    def small_straight(self, hand):
        hand = list(set(sorted(hand.get_hand())))
        try:
            if len(hand) >= 4:
                for idx, val in enumerate(hand):
                    if hand[idx+1] == val+1 and \
                        hand[idx+2] == val+2 and \
                        hand[idx+3] == val+3:
                        return 30
        except IndexError:
            pass
        return 0

    def large_straight(self, hand):
        hand = list(set(sorted(hand.get_hand())))
        try:
            if len(hand) >= 5:
                for idx, val in enumerate(hand):
                    if hand[idx+1] == val+1 and \
                        hand[idx+2] == val+2 and \
                        hand[idx+3] == val+3 and \
                        hand[idx+4] == val+4:
                        return 40
        except IndexError:
            pass
        return 0

    def yahtzee(self, hand):
        if len(set(hand.get_hand())) == 1:
            return 50
        return 0

    def chance(self, hand):
        return sum(hand.get_hand())


class ScoreBoard(object):

    
    def __init__(self):
        self.scoreboard_rows = {
            1: "Aces",
            2: "Twos",
            3: "Threes",
            4: "Fours",
            5: "Fives",
            6: "Sixes",
            7: "Three of a Kind",
            8: "Four of a Kind",
            9: "Full House",
            10: "Small Straight",
            11: "Large Straight",
            12: "Yahtzee",
            13: "Chance",
        }
       
        self.__scoreboard_points = {}

    def set_scoreboard_row_value(self, row, value):
        if row not in self.scoreboard_rows.keys():
            print("Bad row index")
            return False
        else:
            if row in self.__scoreboard_points.keys():
                print("ScoreBoard already saved!")
                return False
            else:
                print("Adding {} points to {}".format(
                    value,
                    self.scoreboard_rows[int(row)])
                )
                self.__scoreboard_points[row] = value
                return True

    def get_scoreboard_points(self):
        return self.__scoreboard_points

    def show_scoreboard_rows(self):
        for key, val in self.scoreboard_rows.items():
            print("{}. {}".format(key, val))

    def show_scoreboard_points(self):
        print("\nSCOREBOARD")
        print("===================================")
        for idx, row in self.scoreboard_rows.items():
            try:
                print("{:<2} {:<21}| {:2} points".format(idx,
                      row,
                      self.__scoreboard_points[idx]))
            except KeyError:
                print("{:<2} {:<21}|".format(idx, row))
        print("===================================")

    def select_scoring(self, hand):
        msg = "Choose which scoring to use "\
               "(press enter to show available rows): "
        scoreboard_row = False
        score_saved = False
        while not scoreboard_row and not score_saved:
            scoreboard_row = input(msg)
            if scoreboard_row.strip() == "":
                self.show_scoreboard_points()
                scoreboard_row = False
                continue
            try:
                scoreboard_row = int(re.sub('[^0-9,]', '', scoreboard_row))
            except ValueError:
                print("You entered something other than a number.")
                print("Please try again")
                scoreboard_row = False
                continue
            if scoreboard_row > len(self.scoreboard_rows):
                print("Please select an existing scoring rule.")
                scoreboard_row = False
                continue
            else:
                score_saved = self.set_scoreboard_row_value(
                    int(scoreboard_row),
                    Rules().rules_map[int(scoreboard_row)](hand)
                )


def Main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
YAHTZEE
Welcome to the game. 
""")

    
    hand = Hand(5, 6)
    scoreboard = ScoreBoard()

    
    while len(scoreboard.get_scoreboard_points()) < len(scoreboard.scoreboard_rows):
        hand.throw()
        hand.show_hand()
        hand.re_roll()
        scoreboard.select_scoring(hand)
        scoreboard.show_scoreboard_points()

        input("\nPress enter to continue")
        os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCongratulations! You finished the game!\n")
    scoreboard.show_scoreboard_points()
    print("Total points: {}".format(sum(scoreboard.get_scoreboard_points().values())))


if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

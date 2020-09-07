import random
import time

from lib.fight import fight_setup
from lib.static import speech_manipulation


class BridgeGuard:
    def __init__(self, player):
        speech_manipulation("Hey! YOU! Don't think about crossing this bridge without paying the price.\n", 0.05)
        print(" " * 6 + "1. Pay 10 Gold.")
        print(" " * 6 + "2. Persuade the Guard.")
        print(" " * 6 + "3. Intimidate the Guard.")
        print(" " * 6 + "4. Go and mind your own business.")
        answ = input("> ")

        while answ not in ["1", "2", "3", "4"]:
            print("Invalid option.")
            answ = input("> ")

        if answ == "1" and player.gold > 9:
            player.gold -= 10
            speech_manipulation("I knew you are a good person. Have a nice day Sir.\n", 0.04)
        elif answ == "1" and player.gold < 10:
            speech_manipulation("I see you have not enough money with you.\n", 0.05)
            fight_setup(player, [1, 0, 0])
        elif answ == "2" and (random.random() > (0.5 + (0.1 * player.level) - player.friendly)):
            speech_manipulation("Am I looking like a joke to you?\n", 0.04)
            fight_setup(player, [1, 0, 0])
            player.friendly += 0.1
        elif answ == "2":
            speech_manipulation("Okay I see you have some serious trouble yourself. I will give you a riddle and you "
                                "can solve this instead of paying the price.\n", 0.05)
            self.riddles(player)
        elif answ == "3" and (random.random() > (0.2 + (0.1 * player.level) - player.friendly)):
            speech_manipulation("Well. It doesn't seem you know whom you are talking to?\n", 0.05)
            fight_setup(player, [1, 0, 0])
            player.friendly += 0.1
        elif answ == "3":
            speech_manipulation(
                "Okay, okay. You don't have to get mad. Go over there .. but don't come back quickly.\n", 0.04)
        elif answ == "4":
            speech_manipulation("Yeah better go now!\n", 0.04)

    def riddles(self, player):
        riddles = [("""
        This thing all things devours:
        Birds, beasts, trees, flowers;
        Gnaws iron, bites steel;
        Grinds hard stones to meal;
        Slays king, ruins town,
        And beats high mountain down.
        \n""", "time"),
                   ("""
        Alive without breath,
        As cold as death;
        Never thirsty, ever drinking,
        All in mail never clinking.
        \n""", "fish"),
                   ("""
        A box without hinges, key, or lid,
        yet golden treasure inside is hid.
        \n""", "egg"),
                   ("""
        It cannot be seen, cannot be felt,
        Cannot be heard, cannot be smelt.
        It lies behind stars and under hills,
        And empty holes it fills.
        It comes first and follows after,
        Ends life, kills laughter.
        \n""", "dark"),
                   ("""
        Voiceless it cries,
        Wingless flutters,
        toothless bites,
        Mouthless mutters.
        \n""", "wind"),
                   ("""
        Thirty white horses on a red hill,
        First they champ,
        Then they stamp,
        Then they stand still.
        \n""", "teeth"),
                   ("""
        What has roots as nobody sees,
        Is taller than trees,
        Up, up it goes,
        And yet never grows?
        \n""", "mountain")]

        speech_manipulation("What is this: \n", 0.05)
        riddle = random.choice(riddles)
        speech_manipulation(riddle[0], 0.04)

        answ = input("> ")
        if answ.lower() != riddle[1]:
            speech_manipulation("Maybe you're better with your sword than with your mind.", 0.05)
            time.sleep(.5)
            fight_setup(player, [1, 0, 0])
        else:
            speech_manipulation("I knew you are clever. So have a good day on your journey.", 0.05)


class TownGuard:
    pass

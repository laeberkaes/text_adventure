import random
import random
import sys
import time

from lib import game_object
from lib.ascii import print_warrior, print_mage, print_rogue
from lib.fight import fight_setup
from lib.guards import BridgeGuard
from lib.map import zonemap, solved_places
from lib.npc import Spell
from lib.player import myPlayer
from lib.static import clear, screen_width, speech_manipulation, game_over


def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        setup_game()
    elif option.lower() == "help":
        help_menu()
    elif option.lower() == "quit":
        sys.exit()

    while option.lower() not in ["play", "help", "quit"]:
        print("Invalid command. Type 'play', 'help', 'quit'")
        title_screen_selections()


def title_screen():
    clear()
    print("#" * screen_width)
    print("#" + (" " * int((screen_width - len("Welcome to the Text RPG")) / 2)) + "Welcome to the Text RPG" + (
            " " * int((screen_width - 2 - len("Welcome to the Text RPG")) / 2)) + "#")
    print("#" + "=" * (screen_width - 2) + "#")
    print("#" + (" " * int((screen_width - 6) / 2)) + "-play-" + (" " * int((screen_width - 9) / 2)) + "#")
    print("#" + (" " * int((screen_width - 6) / 2)) + "-help-" + (" " * int((screen_width - 9) / 2)) + "#")
    print("#" + (" " * int((screen_width - 6) / 2)) + "-quit-" + (" " * int((screen_width - 9) / 2)) + "#")
    print("#" * screen_width + "\n")
    title_screen_selections()


def help_menu():
    clear()
    print("#" * screen_width)
    print(("=" * int((screen_width - len("HELP MENU")) / 2)) + "HELP MENU" + (
            "=" * int((screen_width - len("HELP MENU")) / 2)))
    print("#" * screen_width)
    print("")
    print(" -- You can always decide to 'examine' a location or 'move' to another.")
    print(" -- You can always see your inventory with 'show inventory' and show your stats with 'show stats'")
    print("-- If you examine a location you may trigger a random encounter and you can 'fish', 'hunt'. 'rest', "
          "'learn' or 'get corn'")
    print(" -- If you move, you can decide to move 'up', 'down', 'left' or 'right'")
    print("")
    print("Press ENTER to continue.")
    input()
    title_screen()
    title_screen_selections()


def print_location():
    print("#" * screen_width)
    print((" " * int((screen_width - len(zonemap[myPlayer.location]["ZONENAME"])) / 2)) + zonemap[myPlayer.location][
        "ZONENAME"] + (" " * int((screen_width - len(zonemap[myPlayer.location]["ZONENAME"])) / 2)))
    print((" " * int((screen_width - len(zonemap[myPlayer.location]["DESCRIPTION"])) / 2)) + zonemap[myPlayer.location][
        "DESCRIPTION"] + (" " * int((screen_width - len(zonemap[myPlayer.location]["DESCRIPTION"])) / 2)))
    if zonemap[myPlayer.location]["SOLVED"] == True:
        print((" " * int(
            (screen_width - len(zonemap[myPlayer.location]["EXAMINATION"] + "EXAMINATION")) / 2)) + "EXAMINATION: " +
              zonemap[myPlayer.location]["EXAMINATION"] + (" " * int(
            (screen_width - len(zonemap[myPlayer.location]["EXAMINATION"] + "EXAMINATION")) / 2)))
    print("#" * screen_width)


def prompt():
    print("You are here:")
    print_location()
    print("\n" + "=" * len("What would you like to do?"))
    print("What would you like to do?\n")
    print("-" * len("What would you like to do?"))
    print(" " * (int((len("What would you like to do?") - len("examine or move?")) / 2)) + "examine or move?")
    print("-" * len("What would you like to do?") + "\n")

    action = input("> ")
    acceptable_locations = ["move", "go", "travel", "walk", "quit", "examine", "inspect", "interact", "look", "hunting",
                            "hunt", "fishing", "fish", "corn", "get corn", "harvest", "heal", "healing", "potion",
                            "use potion", "show inventory", "inventory", "show stats", "stats", "buy", "sell", "repair",
                            "blacksmith", "knock", "magic", "learn", "spell", "rest", "play", "talk", "quests", "quest"]

    while action.lower() not in acceptable_locations:
        print("Unknown action. Try again. (move, examine, quit)")
        action = input("> ")

    if action.lower() == "quit":
        sys.exit()
    elif action.lower() in ["move", "go", "travel", "walk"]:
        player_move()
    elif action.lower() in ["examine", "inspect", "interact", "look"]:
        player_examine()
    elif action.lower() in ["fishing", "fish"]:
        myPlayer.fishing()
    elif action.lower() in ["hunting", "hunt"]:
        myPlayer.hunting()
    elif action.lower() in ["corn", "get corn", "harvest"]:
        myPlayer.get_corn()
    elif action.lower() in ["heal", "healing", "potion", "use potion"]:
        myPlayer.use_potion()
    elif action.lower() in ["show inventory", "inventory"]:
        myPlayer.print_inventory()
    elif action.lower() in ["show stats", "stats"]:
        myPlayer.show_stats()
    elif action.lower() in ["buy", "sell", "blacksmith", "repair"]:
        myPlayer.buy_equipment()
    elif action.lower() in ["knock", "magic", "learn", "spell"]:
        myPlayer.learn_spell()
    elif action.lower() == "rest":
        myPlayer.rest()
    elif action.lower() == "play":
        myPlayer.play_game()
    elif action.lower() == "talk":
        myPlayer.escape_room()
    elif action.lower() in ["quests", "quest"]:
        myPlayer.show_quests()

def player_move():
    dest = input("Where do you like to move to? ('up', 'down', 'left', 'right')\n> ")

    while dest not in ['up', 'down', 'left', 'right']:
        print("Invalid entry!")
        dest = input("Where do you like to move to? ('up', 'down', 'left', 'right')\n> ")

    if dest.lower() == "up":
        if zonemap[myPlayer.location]["UP"] != "":
            destination = zonemap[myPlayer.location]["UP"]
            myPlayer.direction = dest.lower()
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "down":
        if zonemap[myPlayer.location]["DOWN"] != "":
            destination = zonemap[myPlayer.location]["DOWN"]
            myPlayer.direction = dest.lower()
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "right":
        if zonemap[myPlayer.location]["RIGHT"] != "":
            destination = zonemap[myPlayer.location]["RIGHT"]
            myPlayer.direction = dest.lower()
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "left":
        if zonemap[myPlayer.location]["LEFT"] != "":
            destination = zonemap[myPlayer.location]["LEFT"]
            myPlayer.direction = dest.lower()
            movement(destination)
        else:
            stay(dest)


def movement(destination):
    if (myPlayer.location == "b1" and destination == "c1") or (myPlayer.location == "c1" and destination == "b1"):
        print("Do you want do 'swim' over the river or go over the the bridge in the west?")
        answer = input("> ")
        if answer == "swim":
            if random.random() < 0.2:
                factor = random.random()
                print("Unfortunately you get attacked by a snake.")
                print("You get " + str(factor * 10) + " damage.")
                myPlayer.health_cur -= factor * 10
                if myPlayer.health_cur < 0:
                    print("You died.")
                    time.sleep(2)
                    game_over()
    if (myPlayer.location == "b2" and destination == "c2") or (myPlayer.location == "c2" and destination == "b2"):
        BridgeGuard(myPlayer)
    myPlayer.location = destination
    print("You have moved to the " + zonemap[myPlayer.location]["ZONENAME"] + ".")
    time.sleep(2)
    clear()


def stay(direct):
    directions = {"up": "north", "down": "south", "left": "west", "right": "east"}
    print("You cannot move further " + directions[direct] + ".")
    time.sleep(3)
    clear()


def player_examine():
    if zonemap[myPlayer.location]["ENCOUNTERS"] > 0:
        fight_setup(myPlayer, zonemap[myPlayer.location]["POSSIBILITIES"])

    if zonemap[myPlayer.location]["SOLVED"] == True:
        print("You have already been here.")
        print(zonemap[myPlayer.location]["EXAMINATION"])
        time.sleep(3)
        clear()
    else:
        print(zonemap[myPlayer.location]["EXAMINATION"])
        zonemap[myPlayer.location]["SOLVED"] = True
        if all(solved_places.values()):
            myPlayer.game_over = True
        time.sleep(3)
        clear()


def intro():
    clear()
    question3 = "Welcome, " + myPlayer.name + " the " + myPlayer.play_class + ".\n"
    speech_manipulation(question3, 0.05)
    speech_manipulation("Welcome to this fantasy world I created for you. ;)\n", 0.05)
    speech_manipulation("I hope you will have some fun\n ... \n ... \n ...\n", 0.15)
    speech_manipulation(
        "Well, you are not the first adventurer here. There have been many before you. And to be honest, there will "
        "be many after you ... when you have ... ",
        0.05)
    speech_manipulation("passed away ... \n", 0.25)
    speech_manipulation("Now have some fun exploring the world. We will see each other when it's time to.\n", 0.05)
    time.sleep(2)


def end_screen():
    speech_manipulation(
        "Congratulations, you have solved the complete game. I never thought you would be able to do this.", 0.05)
    print("")
    speech_manipulation(
        "I will get in touch with you soon. Wait for a sign from me. I think I have a good job for some strong "
        "adventurer like you.",
        0.04)
    time.sleep(5)
    clear()
    # print("Made by laeberkaes")
    # print("Hit me "UP" at: https://github.com/laeberkaes/ or @laeberkaes:uraltemorla.xyz")
    #
    # time.sleep(5)
    sys.exit()


# def game_over():
#     clear()
#     speech_manipulation("Ouh there you are again.\n", 0.05)
#     speech_manipulation(
#         "Don't get me wrong. This is no surprise for me. Maybe you have more luck in your next reincarnation.\n",
#         0.05)
#     speech_manipulation("Have a good day. :)", 0.07)
#     myPlayer.game_over = True
#     time.sleep(2)
#     sys.exit()


def game_loop():
    while not myPlayer.game_over:
        prompt()


def setup_game():
    clear()
    question1 = "Hello what's your name?\n"
    speech_manipulation(question1, 0.05)
    print("")
    myPlayer.name = input("> ").lower()

    clear()

    classes = ["warrior", "mage", "rogue", "debug"]
    question2 = "What Class do you want to play? ('Warrior', 'Mage', 'Rogue')\n"
    speech_manipulation(question2, 0.01)
    print("")
    player_class = input("> ").lower()
    print("")
    if player_class.lower() in classes:
        myPlayer.play_class = player_class
        print("You are now a:")
    else:
        while player_class.lower() not in classes:
            print("No valid class.\n")
            player_class = input("> ").lower()
        if player_class.lower() in classes:
            myPlayer.play_class = player_class
            print("You are now " + player_class)

    if myPlayer.play_class == "warrior":
        print_warrior()
        time.sleep(2)
        myPlayer.health_max = 120
        myPlayer.health_cur = 120
        myPlayer.mp_cur_max.append(20)
        myPlayer.mp_cur_max.append(20)

        myPlayer.karma = 1.0
        myPlayer.strength = 0.3
        myPlayer.dexterity = -0.1
        myPlayer.constitution = 0.2
        myPlayer.intelligence = 0.0
        myPlayer.wisdom = 0.1
        myPlayer.charisma = 0.2
    elif myPlayer.play_class == "mage":
        print_mage()
        time.sleep(2)
        myPlayer.health_max = 80
        myPlayer.health_cur = 80
        myPlayer.mp_cur_max.append(80)
        myPlayer.mp_cur_max.append(80)

        myPlayer.karma = 1.0
        myPlayer.strength = 0.0
        myPlayer.dexterity = 0.2
        myPlayer.constitution = 0.2
        myPlayer.intelligence = 0.3
        myPlayer.wisdom = 0.1
        myPlayer.charisma = -0.1
    elif myPlayer.play_class == "rogue":
        print_rogue()
        time.sleep(2)
        myPlayer.health_max = 100
        myPlayer.health_cur = 100
        myPlayer.mp_cur_max.append(40)
        myPlayer.mp_cur_max.append(40)

        myPlayer.karma = 1.0
        myPlayer.strength = -0.1
        myPlayer.dexterity = 0.3
        myPlayer.constitution = 0.1
        myPlayer.intelligence = 0.1
        myPlayer.wisdom = 0.0
        myPlayer.charisma = 0.3
    elif myPlayer.play_class == "debug":
        myPlayer.health_max = 1000
        myPlayer.health_cur = 1000
        myPlayer.mp_cur_max.append(400)
        myPlayer.mp_cur_max.append(400)
        myPlayer.level = 10
        myPlayer.gold = 10000

        myPlayer.karma = 1.0
        myPlayer.strength = -0.1
        myPlayer.dexterity = 0.3
        myPlayer.constitution = 0.1
        myPlayer.intelligence = 0.1
        myPlayer.wisdom = 0.0
        myPlayer.charisma = 0.3

        for i in range(3):
            myPlayer.spells.append(Spell(myPlayer))
        myPlayer.weapon = game_object.Weapon(10)
        print("Where to start? (a1, a2, etc.")
        myPlayer.location = input("> ")
    # intro()

    clear()
    print("#" * screen_width + "\n")
    print("#" + (" " * int((screen_width - 2 - len("Let's start now")) / 2)) + "Let's start now" + (
            " " * int((screen_width - 2 - len("Let's start now")) / 2)) + "#\n")
    print("#" * screen_width + "\n")

    game_loop()

    end_screen()


if __name__ == "__main__":
    title_screen()

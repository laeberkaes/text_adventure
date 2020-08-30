import os
import random
import sys
import time

import weapon  # player

screen_width = 60


class Player:
    def __init__(self):
        self.name = ""
        self.play_class = ""
        self.health_max = 0
        self.health_cur = self.health_max
        self.mp = 0
        self.ep = 0
        self.level = 1
        self.status_effects = []
        self.location = "b2"
        self.game_over = False
        self.weapon = weapon.Weapon(self.level)
        self.weapon.equiped = True
        self.potions = 1
        self.inventory = {"weapons": [self.weapon], "armor": [], "misc": dict()}
        self.gold = 10
        self.head_protect = 0
        self.chest_protect = 0
        self.leg_protect = 0
        self.arm_protect = 0
        self.pos = (0.95, 0.05, 0)

    def calc_armor(self):
        return sum([self.head_protect, self.chest_protect, self.leg_protect, self.arm_protect])

    def health(self):
        print("Your health: " + str(self.health_cur) + "/" + str(self.health_max) + " HP")

    def level_up(self):
        self.level += 1
        self.health_max += 20
        self.ep -= 100
        self.pos = (
            self.pos[0] - (self.level * 0.05), self.pos[1] + (self.level * 0.1), self.pos[2] + (self.level * 0.05))
        speech_manipulation(
            "Congratulations, you leveled up. You are now a level " + str(self.level) + " " + self.play_class + ".\n",
            0.03)
        speech_manipulation("You have " + str(self.health_max) + " HP.", 0.03)
        time.sleep(2)
        while self.ep > 100:
            self.level_up()

    def get_ep(self, amount):
        self.ep += amount
        if self.ep > 100:
            self.level_up()

    def get_weapon(self, weapon):
        self.weapon.equiped = False
        self.weapon = weapon
        self.weapon.equiped = True
        self.inventory["weapons"].append(weapon)

    def get_armor(self, armor):
        for arm in self.inventory["armor"]:
            if arm.slot == armor.slot and arm.equiped == True:
                arm.equiped = False
        self.protect(armor.slot, armor.protection)
        armor.equiped = True
        self.inventory["armor"].append(armor)

    def get_gold(self, amount):
        self.gold += amount

    def get_potion(self, amount):
        self.potions += amount

    def print_inventory(self):
        os.system("clear")
        print("#" * screen_width)
        print(
            "=" * int((screen_width - len("WEAPONS")) / 2) + "WEAPONS" + "=" * int((screen_width - len("WEAPONS")) / 2))
        for weapon in self.inventory["weapons"]:
            if weapon.equiped == True:
                print("EQUIPED: " + str(weapon)[13:])
            else:
                print(str(weapon)[13:])
        print("")
        print("=" * int((screen_width - len("ARMOR")) / 2) + "ARMOR" + "=" * int((screen_width - len("ARMOR")) / 2))
        for armor in self.inventory["armor"]:
            if armor.equiped == True:
                print("EQUIPED: A" + str(armor)[6:])
            else:
                print("A" + str(armor)[6:])
        print("")
        print(
            "=" * int((screen_width - len("POTIONS")) / 2) + "POTIONS" + "=" * int((screen_width - len("POTIONS")) / 2))
        if self.potions == 1:
            print("You have " + str(self.potions) + " potion.")
        if self.potions > 1:
            print("You have " + str(self.potions) + " potions.")
        print("")
        print("=" * int((screen_width - len("MISC")) / 2) + "MISC" + "=" * int((screen_width - len("MISC")) / 2))
        for misc in self.inventory["misc"]:
            print(misc + ": " + str(self.inventory["misc"][misc]))
        print("")
        print("Press ENTER to continue.")
        input()
        os.system("clear")

    def show_stats(self):
        os.system("clear")
        print("#" * screen_width)
        print("")
        print("Name:" + " " * (20 - len("Name:")) + self.name)
        print("Class:" + " " * (20 - len("Class:")) + self.play_class)
        print("Level:" + " " * (20 - len("Level:")) + str(self.level))
        print("EP:" + " " * (20 - len("EP:")) + str(self.ep))
        print("Health:" + " " * (20 - len("Health:")) + str(self.health_cur) + "/" + str(self.health_max))
        print("Armor:" + " " * (20 - len("Armor:")) + str(self.calc_armor()))
        print("")
        print("#" * screen_width)
        print("")
        print("Press ENTER to continue.")
        input()
        os.system("clear")

    def use_potion(self):
        if self.potions > 0:
            self.health_cur += 25
            if self.health_cur > self.health_max:
                self.health_cur = self.health_max
            self.potions -= 1
            print("Ahhhh this feels good. You feel new power filling up your body. (HP +25)")
        else:
            print("You don't have any potions left.")
        time.sleep(2)
        os.system("clear")

    def get_object(self, obj):
        if obj not in self.inventory["misc"] and type(obj) == str:
            self.inventory["misc"][obj] = 1
        elif obj in self.inventory["misc"]:
            self.inventory["misc"][obj] += 1
        elif obj.obj_type() == "weapon":
            self.inventory["weapons"].append(obj)
        elif obj.obj_type() == "armor":
            self.inventory["armor"].append(obj)

    def protect(self, place, amount):
        if place == "head":
            self.head_protect = amount
        elif place == "chest":
            self.chest_protect = amount
        elif place == "leg":
            self.leg_protect = amount
        elif place == "arm":
            self.arm_protect = amount

    def fishing(self):
        if self.location in ["a4", "c1", "c2"] and "fishingrot" in self.inventory:
            p = random.random()
            if p > 0.95:
                print("You get an old, stinky boot. *urgh*")
                if "Old, stinky boot" not in self.inventory:
                    self.inventory["Old, stinky boot"] = 1
                else:
                    self.inventory["Old, stinky boot"] += 1
            elif p > 0.5:
                print("You got a nice, fresh fish")
                if "fish" not in self.inventory:
                    self.inventory["fish"] = 1
                else:
                    self.inventory["fish"] += 1

            else:
                print("You got nothing for now. But you can fish all day long.")

        else:
            print("Well you can try to fish here. But you will not get any more than some dirt.")

        time.sleep(2)
        os.system("clear")

    def getCorn(self):
        if self.location == "d2":
            p = random.random()
            if p > 0.25:
                print("You get some nice corn.")
                if "bag of corn" not in self.inventory:
                    self.inventory["bag of corn"] = 1
                else:
                    self.inventory["bag of corn"] += 1
            else:
                print("Baaah. You better not take this corn with you.")
        else:
            print("Well you cannot get corn out of this place.")

        time.sleep(2)
        os.system("clear")

    def hunting(self):
        if self.location in ["b3", "b4", "c3", "c4"]:
            p = random.random()
            if p > 0.95:
                print("You get some nice deer. This will give you good food for some days.")
                if "meat" not in self.inventory:
                    self.inventory["meat"] = 10
                else:
                    self.inventory["meat"] += 10
            elif p > 0.6:
                print("You get some rabbits and a small boar.")
                if "meat" not in self.inventory:
                    self.inventory["meat"] = 7
                else:
                    self.inventory["meat"] += 7
            else:
                print("Well you are out of luck for now.")
        else:
            print("You will find no wild animals in this area. Try your luck in the eastern forest.")

        time.sleep(2)
        os.system("clear")


myPlayer = Player()


##### Title #####
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
    os.system("clear")
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
    os.system("clear")
    print("#" * screen_width)
    print(("=" * int((screen_width - len("HELP MENU")) / 2)) + "HELP MENU" + (
            "=" * int((screen_width - len("HELP MENU")) / 2)))
    print("#" * screen_width)
    print("")
    print(" -- You can always decide to 'examine' a location or 'move' to another.")
    print(" -- You can always see your inventory with 'show inventory' and show your stats with 'show stats'")
    print(" -- If you examine a location you may trigger a random encounter and you can 'fish', 'hunt' or 'get corn'")
    print(" -- If you move, you can decide to move 'up', 'down', 'left' or 'right'")
    print("")
    print("Press ENTER to continue.")
    input()
    title_screen()
    title_screen_selections()


### MAP ###
solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False, 'b1': False, 'b2': False, 'b3': False, 'b4': False,
                 'c1': False, 'c2': False, 'c3': False, 'c4': False, 'd1': False, 'd2': False, 'd3': False, 'd4': False}

##### MAP PRE #####
# ""ZONENAME"" = ""
# ""DESCRIPTION"" = ""DESCRIPTION""
# ""EXAMINATION"" = "examine"
# ""SOLVED"" = False
# ""UP"" = ""UP""
# ""DOWN"" = ""DOWN""
# ""LEFT"" = ""LEFT""
# ""RIGHT"" = ""RIGHT""
# ""SOLVED"_ENCOUNTER_COUNT" = 0
# ""ENCOUNTERS"" = 0
POSSIBILITIES = myPlayer.pos

zonemap = {
    "a1": {
        "ZONENAME": "Town Marketplace",
        "DESCRIPTION": "This is the marketplace of your hometown.",
        "EXAMINATION": "You can see some stalls selling different things.",
        "SOLVED": False,
        "UP": "",
        "DOWN": "b1",
        "LEFT": "",
        "RIGHT": "a2",
        "ENCOUNTERS": 0,
        "POSSIBILITIES": POSSIBILITIES
    },
    "a2": {
        "ZONENAME": "Towngate",
        "DESCRIPTION": "This is the gate of your hometown.",
        "EXAMINATION": "The gate is locked at night. You have to be nice to the guardsmen, if you try to enter at "
                       "night.",
        "SOLVED": False,
        "UP": "",
        "DOWN": "b2",
        "LEFT": "a1",
        "RIGHT": "a3",
        "ENCOUNTERS": 0,
        "POSSIBILITIES": POSSIBILITIES
    },
    "a3": {
        "ZONENAME": "Grassland",
        "DESCRIPTION": "Nothing but green grass.",
        "EXAMINATION": "I'm serious. It's nothing but grass.",
        "SOLVED": False,
        "UP": "",
        "DOWN": "b3",
        "LEFT": "a2",
        "RIGHT": "a4",
        "ENCOUNTERS": 2,
        "POSSIBILITIES": POSSIBILITIES
    },
    "a4": {
        "ZONENAME": "Little Pond",
        "DESCRIPTION": "This is a cute little pond.",
        "EXAMINATION": "With a fishingrot you could get some fish out of it.",
        "SOLVED": False,
        "UP": "",
        "DOWN": "b4",
        "LEFT": "a3",
        "RIGHT": "",
        "ENCOUNTERS": 2,
        "POSSIBILITIES": POSSIBILITIES
    },
    "b1": {
        "ZONENAME": "Blacksmith",
        "DESCRIPTION": "This is your local blacksmith.",
        "EXAMINATION": "Here you can buy/sell some weapons or protections",
        "SOLVED": False,
        "UP": "a1",
        "DOWN": "c1",
        "LEFT": "",
        "RIGHT": "b2",
        "ENCOUNTERS": 0,
        "POSSIBILITIES": POSSIBILITIES
    },
    "b2": {
        "ZONENAME": "Home",
        "DESCRIPTION": "This is your home!",
        "EXAMINATION": "Your home looks cosy.",
        "SOLVED": False,
        "UP": "a2",
        "DOWN": "c2",
        "LEFT": "b1",
        "RIGHT": "b3",
        "ENCOUNTERS": 0,
        "POSSIBILITIES": POSSIBILITIES
    },
    "b3": {
        "ZONENAME": "Small Forest",
        "DESCRIPTION": "A small forest next to your home.",
        "EXAMINATION": "You could hunt in this forest to get some food. But some bandits were seen in there, too.",
        "SOLVED": False,
        "UP": "a3",
        "DOWN": "c3",
        "LEFT": "b2",
        "RIGHT": "b4",
        "ENCOUNTERS": 3,
        "POSSIBILITIES": POSSIBILITIES
    },
    "b4": {
        "ZONENAME": "Small Forest",
        "DESCRIPTION": "A small forest next to your home.",
        "EXAMINATION": "You could hunt in this forest to get some food. But some bandits were seen in there, too.",
        "SOLVED": False,
        "UP": "a4",
        "DOWN": "c4",
        "LEFT": "b3",
        "RIGHT": "",
        "ENCOUNTERS": 3,
        "POSSIBILITIES": POSSIBILITIES
    },
    "c1": {
        "ZONENAME": "Little River",
        "DESCRIPTION": "This river comes out of the forest in the east.",
        "EXAMINATION": "Further to the forest you can see a bridge over the river.",
        "SOLVED": False,
        "UP": "b1",
        "DOWN": "d1",
        "LEFT": "",
        "RIGHT": "c2",
        "ENCOUNTERS": 2,
        "POSSIBILITIES": POSSIBILITIES
    },
    "c2": {
        "ZONENAME": "Little River (Bridge)",
        "DESCRIPTION": "This river comes out of the forest in the east.",
        "EXAMINATION": "You see a bridge leading over the river to get to the other side.",
        "SOLVED": False,
        "UP": "b2",
        "DOWN": "d2",
        "LEFT": "c1",
        "RIGHT": "c3",
        "ENCOUNTERS": 2,
        "POSSIBILITIES": POSSIBILITIES
    },
    "c3": {
        "ZONENAME": "Small Forest",
        "DESCRIPTION": "A small forest next to your home.",
        "EXAMINATION": "You could hunt in this forest to get some food. But some bandits were seen in there, too.",
        "SOLVED": False,
        "UP": "b3",
        "DOWN": "d3",
        "LEFT": "c2",
        "RIGHT": "c4",
        "ENCOUNTERS": 3,
        "POSSIBILITIES": POSSIBILITIES
    },
    "c4": {
        "ZONENAME": "Small Forest",
        "DESCRIPTION": "A small forest next to your home.",
        "EXAMINATION": "You could hunt in this forest to get some food. But some bandits were seen in there, too.",
        "SOLVED": False,
        "UP": "b4",
        "DOWN": "d4",
        "LEFT": "c3",
        "RIGHT": "",
        "ENCOUNTERS": 3,
        "POSSIBILITIES": POSSIBILITIES
    },
    "d1": {
        "ZONENAME": "Cave",
        "DESCRIPTION": "Down in the south is a small Trollcave.",
        "EXAMINATION": "You see some skelletons of deer and horses. Is it really a good idea to go into the cave?",
        "SOLVED": False,
        "UP": "c1",
        "DOWN": "",
        "LEFT": "",
        "RIGHT": "d2",
        "ENCOUNTERS": 5,
        "POSSIBILITIES": [0.7, 0.3, 1]
    },
    "d2": {
        "ZONENAME": "Cornfield",
        "DESCRIPTION": "This cornfield belongs to the farm in the east. Maybe you can get some corn from it?",
        "EXAMINATION": "Looks like this corn is better than what you have ever seen.",
        "SOLVED": False,
        "UP": "c2",
        "DOWN": "",
        "LEFT": "d1",
        "RIGHT": "d3",
        "ENCOUNTERS": 2,
        "POSSIBILITIES": POSSIBILITIES
    },
    "d3": {
        "ZONENAME": "Farm",
        "DESCRIPTION": "This farm is owned by an old farmer.",
        "EXAMINATION": "You have heard some scary stories about this farmer. Maybe he is not very nice?",
        "SOLVED": False,
        "UP": "c3",
        "DOWN": "",
        "LEFT": "d2",
        "RIGHT": "d4",
        "ENCOUNTERS": 3,
        "POSSIBILITIES": POSSIBILITIES
    },
    "d4": {
        "ZONENAME": "Bandit Hideout",
        "DESCRIPTION": "This looks like some bandit hideout, which was not here the last time you were here.",
        "EXAMINATION": "You cannot see any other human being. But you feel that you better move away.",
        "SOLVED": False,
        "UP": "c4",
        "DOWN": "",
        "LEFT": "d3",
        "RIGHT": "",
        "ENCOUNTERS": 7,
        "POSSIBILITIES": [0.5, 1, 0]
    }
}


# class Weapon():
#     def __init__(self, level):
#         adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody"]
#         subst = [" Dagger", " Hammer", " Sword", " Bow", " Spear", " Morning Star", " Club", " Axe"]
#         self.obj_type = "weapon"
#         self.level = level
#         self.name = random.choice(adjective) + random.choice(subst)
#         self.damage = random.randrange(3,6)*level #=> 3-5
#
#     def __repr__(self):
#         return "Your weapon: "+self.name+", with "+str(self.damage)+" damage"
#
# class Armor():
#     def __init__(self,level):
#         adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody"]
#         subst = [" Plate Armor", " Chain Armor", " Leather Armor"]
#         self.obj_type = "armor"
#         self.slot = random.choice(["head","chest","leg","arm"])
#         self.level = level
#         self.name = random.choice(adjective) + random.choice(subst)
#         self.protection = random.randrange(10,21)*level #=> 3-5
#
#     def __repr__(self):
#         return "Your weapon: "+self.name+", with "+str(self.damage)+" damage"
#
#     def equip_armor(self,person):
#             if self.slot == "head":
#                 person.head_protect += self.protection
#             elif self.slot == "chest":
#                 person.chest_protect += self.protection
#             elif self.slot == "leg":
#                 person.leg_protect += self.protection
#             elif self.slot == "arm":
#                 person.arm_protect += self.protection

class NPC:
    def __init__(self, health, strength):
        self.health = health * random.randrange(10, 21)
        self.strength = strength * random.randrange(5, 11)

    def health_print(self):
        print("Enemy Health " + str(self.health))


class Bandit(NPC):
    def __init__(self):
        super().__init__(1, 1)  # set health + strength
        self.name = "Bandit"
        self.quip = ["Oi!", "Ow!", "Aaargh!", "Hng!"]
        self.accuracy = 0.65
        self.loot_chance = 0.80
        self.loot_level = 2
        self.ep_drop = random.randrange(30, 41)


class Orc(NPC):
    def __init__(self):
        super().__init__(3, 3)
        self.name = "Orc"
        self.quip = ["Uagh!", "Uff!", "Gnar!", "Grrrrr!"]
        self.accuracy = 0.75
        self.loot_chance = 40
        self.loot_level = 3
        self.ep_drop = random.randrange(50, 71)


class Giant(NPC):
    def __init__(self):
        super().__init__(10, 10)
        self.name = "Giant"
        self.quip = ["AAAAAH!", "Fi, Fai, Fo, Fumm!", "Hargh!"]
        self.accuracy = 0.9
        self.loot_chance = 50
        self.loot_level = 5
        self.ep_drop = random.randrange(100, 151)  # bei 100EP cap quasi ein garantiertes level"UP"


def fight(player, poss):
    os.system("clear")
    print("#" * screen_width)
    print(" " * int((screen_width - len("FIGHT")) / 2) + "FIGHT")
    print("#" * screen_width)
    enemy = ""
    x = random.random()
    if x < poss[0]:
        enemy = Bandit()
    elif poss[0] < x < poss[0] + poss[1]:
        enemy = Orc()
    else:
        enemy = Giant()  # else, solange nur 3 mögliche Gegner
    flee = 0
    dead = 0
    while dead == 0:  # es läuft mal mit meinen beiden Schleifen, weil ich nicht genau weiß, wie wir bei dir
        # game_over einbinden können
        while enemy.health > 0 and flee == 0:
            print("                 ")
            print("You fight against: " + enemy.name)
            enemy.health_print()
            player.health()  # Die fehlt noch in der init
            a = fight_options().lower()  # das geht sicher eleganter

            valid_options = ["attack", "heal", "flee", "show stats", "quit"]
            while a not in valid_options:
                print("Please use a valid answer.")  # nochmal eine Chance zur Eingabe oder direkt Angriff Gegner?
                a = fight_options().lower()

            if a == "attack":
                print("You attack with your weapon and do " + str(player.weapon.damage) + " damage.")
                enemy.health -= player.weapon.damage
                print("enemy: " + random.choice(enemy.quip))
                if enemy.health <= 0:
                    print("       ")
                    print("**** You won!!! ****")
                    print("       ")
                    zonemap[myPlayer.location]["ENCOUNTERS"] -= 1
                    break
            elif a == "heal":
                player.use_potion()  # Einbindung neuer Methode
            elif a == "flee":
                if random.random() < 0.6:  # 60% Fluchchance (fix? Future-Feature)
                    flee = 1
                    break
                else:
                    print("Your enemy won't let you go!")
            elif a == "show stats":
                myPlayer.show_stats()
            elif a == "quit":
                sys.exit()

            if random.random() < enemy.accuracy:
                print("Your enemy attacks and does " + str(enemy.strength) + " damage.")
                player.health_cur -= int(enemy.strength - (player.calc_armor() / 100))
                # Hier kommt noch player.armor dazu

                if player.health_cur <= 0:
                    speech_manipulation("You are dead . . .", 0.03)
                    print(" ")
                    time.sleep(2)
                    player.game_over = True
                    dead = 1
                    game_over()
                    break  # die Breaks sind etwas schwierig zu erklären ...
            else:
                print("Your enemy attacks.")
                # sleep(1) #dramatic pause :D
                print("Missed!")
        time.sleep(2)
        os.system("clear")
        if flee == 1 and dead == 0:
            print("You ran away. You don't get a reward.")
            break
        elif dead == 1:
            break
        else:
            if random.random() < enemy.loot_chance:  # Chance ob Loot-Drop oder nicht (abhängig von Gegner)
                loot(enemy, player)

                # gold_reward = enemy.loot_level * random.randrange(10,20)
                # player.gold += gold_reward
                # print("You get "+str(gold_reward)+" gold.")

                # player.getEP(enemy.ep_drop) #Versuch deine Player.methoden einzubinden
                # print("You get "+str(enemy.ep_drop)+" experience.")
            else:
                print("Looks like you got nothing...")

            print("You get " + str(
                enemy.ep_drop) + " experience.")  # Ich dachte vielleicht sollte man bei einem Sieg immer EP bekommen?
            time.sleep(2)
            player.get_ep(enemy.ep_drop)  # Versuch deine Player.methoden einzubinden
        time.sleep(2)
        os.system("clear")
        break
    return dead  # das war für meinen game_loop nötig, kann vermutlich weg


def loot(enemy, player):
    if random.random() < 0.70:
        g = random.choice([weapon.Weapon(enemy.loot_level), weapon.Armor(enemy.loot_level)])
        if g.obj_type == "weapon":
            print("You find: " + g.name)
            print("Damage: " + str(g.damage))
            print("Would you like to swap your weapon? (y/n)\n")
            ant = input("> ")
            print(" ")
            if ant.lower()[0] in ["y", ""]:
                # player.getObject(player.weapon) #aktuelle Waffe ins Inventar
                player.get_weapon(g)  # neue Waffe = aktuelle Waffe
            elif ant.lower()[0] == "n":
                player.get_object(g)  # Waffe ins Inventar
        elif g.obj_type == "armor":
            print("You find: " + g.name)
            print("Protection: " + str(g.protection))
            print("Slot: " + g.slot)
            print("Would you like to swap your armor? (y/n)\n")
            ant = input("> ")
            print("")
            if ant.lower()[0] in ["y", ""]:
                # player.getObject(player.weapon) #aktuelle Waffe ins Inventar
                player.get_armor(g)  # neue Waffe = aktuelle Waffe
            elif ant.lower()[0] == "n":
                player.get_object(g)  # Waffe ins Inventar
    else:
        print("You find a potion.")
        player.get_potion(1)


def fight_options():
    print("Choose: attack, heal, flee\n")
    ant = input("> ")
    os.system("clear")
    return ant


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


def promt():
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
                            "use potion", "show inventory", "inventory", "show stats", "stats"]

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
        myPlayer.getCorn()
    elif action.lower() in ["heal", "healing", "potion", "use potion"]:
        myPlayer.use_potion()
    elif action.lower() in ["show inventory", "inventory"]:
        myPlayer.print_inventory()
    elif action.lower() in ["show stats", "stats"]:
        myPlayer.show_stats()


def player_move():
    dest = input("Where do you like to move to? ('up', 'down', 'left', 'right')\n> ")

    while dest not in ['up', 'down', 'left', 'right']:
        print("Invalid entry!")
        dest = input("Where do you like to move to? ('up', 'down', 'left', 'right')\n> ")

    if dest.lower() == "up":
        if zonemap[myPlayer.location]["UP"] != "":
            destination = zonemap[myPlayer.location]["UP"]
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "down":
        if zonemap[myPlayer.location]["DOWN"] != "":
            destination = zonemap[myPlayer.location]["DOWN"]
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "right":
        if zonemap[myPlayer.location]["RIGHT"] != "":
            destination = zonemap[myPlayer.location]["RIGHT"]
            movement(destination)
        else:
            stay(dest)
    elif dest.lower() == "left":
        if zonemap[myPlayer.location]["LEFT"] != "":
            destination = zonemap[myPlayer.location]["LEFT"]
            movement(destination)
        else:
            stay(dest)


def movement(destination):
    myPlayer.location = destination
    print("You have moved to the " + zonemap[myPlayer.location]["ZONENAME"] + ".")
    time.sleep(3)
    os.system("clear")
    # if not zonemap[myPlayer.location]["SOLVED"] and zonemap[myPlayer.location][ENC_POS]:
    #     pass # muss dann weg
    # Hier würde dann die Ecounter Funktion rein passen denke ich.
    # Und nach dem Encounter dann:

    # zonemap[myPlayer.location]["SOLVED"_ENCOUNTER_COUNT] += 1
    # if zonemap[myPlayer.location]["SOLVED"_ENCOUNTER_COUNT] == 2:
    #     zonemap[myPlayer.location]["SOLVED"] = True
    #     "SOLVED"_places[myPlayer.location] = True


def stay(direct):
    directions = {"up": "north", "down": "south", "left": "west", "right": "east"}
    print("You cannot move further " + directions[direct] + ".")
    time.sleep(3)
    os.system("clear")


def player_examine():
    if zonemap[myPlayer.location]["ENCOUNTERS"] > 0:
        # poss = []
        # if zonemap[myPlayer.location][POSSIBILITIES]:
        # poss = zonemap[myPlayer.location][POSSIBILITIES]
        # else:
        #     poss = POSSIBILITIES # global
        fight(myPlayer, zonemap[myPlayer.location]["POSSIBILITIES"])

    if zonemap[myPlayer.location]["SOLVED"] == True:
        print("You have already been here.")
        print(zonemap[myPlayer.location]["EXAMINATION"])
        time.sleep(3)
        os.system("clear")
    else:
        print(zonemap[myPlayer.location]["EXAMINATION"])
        zonemap[myPlayer.location]["SOLVED"] = True
        if all(solved_places.values()):
            myPlayer.game_over = True
        time.sleep(3)
        os.system("clear")


def intro():
    os.system("clear")
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
    os.system("clear")
    # print("Made by laeberkaes")
    # print("Hit me "UP" at: https://github.com/laeberkaes/ or @laeberkaes:uraltemorla.xyz")
    #
    # time.sleep(5)
    sys.exit()


def game_over():
    os.system("clear")
    speech_manipulation("Ouh there you are again.\n", 0.05)
    speech_manipulation(
        "Don't understand me wrong. This is no surprise for me. Maybe you have more luck in your next reincarnation.\n",
        0.05)
    speech_manipulation("Have a good day. :)", 0.07)
    time.sleep(2)
    sys.exit()


def game_loop():
    while not myPlayer.game_over:
        promt()


def speech_manipulation(text, speed):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def setup_game():
    os.system("clear")
    question1 = "Hello what's your name?\n"
    speech_manipulation(question1, 0.05)
    print("")
    myPlayer.name = input("> ").lower()

    os.system("clear")

    classes = ["warrior", "mage", "rogue"]
    question2 = "What Class do you want to play? (Warrior, Mage, Rogue)\n"
    speech_manipulation(question2, 0.01)
    print("")
    player_class = input("> ").lower()
    print("")
    if player_class.lower() in classes:
        myPlayer.play_class = player_class
        print("You are now " + player_class)
        time.sleep(1.5)
    else:
        while player_class.lower() not in classes:
            print("No valid class.\n")
            player_class = input("> ").lower()
        if player_class.lower() in classes:
            myPlayer.play_class = player_class
            print("You are now " + player_class)
            time.sleep(1.5)

    if myPlayer.play_class == "warrior":
        myPlayer.health_max = 120
        myPlayer.health_cur = 120
        myPlayer.mp = 20
    elif myPlayer.play_class == "mage":
        myPlayer.health_max = 80
        myPlayer.health_cur = 80
        myPlayer.mp = 80
    elif myPlayer.play_class == "rogue":
        myPlayer.health_max = 100
        myPlayer.health_cur = 100
        myPlayer.mp = 40

    # intro()

    os.system("clear")
    print("#" * screen_width + "\n")
    print("#" + (" " * int((screen_width - 2 - len("Let's start now")) / 2)) + "Let's start now" + (
            " " * int((screen_width - 2 - len("Let's start now")) / 2)) + "#\n")
    print("#" * screen_width + "\n")

    game_loop()

    end_screen()


if __name__ == "__main__":
    title_screen()

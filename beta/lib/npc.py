import random
import time

from lib.ascii import print_blacksmith
from lib.game_object import Weapon, Armor
from lib.static import screen_width, clear, speech_manipulation


class NPC:
    def __init__(self, health, strength):
        self.health = health * random.randrange(10, 21)
        self.strength = strength * random.randrange(5, 11)
        self.active_effect = []

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


class Blacksmith():
    def __init__(self, player):
        self.greeting = ["Welcome, traveller. How may I help you?",
                         "Hey! You. Get over here. How about a nice new sword for you?",
                         "Oi! You have some coin to spend?"]
        self.inventory = []
        self.set_inventory(player)  # Auslage wird erstellt
        self.gold = random.randrange(150, 301)  # Gold für Ankäufe
        clear()
        print_blacksmith()
        print(random.choice(self.greeting))
        self.decision(player)  # Interaktion mit blacksmith wird gestartet

    def decision(self, player):
        print("Do you want to 'buy', 'sell' or 'repair' something? Or you can 'go' if you cannot afford my goods.")
        a = input("> ")
        while a.lower() not in ["buy", "sell", "go", "repair", "quit"]:
            print("What? I didn't catch that.")
            self.decision(player)
        if a.lower() == "buy":
            self.buy_inventory(player)
        elif a.lower() == "sell":
            self.sell_inventory(player)
        elif a.lower() == "repair":
            self.repair(player)
        elif a.lower() in ["go", "quit"]:
            print("Well in the moment you came in I saw, that you are a poor guy. Now get out of here.")
            time.sleep(2)

    def set_inventory(self, player):  # Auslage wird erstellt
        lvl = player.level
        for i in range(3):  # blacksmith bekommt 3 Gegenstände
            if random.random() < 0.6:  # 60% Chance auf Waffe in der Auslage, 50:50 besser?
                self.inventory.append(Weapon(lvl))
            else:
                self.inventory.append(Armor(lvl))

    def buy_inventory(self, player):
        clear()
        print("#" * screen_width)
        for i in range(3):
            o = self.inventory[i]
            if o.obj_type == "weapon":
                m = o.obj_type + ": " + o.name + ", damage: " + str(o.damage) + " " * (screen_width - (11 + len(
                    o.obj_type + ": " + o.name + ", damage: " + str(
                        o.damage)))) + "#\n" + "#" + " " * 10 + ">> Price: " + str(o.value) + " <<" + " " * (
                            screen_width - (12 + len(">> Price: " + str(o.value) + " <<"))) + "#"
            else:
                m = o.obj_type + ": " + o.name + " for your " + o.slot + ", protection: " + str(o.protection) + " " * (
                        screen_width - (11 + len(
                    o.obj_type + ": " + o.name + " for your " + o.slot + ", protection: " + str(
                        o.protection)))) + "#" + "\n" + "#" + " " * 10 + ">> Price: " + str(
                    o.value) + " <<" + " " * (screen_width - (12 + len(">> Price: " + str(o.value) + " <<"))) + "#"
            print("#" + " " * 6 + str(i + 1) + ". " + m)
        print("#" * screen_width)  # TODO Hannes, mach das schön! :D
        print(" ")
        print("Which one do you want? ('1', '2', '3', 'nothing')")
        valid_input = ["1", "2", "3", "nothing"]
        a_capital = input("> ")
        a = a_capital.lower()  # Workaround fürs debuggen
        auswahl = -1  # Hilfsmittel :D
        while a not in valid_input:
            print("Please give me a normal answer, stranger.")
            self.buy_inventory(player)
        if a == "1":
            auswahl = 0
        elif a == "2":
            auswahl = 1
        elif a == "3":
            auswahl = 2
        elif a == "nothing":  # oder direkt else, für die Lesbarkeit aber noch so
            print("Well, why do you waste my time then?")

        if auswahl >= 0:
            if self.inventory[auswahl] != " ":
                if player.gold > self.inventory[auswahl].value:
                    print("So you want the " + self.inventory[auswahl].name + ". Are you sure? ('y'/'n')")
                    ax = input()
                    a2 = ax.lower()  # debug workaround

                    if a2 == "y":  # der eigentliche Kauf
                        if self.inventory[auswahl].obj_type == "weapon":
                            player.get_weapon(self.inventory[auswahl], p=False)
                            player.equip_weapon(self.inventory[auswahl])
                        else:
                            player.get_armor(self.inventory[auswahl], p=False)
                            player.equip_armor(self.inventory[auswahl])

                        player.gold -= self.inventory[auswahl].value  # Bezahlvorgang
                        self.inventory[
                            auswahl] = " "  # Inventarslot wird geleert. Man könnte auch direkt nen neuen Gegenstand rein, aber weiß nich ob das so cool ist :D
                    else:  # Quasi if a2 == "n" oder was anderes
                        (print("Your loss."))
                        self.buy_inventory(player)
                else:
                    print("You don't have the coin for that!")
                    self.buy_inventory(player)
            else:
                print("I got nothing there for you.")
                self.buy_inventory(player)
        time.sleep(2)
        clear()

    def sell_inventory(self, player):
        clear()
        player.print_inventory(interactive=True)
        print("What do you want to sell? ('weapon', 'armor'): ")
        sell = input("> ")

        while sell.lower() not in ["weapon", "armor"]:
            print("Please write 'weapon' or 'armor'")
            sell = input("> ")

        clear()
        if sell.lower() == "weapon":
            print("#" * screen_width, end="\n\n")
            for num, weapon in enumerate(player.inventory["weapons"]):
                if not weapon.equipped:
                    print(" " * 5 + str(num + 1) + " " + weapon.name + " with " + str(
                        weapon.durability[0] / weapon.durability[1] * 100) + "% of durability.")
                    print(" " * 9 + "~~ Value: " + str(weapon.value) + " Gold ~~", end="\n\n")
                else:
                    print(" " * 5 + str(num + 1) + " --> >>UNSELLABLE<< " + weapon.name + " with " + str(
                        weapon.durability[0] / weapon.durability[1] * 100) + "% of durability.", end="\n\n")
            print("#" * screen_width, end="\n\n")
            print("Which one do you want to sell? (number):")
            select = input("> ")

            if not player.inventory["weapons"][int(select) - 1].equipped:
                if self.gold - player.inventory["weapons"][int(int(select) - 1)].value >= 0:
                    print("You get " + str(player.inventory["weapons"][int(int(select) - 1)].value) + " Gold.")
                    player.gold += player.inventory["weapons"][int(int(select) - 1)].value
                    player.drop_weapon(player.inventory["weapons"][int(select) - 1])
                else:
                    print("Oh thats to much gold for me. Come again later.")
                    time.sleep(2)
                    self.decision(player)
            else:
                print("Oh unfortunately this weapon is equipped and you cannot sell it.")
                self.decision(player)

        elif sell.lower() == "armor":
            print("#" * screen_width, end="\n\n")
            for num, armor in enumerate(player.inventory["armor"]):
                if not armor.equipped:
                    print(" " * 5 + str(num + 1) + " --> " + armor.name + " for your " + armor.slot + " with " + str(
                        armor.durability[0] / armor.durability[1] * 100) + "% of durability.")
                    print(" " * 9 + "~~ Value: " + str(armor.value) + " Gold ~~", end="\n\n")
                else:
                    print(" " * 5 + str(
                        num + 1) + " --> >>UNSELLABLE<< " + armor.name + " for your " + armor.slot + " with " + str(
                        armor.durability[0] / armor.durability[1] * 100) + "% of durability.", end="\n\n")
            print("#" * screen_width, end="\n\n")
            print("Which one do you want to sell? (number):")
            select = input("> ")

            if not player.inventory["armor"][int(select) - 1]:
                if self.gold - player.inventory["armor"][int(int(select) - 1)].value >= 0:
                    print("You get " + str(player.inventory["armor"][int(int(select) - 1)].value) + " Gold.")
                    player.gold += player.inventory["armor"][int(int(select) - 1)].value
                    player.drop_armor(player.inventory["armor"][int(select) - 1])
                    time.sleep(2)
                    self.decision(player)
                else:
                    print("Oh thats to much gold for me. Come again later.")
                    time.sleep(2)
                    self.decision(player)
            else:
                print("Oh unfortunately this armor is equipped and you cannot sell it.")
                time.sleep(2)
                self.decision(player)

    def repair(self, player):
        clear()
        player.print_inventory(interactive=True)
        print("What do you want to repair? ('weapon', 'armor'): ")
        sell = input("> ")

        while sell.lower() not in ["weapon", "armor"]:
            print("Please write 'weapon' or 'armor'")
            sell = input("> ")

        clear()
        if sell.lower() == "weapon":
            print("#" * screen_width, end="\n\n")
            for num, weapon in enumerate(player.inventory["weapons"]):
                if weapon.durability[0] < weapon.durability[1]:
                    print(" " * 5 + str(num + 1) + " " + weapon.name + " with " + str(
                        weapon.durability[0] / weapon.durability[1] * 100) + "% of durability.")
                    print(" " * 9 + "~~ Cost: " + str(int(weapon.value * .25)) + " Gold ~~", end="\n\n")
                else:
                    print(" " * 5 + str(num + 1) + " --> >>FULL DURABILITY<< " + weapon.name + " with " + str(
                        weapon.durability[0] / weapon.durability[1] * 100) + "% of durability.", end="\n\n")
            print("#" * screen_width, end="\n\n")
            print("Which one do you want to repair? (number):")
            select = input("> ")

            if player.inventory["weapons"][int(select) - 1].durability[0] < \
                    player.inventory["weapons"][int(select) - 1].durability[1]:
                if player.gold - int(player.inventory["weapons"][int(int(select) - 1)].value * .25) >= 0:
                    print("This costs you " + str(
                        int(player.inventory["weapons"][int(int(select) - 1)].value * .25)) + " Gold.")
                    player.gold -= int(player.inventory["weapons"][int(int(select) - 1)].value * .25)
                    player.inventory["weapons"][int(select) - 1].durability[0] = \
                        player.inventory["weapons"][int(select) - 1].durability[1]
                    time.sleep(2)
                else:
                    print("Oh this seems to be too expensive for a poor guy like you.")
                    time.sleep(2)
                    self.decision(player)
            else:
                print("This weapon is in shape. No need to repair..")
                self.decision(player)

        elif sell.lower() == "armor":
            print("#" * screen_width, end="\n\n")
            for num, armor in enumerate(player.inventory["armor"]):
                if armor.durability[0] < armor.durability[1]:
                    print(" " * 5 + str(num + 1) + " --> " + armor.name + " for your " + armor.slot + " with " + str(
                        armor.durability[0] / armor.durability[1] * 100) + "% of durability.")
                    print(" " * 9 + "~~ Cost: " + str(int(armor.value * .25)) + " Gold ~~", end="\n\n")
                else:
                    print(" " * 5 + str(
                        num + 1) + " --> >> FULL DURABILITY<< " + armor.name + " for your " + armor.slot + " with " + str(
                        armor.durability[0] / armor.durability[1] * 100) + "% of durability.", end="\n\n")
            print("#" * screen_width, end="\n\n")
            print("Which one do you want to repair? (number):")
            select = input("> ")

            if player.inventory["armor"][int(select) - 1].durability[0] < \
                    player.inventory["armor"][int(select) - 1].durability[1]:
                if player.gold - int(player.inventory["weapons"][int(int(select) - 1)].value * .25) >= 0:
                    print("This costs you " + str(
                        int(player.inventory["armor"][int(int(select) - 1)].value * .25)) + " Gold.")
                    player.gold -= int(player.inventory["armor"][int(int(select) - 1)].value * .25)
                    player.inventory["armor"][int(select) - 1].durability[0] = \
                        player.inventory["armor"][int(select) - 1].durability[1]
                    time.sleep(2)
                else:
                    print("Oh this seems to be too expensive for a poor guy like you.")
                    time.sleep(2)
                    self.decision(player)
            else:
                print("This armor is in shape. No need to repair..")
                self.decision(player)


class Magician():
    def __init__(self, player):
        self.inventory = list()
        self.symbol = """         /^\ \n    /\   "V"\n   /__\   I\n  //..\\\  I\n  \].`[/  I\n  /l\/j\  (]\n /. ~~ ,\/I\n \\\L__j^\/I\n  \/--v}  I\n  |    |  I\n  |    |  I\n  |    l  I\n_/j  L l\_!"""
        self.greeting = ["Who dares knocking at my door? Go away.", "Chrrr... Zzzzz... Huh?",
                         "Raven eyes and kitten pee, I wish my wife had not left me..."]
        print(self.symbol, sep="\n")
        print(random.choice(self.greeting))
        self.set_inventory(player)
        self.teach_magic(player)

    def set_inventory(self, player):
        i = 0
        while i < 3:
            s = Spell(player)
            if s not in self.inventory:
                self.inventory.append(s)
                i += 1  # sorgt für 3 verschiedene spells, damit kein dict.key identisch ist

    def teach_magic(self, player):
        self.show_inventory()
        valid_choices = ["1", "2", "3", "nothing"]
        print("Do you want to learn something? (1,2,3,nothing)")
        a = str(input("> ")).lower()
        while a not in valid_choices:
            print("What did you call me??")
            a = str(input("> ")).lower()
        choice = -1
        if a == "1":
            choice = 0
        elif a == "2":
            choice = 1
        elif a == "3":
            choice = 2
        else:  # a == "nothing"
            print("Then leave me alone...")
        if choice >= 0:
            if player.gold > self.inventory[choice].value:
                print("Ah, yes. " + self.inventory[choice].name + ". Are you sure? (y/n)")
                b = str(input("> ")).lower()
                if b == "y":
                    player.spells.append(self.inventory[choice])
                    print("You learned " + self.inventory[choice].name + ".")
                    player.gold -= self.inventory[choice].value
                else:
                    print("Coward. Are you afraid of the dark arts?... I mean, magic?")
            else:
                print("Come again, when you can pay me.")

    def show_inventory(self):
        print("#" * screen_width)
        print("I can teach you the ancient arts of destruction and creation... for a price.")
        print(" ")
        for spell in self.inventory:
            if spell.status_effect == "healing":
                print("Name: " + spell.name + "    Healing: " + str(
                    spell.damage) + "    Effect: " + spell.status_effect + "\n Price: " + str(spell.value))
                print(" ")
            else:
                print("Name: " + spell.name + "    Damage: " + str(
                    spell.damage) + "    Effect: " + spell.status_effect + "\n Price: " + str(spell.value))
            print(" ")
        print("#" * screen_width)


class Spell():
    def __init__(self, player):
        self.element_type = random.choice(["Fire", "Earth", "Ice", "Water", "Air"])
        self.damage = random.randrange(10, 20) * player.level
        self.name = ""
        self.status_effect = ""
        self.status_chance = 0
        self.status_damage = 0
        self.status_duration = 0
        self.spell_activated = False
        self.status_description = ""
        self.set_spell(self.element_type, player)
        self.mana_cost = 10  # erst mal fix, später im balancing (#TODO)
        self.value = random.randrange(50, 100) * player.level

    def set_spell(self, element_type, player):
        element_type = self.element_type
        if element_type == "Fire":
            self.name = random.choice(["Firestorm", "Fireball", "Flamewall"])
            x = random.randrange(0, 2)
            self.status_effect = ["lingering fire", "severe burn"][x]
            self.status_description = ["Your enemy is burning.", "Your enemy was burnt."][x]
            self.status_chance = [0.5, 0.4][x]
            self.status_damage = [5, 10][x] * player.level
            self.status_duration = [3, 1][x]
        elif element_type == "Earth":
            self.name = random.choice(["Rock Slide", "Meteor", "Boulder"])
            x = random.randrange(0, 2)
            self.status_effect = ["bleeding", "knockout"][x]
            self.status_description = ["Your enemy is bleeding.", "Your enemy was knocked out."][x]
            self.status_chance = [0.5, 0.3][x]
            self.status_damage = [7, 0][x] * player.level
            self.status_duration = [3, 1][x]
        elif element_type == "Ice":
            self.name = random.choice(["Avalanche", "Ice Crystal", "Freeze"])
            self.status_effect = "freezing"
            self.status_description = "Your enemy is frozen."
            self.status_chance = 0.3
            self.status_damage = 0
            self.status_duration = 1
        elif element_type == "Water":
            self.name = random.choice(["Wave", "Water Blast", "Heavy Rain"])
            self.status_effect = random.choice(["drowning", "soaking"])
            x = random.randrange(0, 2)
            self.status_effect = ["drowning", "soaking"][x]
            self.status_description = ["Your enemy can't breath.", "Your enemy is soaking wet."][x]
            self.status_chance = [0.4, 0.5][x]
            self.status_damage = [8, 6][x] * player.level
            self.status_duration = [2, 2][x]
        elif element_type == "Air":
            self.name = random.choice(["Healing winds", "Soft Breeze", "Gentle Blow"])
            self.status_effect = random.choice(["healing"])
            x = random.randrange(0, 3)
            self.damage = [20, 30, 40][x]
            self.value = [100, 150, 200][x]


class Trickster():
    def __init__(self, player):
        self.setup_game(player)

    def setup_game(self, player):
        speech_manipulation("Hello stranger. Care for a round of the shell game?\n", 0.05)
        time.sleep(0.3)
        speech_manipulation(
            "The rules are simple. One ball, three cups. You tell me where the ball is and I pay you money.\n", 0.05)
        time.sleep(0.3)
        speech_manipulation("If you lose, you pay me.\n", 0.05)
        time.sleep(0.3)
        speech_manipulation("Do you want to play?\n", 0.05)
        a = str(input("> ")).lower()
        if a in ["yes", "y"]:
            speech_manipulation("Alright! Place your bet.\n", 0.05)
            time.sleep(0.3)
            speech_manipulation("How much do you want to play for? If you win, I'll double it.\n", 0.05)
            amount = input("> ")
            while not all([c in "0123456789" for c in amount]):
                speech_manipulation("You should give me an amount of gold you want to bet?\n", 0.05)
                amount = input("> ")
            # try:
            #     amount = int(input("> "))
            # except ValueError:
            #     print("Tell me, how much money do you want to bet?")
            amount = int(amount)
            if amount > 0:
                if amount > player.gold:
                    speech_manipulation("Sorry, your coin purse seems a little light for such a bet.\n", 0.05)
                    time.sleep(1)
                else:
                    speech_manipulation("Okay, here we go.\n", 0.05)
                    win = self.play_game(player)
                    if win > 0:
                        player.gold += amount
                        speech_manipulation("You get " + str(amount) + " gold from me. Be sure to play again.\n", 0.05)
                        time.sleep(2)
                    else:
                        player.gold -= amount
                        speech_manipulation("Thanks for the money, sucker!\n", 0.05)
                        time.sleep(2)
            else:
                speech_manipulation("Not funny.\n", 0.05)
        else:
            speech_manipulation("Really? Well then... See you around.\n", 0.05)

    def play_game(self, player):
        print("Watch the ball!")
        time.sleep(0.5)
        clear()
        self.print_animation()
        print("Could you follow? Tell me, under which cup is the ball? (left, middle, right)")
        a = str(input("> ")).lower()
        valid_options = ["left", "middle", "right"]
        while a not in valid_options:
            print("Come on... play the game!")
            a = str(input("> ")).lower()
        x = random.randint(1, 3)
        if x == 1:
            position = "left"
        elif x == 2:
            position = "middle"
        elif x == 3:
            position = "right"

        if a == position:
            print("Not bad, you got it right.")
            self.result(x)
            return 1
        else:
            print("Sorry, no luck this time.")
            self.result(x)
            return 0

    def print_animation(self):
        cups_opened = "    .-------.           .-------.           .-------.\n   /         \         /         \         /         \\\n  /           \       /           \       /           \\\n ;    _ _ _    ;     ;    _ _ _    ;     ;    _ _ _    ;\n .-' `     ' '-.     .-' ` _._ ' '-.     .-' `     ' '-.\n(               )   (    .'--.`.    )   (               )\n `-=.._____..--'     `-=.|  .' |.--'     `-=.._____..--'\n                          `--`'"
        cups_closed = "        ____             ____             ____\n     ,,:____:,,       ,,:____:,,       ,,:____:,,\n    /          \     /          \     /          \\\n   ;            ;   ;            ;   ;            ;\n   |            |   |            |   |            |\n   ;            ;   ;            ;   ;            ; \n    '-.,____,.-'     '-.,____,.-'     '-.,____,.-'"
        shuffle_left = "                              ____\n                           ,,:____:,,\n        ____              /          \\\n     ,,:____:,,          ;            ;\n    /          \         |            |\n   ;            ;        ;        ____;\n   |            |         '-.,_,,:____:,,\n   ;            ;             /          \\\n    '-.,____,.-'             ;            ;\n                             |            |\n                             ;            ;\n                              '-.,____,.-'"
        shuffle_left2 = "                              ____\n                           ,,:____:,,\n        ____              /          \\\n     ,,:____:,,          ;            ;\n    /          \         |            |\n   ;            ;    ____;            ;\n   |            | ,,:____:,,.,____,.-'\n   ;            ;/          \\\n    '-.,____,.-';            ;\n                |            |\n                ;            ;\n                 '-.,____,.-'"
        shuffle_right = "                 ____\n              ,,:____:,,                  ____\n             /          \              ,,:____:,,\n            ;            ;            /          \\\n            |            |           ;            ;\n            ____         ;           |            |\n         ,,:____:,,__,.-'            ;            ;\n        /          \                  '-.,____,.-'\n       ;            ;\n       |            |\n       ;            ;\n        '-.,____,.-'"
        shuffle_right2 = "                 ____\n              ,,:____:,,                  ____\n             /          \              ,,:____:,,\n            ;            ;            /          \\\n            |            |           ;            ;\n            ;            ____        |            |\n             '-.,____,,,:____:,,     ;            ;\n                     /          \     '-.,____,.-'\n                    ;            ;\n                    |            |\n                    ;            ;\n                     '-.,____,.-'"

        self.box_print(cups_opened, 1.0)
        self.box_print(cups_closed, 1.0)
        self.box_print(shuffle_left, 0.5)
        self.box_print(cups_closed, 0.5)
        self.box_print(shuffle_right, 0.5)
        self.box_print(cups_closed, 0.5)
        self.box_print(shuffle_left, 0.2)
        self.box_print(shuffle_left2, 0.2)
        self.box_print(shuffle_right, 0.2)
        self.box_print(shuffle_right2, 0.2)
        for i in range(4):
            self.box_print(shuffle_left, 0.1)
            self.box_print(shuffle_right2, 0.1)
            self.box_print(shuffle_left2, 0.1)
            self.box_print(shuffle_right, 0.1)
        print(cups_closed)

    def box_print(self, message, x):
        print("#" * 70)
        print(" ")
        print(" ")
        print(message)
        print(" ")
        print(" ")
        print("#" * 70)
        time.sleep(x)
        clear()

    def result(self, x):
        ball_left = "    .-------.            ____             ____\n   /         \        ,,:____:,,       ,,:____:,,\n  /           \      /          \     /          \\\n ;    _ _ _    ;    ;            ;   ;            ;\n .-' ` _._ ' '-.    |            |   |            |\n(    .'--.`.    )   ;            ;   ;            ;\n `-=.|  .' |.--'     '-.,____,.-'     '-.,____,.-'\n      `--`'"
        ball_middle = "        ____            .-------.            ____\n     ,,:____:,,        /         \        ,,:____:,,\n    /          \      /           \      /          \\\n   ;            ;    ;    _ _ _    ;    ;            ;\n   |            |    .-' ` _._ ' '-.    |            |\n   ;            ;   (    .'--.`.    )   ;            ; \n    '-.,____,.-'     `-=.|  .' |.--'     '-.,____,.-'\n                          `--`' "
        ball_right = "        ____             ____            .-------.\n     ,,:____:,,       ,,:____:,,        /         \\\n    /          \     /          \      /           \\\n   ;            ;   ;            ;    ;    _ _ _    ;\n   |            |   |            |    .-' ` _._ ' '-.\n   ;            ;   ;            ;   (    .'--.`.    )\n    '-.,____,.-'     '-.,____,.-'     `-=.|  .' |.--'\n                                           `--`'"
        if x == 1:
            print(ball_left)
        elif x == 2:
            print(ball_middle)
        elif x == 3:
            print(ball_right)


class RPSMan:
    def __init__(self, player):
        self.setup(player)

    def setup(self, player):
        print("Hello there. Do you want to make some money?")
        time.sleep(0.5)
        speech_manipulation("How about a round of rock, paper, scissors?\n", 0.05)
        a = str(input("> ")).lower()
        while a not in ["yes", "no"]:
            print("What did you say?")
            a = str(input("> ")).lower()
        if a == "yes":
            clear()
            speech_manipulation("Alright! Place your bet.\n", 0.05)
            time.sleep(0.3)
            speech_manipulation("How much do you want to play for? If you win, I'll double it.\n", 0.05)
            amount = input("> ")
            while not all([c in "0123456789" for c in amount]):
                speech_manipulation("You should give me an amount of gold you want to bet?\n", 0.05)
                amount = input("> ")
            amount = int(amount)
            if amount > 0:
                if amount > player.gold:
                    print("Sorry mate, you don't have the bank for that.")
                else:
                    speech_manipulation("Alright.", 0.05)
                    win = self.play_rps()
                    if win == 1:
                        speech_manipulation("You won! Not bad.\n", 0.05)
                        time.sleep(0.5)
                        print("Here is your reward!")
                        speech_manipulation("You earn " + str(amount) + " Gold.", 0.05)
                        player.gold += amount
                        time.sleep(2)
                    elif win == 2:
                        speech_manipulation("Oh. A tie.\n", 0.05)
                        print("Well, no luck for both of us.")
                        time.sleep(2)
                    else:
                        speech_manipulation("You lose... Better luck next time!\n", 0.05)
                        time.sleep(0.5)
                        print("Pay your bet!")
                        player.gold -= amount
                        time.sleep(2)
            else:
                print("Try again...")

    def play_rps(self):
        rock_left = """    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
        """
        rock_right = """  _______
 (____   '---
(_____)
(_____)
 (____)
  (___)__.---
"""
        paper_left = """    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)"""
        paper_right = """       _______
  ____(____   '---
 (______
(_______
 (_______
   (__________.---"""
        scissors_left = """    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)"""
        scissors_right = """       _______
  ____(____   '---
 (______
(__________
      (____)
       (___)__.---"""
        clear()
        print("Choose your symbol: (rock, paper, scissors)")
        choice = str(input("> ")).lower()
        while choice not in ["rock", "paper", "scissors"]:
            print("Choose a valid answer.")
            choice = str(input("> ")).lower()
        print("ROCK")
        time.sleep(0.8)
        print("PAPER")
        time.sleep(0.8)
        print("SCISSORS")
        time.sleep(0.8)
        clear()
        own_choice = random.choice(["rock", "paper", "scissors"])
        print("Your choice:                              Opponent's choice:")
        print("    " + choice + "                                   " + own_choice)
        if choice == "rock":
            print(rock_left)
        elif choice == "paper":
            print(paper_left)
        else:
            print(scissors_left)
        if own_choice == "rock":
            print(rock_right)
        elif own_choice == "paper":
            print(paper_right)
        else:
            print(scissors_right)
        winning_combinations = [("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")]
        losing_combinations = [("rock", "paper"), ("paper", "scissors"), ("scissors", "rock")]
        tie_combinations = [("scissors", "scissors"), ("rock", "rock"), ("paper", "paper")]
        for combination in winning_combinations:
            if combination[0] == choice and combination[1] == own_choice:
                return 1
        for combination in losing_combinations:
            if combination[0] == choice and combination[1] == own_choice:
                return 0
        for combination in tie_combinations:
            if combination[0] == choice and combination[1] == own_choice:
                return 2

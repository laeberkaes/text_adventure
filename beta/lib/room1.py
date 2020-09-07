from lib.static import screen_width, clear, speech_manipulation, confirmation
import random
import time

#for Testing: ---------------
class P():
    def __init__(self):
        self.name = "Testy McTesterton"
        self.location = "a2"
#end Testing: ---------------

class Room1():
    def __init__(self, player):
        self.intro(player) #comment out for quicker testing
        self.story_setup() #comment out for quicker testing
        self.solved = False
        self.clues_found = 0
        self.found_objects = []
        self.inventory = []
        t = Table()
        n = Notebook()
        c = Chair()
        d = Door()
        dr = Drawer()
        p = PieceOfPaper()
        b = Book()
        cu = Cupboard()
        self.objects = [t, n, c, d, dr, p, b, cu]
        self.turnable = [n, c, p, b]
        self.breakable = [c]
        self.openable = [dr, d, cu]
        while not self.solved:
            self.room_prompt()
        print("You are free. You walk around a bit and find your way to your house.")
        player.location = "b2"

    def push_obj(self,l):
        if l[0] not in self.found_objects:
            self.found_objects += l

    def get_obj(self,o):
        if o not in self.inventory:
            self.inventory.append(o)

    def intro(self, player):
        print("Hey!", end = " ")
        time.sleep(1)
        print(" " + player.name)
        time.sleep(1)
        speech_manipulation("Come over here for a second, I have an offer for you.", 0.08)
        time.sleep(1)
        clear()
        print("You look like a trustworthy adventure. I have a problem, you see, and I need help. My farm was raided by some bandits and I have nothing left to eat.")
        time.sleep(3)
        print("They left a note with a message. I have it in my house. Would you come take a look and help me?")
        ant = str(input("> ")).lower()
        if ant not in ["yes", "y"]:
            print("Oh. I thought you were the one to save me...")
            time.sleep(2)
        else:
            speech_manipulation("Thank you!!", 0.08)
            time.sleep(1)
            print(" ")
            speech_manipulation("** You follow the man through a narrow street. After you turn a corner everything is black!", 0.065)
            time.sleep(1)
            clear()
            time.sleep(2)

    def story_setup(self):
        #player.location = "room_1"
        speech_manipulation("** You wake up. Your head hurts like hell.\n", 0.075)
        time.sleep(1)
        speech_manipulation("** You feel your pockets. Empty.\n", 0.075)
        time.sleep(1)
        speech_manipulation("** Looks like you need to get out of here.", 0.06)
        time.sleep(1)

    def room_prompt(self):
        clear()
        print("You look around the room. You can see:")
        found = "A big wooden door, a cupboard, a table, a chair"
        for i in self.found_objects:
            found += ", "+i
        print(found)
        if self.inventory:
            print("You have:")
            have = ""
            for i in self.inventory:
                have += i + " "
            print(have)
        print("\n" + "=" * len("What would you like to do?"))
        print("What would you like to do?\n")
        print("-" * len("What would you like to do?"))
        print(" " * (int((len("What would you like to do?") - len("examine, take, put, look, etc.")) / 2)) + "examine, help, etc.")
        print("-" * len("What would you like to do?") + "\n")
        action = str(input("> ")).lower().split()
        acceptable_actions = ["help", "examine", "turn", "open", "break"]
        acceptable_objects = ["table", "chair", "door", "cupboard"] + self.found_objects
        if len(action)>0:
            while action[0] not in acceptable_actions:
                print("Unknown action. Try again.")
                action = str(input("> ")).lower().split()
        elif len(action) == 0:
            print("Unknown action. Try again.")
            action = str(input("> ")).lower().split()
        if len(action) <= 1 or len(action) > 2:
            if action[0] == "help":
                print("Try one of the following actions with an object:")
                s = ""
                for act in acceptable_actions:
                    s += " " + act + " "
                print(s)
                confirmation()
            else:
                print("Try a combination of action + object.")
                confirmation()
        else:
            if action[0] == "examine":
                if action[1] in acceptable_objects:
                    for obj in self.objects:
                        if obj.name == action[1]:
                            obj.examine(self)
                            confirmation()
                else:
                    print("There is no such object.")
                    confirmation()

            if action[0] == "turn":
                if action[1] in [o.name for o in self.turnable]:
                    for obj in self.turnable:
                        if action[1] == obj.name:
                            obj.turn(self)
                            confirmation()
                else:
                    print("You cannot turn this " + action[1])
                    confirmation()

            if action[0] == "break":
                if action[1] in [o.name for o in self.breakable]:
                    for obj in self.breakable:
                        if action[1] == obj.name:
                            obj.breaking(self)
                            confirmation()
                else:
                    print("You cannot break this " + action[1])
                    confirmation()

            if action[0] == "open":
                if action[1] in [o.name for o in self.openable]:
                    for obj in self.openable:
                        if action[1] == obj.name:
                            obj.open(self)
                            confirmation()
                else:
                    print("You cannot open this " + action[1])
                    confirmation()
        if not self.solved:
            self.room_prompt()

class Table():
    def __init__(self):
        self.name = "table"
    def examine(self, room):
        print("You see a table with a notebook on top and a big drawer.")
        room.push_obj(["notebook", "drawer"])

class Notebook():
    def __init__(self):
        self.name = "notebook"
    def turn(self,room):
        print("You turn it around. There is nothing on its back.")
    def examine(self, room):
        print("You open the notebook. You read the first lines of the notebook: 'The Earth is the Center.' A piece of paper falls out.")
        room.push_obj(["paper"])
        room.clues_found += 1

class Chair():
    def __init__(self):
        self.name = "chair"
        self.broken = False
    def examine(self, room):
        print("Looks like an old wooden chair.")#+" You can see nothing on the seat.")
    def turn(self,room):
        s = """
    +   +
  v | i | r 
+---|---|---+
  o | n | u 
+---|---|---+
  f | h | e 
    +   +
"""
        print("On the bottom of the chair you find strange markings." + s)
        room.clues_found += 1
    def breaking(self, room):
        if not self.broken:
            print("You broke the chair into pieces.")
            self.broken = True
            if "Chair Leg" not in room.inventory:
                room.get_obj("Chair Leg")
        else:
            print("It's already broken.")

class Cupboard():
    def __init__(self):
        self.name = "cupboard"
        self.combination = "2"
    def examine(self, room):
        print("An old mahagony wardrobe with big doors.")
    def open(self, room):
        combination = self.combination
        print("You carefully open the cupboard. In it you find a note.")
        print("The note says: In the language of the snake, let your machine write the **combination** to you.")
        room.clues_found += 1
        x = input("> ")
        if x[:5] != "print":
            print("Not quite the right command.")
        else:
            if len(x) != len("print(combination)"):
                print("That's it. almost there.")
            else:
                eval(x)
        #try:
        #    eval(x)
        #except:
        #    print("Not quite...")

class PieceOfPaper():
    def __init__(self):
        self.name = "paper"
    def examine(self, room):
        print("It reads: 'When the planets allign, take the third of the second, the fourth of the fifth, the last of the sixth and the first of the third.")
        room.clues_found += 1
    def turn(self,room):
        print("On its back it reads: 'M, ...'")

class Door():
    def __init__(self):
        self.name = "door"
        self.combination = "295"
    def examine(self, room):
        print("A scratched metal door with a combination look. You need three digits to open it.")
    def open(self, room):
        if room.clues_found >= 4:
            print("If you know the combination, try it now:")
            ant = str(input("> ")).lower()
            if ant == self.combination:
                speech_manipulation("** You manage to open the door with your combination!\n", 0.06)
                time.sleep(2)
                print("In the next room you find all your equipment and a note from your capturer:")
                print("'Not bad. You are not as dumb as I thought... Maybe you are useful after all. We will be in touch.'")
                i = """          ▄▀▄
        ▄▀───▀▄
      ▄▀──▄▄▄──▀▄
    ▄▀──▄▀─▄─▀▄──▀▄
  ▄▀─────▀▄▄▄▀─────▀▄
▄▀───────────────────▀▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"""
                print(i)
                room.solved = True
            else:
                print("That was not the right combination. Try again and review your clues.")
        else:
            print("Are you sure you've found enough to know the combination?")

class Drawer():
    def __init__(self):
        self.name = "drawer"
    def examine(self, room):
        print("It looks stuck. You need something to pry it open.")
    def open(self, room):
        if "Chair Leg" in room.inventory:
            print("You use the leg of the chair to open the drawer and find a book inside.")
            room.push_obj(["book"])
        else:
            print("It's stuck...")

class Book():
    def __init__(self):
        self.name = "book"
    def examine(self, room):
        print("You flip through its pages and on the last page you find a peculiar symbol: ┐ U ┘ ┌")
        room.clues_found += 1
    def turn(self,room):
        print("You turn around the book but it has nothing interesting on its back.")


#for Testing:
#p = P() 
#Room1 = Room1(p)

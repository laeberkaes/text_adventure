import weapon
import random,time,os

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
        self.location = "d2"
        self.game_over = False
        self.weapon = weapon.Weapon(self.level)
        self.potions = 1
        self.inventory = {"weapons":[self.weapon],"armor":[],"misc":dict()}
        self.gold = 10
        self.head_protect = 0
        self.chest_protect = 0
        self.leg_protect = 0
        self.arm_protect = 0

    def health(self):
        print("Deine Gesundheit: "+str(self.health_cur)+"/"+str(self.health_max))

    def levelUp(self):
        self.level += 1
        self.health_max += 20
        self.ep -= 100
        POSSIBILITIES = [POSSIBILITIES[0]-(self.level*0.05),POSSIBILITIES[1]+(self.level*0.1),POSSIBILITIES[2]+(self.level*0.05)]

    def getEP(self,amount):
        self.ep += amount
        if self.ep > 100:
            self.levelUp()

    def getWeapon(self,weapon):
        self.weapon = weapon
        self.inventory["weapons"].append(weapon)

    def getArmor(self,armor):
        self.protect(armor.slot,armor.protection)
        self.inventory["armor"].append(armor)

    def getGold(self,amount):
        self.gold += amount

    def getPotion(self,amount):
        self.potions += amount

    def usePotion(self):
        if self.potions > 0:
            self.health_cur += 25
            if self.health_cur > self.health_max:
                self.health_cur = self.health_max
            self.potions -= 1
            print("Ahhhh this feels good. You feel new power filling your up body. (HP +25)")
        else:
            print("You don't have any potions left.")
        time.sleep(2)
        os.system("clear")

    def getObject(self,object):
        if object not in self.inventory["misc"] and type(object) == str:
            self.inventory.misc[object] = 1
        elif object in self.inventory["misc"]:
            self.inventory.misc[object] += 1
        elif object.obj_type() == "weapon":
            self.inventory["weapons"].append(object)
        elif object.obj_type() == "armor":
            self.inventory["armor"].append(object)

    def protect(self,place,amount):
        if place == "head":
            self.head_protect += amount
        elif place == "chest":
            self.chest_protect += amount
        elif place == "leg":
            self.leg_protect += amount
        elif place == "arm":
            self.arm_protect += amount

    def fishing(self):
        if self.location in ["a4","c1","c2"] and "fishingrot" in self.inventory:
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
                if "corn" not in self.inventory:
                    self.inventory["corn"] = 1
                else:
                    self.inventory["corn"] += 1
            else:
                print("Baaah. You better not take this corn with you.")
        else:
            print("Well you cannot get Corn out of this place.")

        time.sleep(2)
        os.system("clear")

    def hunting(self):
        if self.location in ["b3","b4","c3","c4"]:
            p = random.random()
            if p > 0.95:
                print("You get some nice deer. This will give you good food for some days.")
                if "food" not in self.inventory:
                    self.inventory["food"] = 10
                else:
                    self.inventory["food"] += 10
            elif p > 0.6:
                print("You get some rabbits and a small boar.")
                if "food" not in self.inventory:
                    self.inventory["food"] = 7
                else:
                    self.inventory["food"] += 7
            else:
                print("Well you are out of luck for now.")
        else:
            print("You will find no wild animals in this area. Try your luck in the eastern forest.")

        time.sleep(2)
        os.system("clear")

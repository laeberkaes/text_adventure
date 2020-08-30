import random

class Weapon():
    def __init__(self, level):
        adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody", "Sharp"]
        subst = [" Dagger", " Hammer", " Sword", " Bow", " Spear", " Morning Star", " Club", " Axe"]
        self.obj_type = "weapon"
        self.level = level
        self.name = random.choice(adjective) + random.choice(subst)
        self.damage = random.randrange(3,6)*level #=> 3-5
        self.used = 0 # used in percent --> multiply with damage
        self.equiped = False

    def __repr__(self):
        return "Your weapon: "+self.name+", with "+str(self.damage)+" damage"

class Armor():
    def __init__(self,level):
        adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody"]
        subst = [" Plate Armor", " Chain Armor", " Leather Armor"]
        self.obj_type = "armor"
        self.slot = random.choice(["head","chest","leg","arm"])
        self.level = level
        self.name = random.choice(adjective) + random.choice(subst)
        self.protection = random.randrange(10,21)*level #=> 3-5
        self.equiped = False

    def __repr__(self):
        return "Your armor for the " + self.slot + ": " + self.name + ", with " + str(self.protection) + " of protection."

    def equip_armor(self,person):
            if self.slot == "head":
                person.head_protect += self.protection
            elif self.slot == "chest":
                person.chest_protect += self.protection
            elif self.slot == "leg":
                person.leg_protect += self.protection
            elif self.slot == "arm":
                person.arm_protect += self.protection

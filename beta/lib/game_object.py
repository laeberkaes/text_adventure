#import game.py
import random
class Weapon():
    def __init__(self, level):
        adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody", "Sharp"]
        subst = [" Dagger", " Hammer", " Sword", " Bow", " Spear", " Morning Star", " Club", " Axe"]
        self.obj_type = "weapon"
        self.level = level
        self.value = random.randrange(5,15)*self.level #Gold-Wiederverkaufswert
        self.name = random.choice(adjective) + random.choice(subst)
        self.damage = random.randrange(3,6)*level #=> 3-5
        self.durability = [20,20] # used in percent --> multiply with damage
        self.broken = False
        self.equipped = False

    def __repr__(self):
        return "Your weapon: "+self.name+", with "+str(self.damage)+" damage"

class Armor():
    def __init__(self,level):
        self.obj_type = "armor"  
        self.level = level
        self.equipped = False
        self.durability = [10,10] #Übersteht 10 Angriffe
        self.broken = False
        self.value = random.randrange(5,15)*self.level #Gold-Wiederverkaufswert

        #Rüstungsname wird festgelegt (und slot angezeigt)
        adjective = ["Dirty", "Crooked", "Big", "Old", "Shiny", "Bloody"]
        subst = [" Plate Armor", " Chain Armor", " Leather Armor"] #Future Feature: Typ der Rüstung erhöht Wert (Plate > Chain > Leather)
        self.name = random.choice(adjective) + random.choice(subst)

        #Rüstungsattribute werden festgelegt
        slot_names = ["head","chest","leg","arm"]
        slot_modifier = [2,3,1,1] #Rüstungswert im Verhältnis zu slot (head = 2, chest = 3, etc.). Auch zusammen als dict denkbar.
        slot_choice = random.randrange(0,len(slot_names)) #wählt Index von names und modifier
        self.slot = slot_names[slot_choice]
        self.protection = slot_modifier[slot_choice]*level


    def __repr__(self):
        return "Your armor for the " + self.slot + ": " + self.name + ", with " + str(self.protection) + " protection."
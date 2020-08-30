import weapon, random

class Enemy():
    def __init__(self,race,size,level,sounds,health=100):
        self.race = race
        self.size = size
        self.level = level
        self.weapon = weapon.get_weapon(level)
        self.health_max = health*size
        self.healt_cur = self.health_max
        self.sounds = sounds

    def makeSound(self):
        return random.choice(self.sounds)

    def attack(self):
        return self.weapon.damage

def makeEnemies(num_ogres,num_orcs,num_humans,level):
    ogres = [Enemy("Ogre",random.choice([2,3]),["Hrrgh","Aarggh","*BRÜLL*"],level) for i in range(num_ogres)]
    orcs = [Enemy("Orc", random.choice([1, 2]),["Hahahaaa","Aaaahhh","*GRUNZ*"], level) for i in range(num_orcs)]
    humans = [Enemy("Human", random.choice([1, 2]),["Das soll alles sein?","Aaaaargh","Hmmpf"],level) for i in range(num_humans)]
    return random.shuffle(ogres,orcs,humans)

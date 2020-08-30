import enemies


class Level():
    def __init__(self, player):
        self.player = player


class Level1(Level):
    def __init__(self, player):
        super().__init__(player)
        self.enemies = enemies.makeEnemies(2,1,0,1)


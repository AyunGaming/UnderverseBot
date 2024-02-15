import random

class Actor():
    def __init__(self,name,level,hp,max_hp,atk,defense,inventory):
        self.action = None
        self.isDead = False
        self.name = name
        self.level = level
        self.atk = atk
        self.defense = defense
        self.max_hp = max_hp

        if hp > self.max_hp:
            self.hp = max_hp
        else:
            self.hp = hp

        if inventory == None:
            self.inventory = {}
        else:
            self.inventory = inventory



    def attack(self,actor):
        x = random.randint(0,10)
        coef = 1
        if x >= 8:
            coef = 2
        elif x <= 1:
            coef = 0
        

        damage = round(((((( 2 * self.level )  + 2 ) * self.atk *  (self.atk / actor.defense)) / 50 ) + 2 ) * coef * round(random.uniform(0.8,1), 1))

        return int(damage)
import json
import Actors.Actor as Actor

class Enemy(Actor.Actor):
    def __init__(self,dict):

        super().__init__(dict["name"],dict["level"],dict["life"],dict["max_life"],dict["atk"],dict["def"],dict["inventory"])

        self.xp = dict["xp"]
        self.gold = dict["gold"]
        self.minlevel = dict["minlevel"]
        self.isDead = dict["isDead"]


    @staticmethod
    def getEnemy(name):
        jsonFile = open("./json/enemy.json","r")
        jsonData = json.load(jsonFile)

        enemies = jsonData["enemies"]
        
        x = 0
        for i in enemies:
            if str(name) in str(enemies[x]["name"]):
                return i
            else:
                x += 1
        return False
    
    @staticmethod
    def getAllEnemiesJson():
        jsonFile = open("json/enemy.json","r")
        jsonData = json.load(jsonFile)

        enemies = jsonData["enemies"]

        return enemies


    @staticmethod
    def getAllEnemies():
        enemies = []
        dict = Enemy.getAllEnemiesJson()
        if type(dict) == bool:
            return False
        for enemy in dict:
            e = Enemy.dictToEnemy(enemy)
            enemies.append(e)
        
        return enemies




    @staticmethod
    def dictToEnemy(dict):
        e = Enemy(dict)

        return e


    def ModifJsonSave(self):
        jsonFile = open("json/enemy.json", "r")
        jsonData = json.load(jsonFile)
        jsonFile.close()

        enemy = self.EnemyToJson()
        ## Vérification si le profil est déjà créé
        x = 0
        for data in jsonData["enemies"]:
            if data["name"] == self.name:
                enemy = {
                    "isDead": bool(self.isDead),
                    "name": str(self.name),
                    "level":self.level,
                    "max_life": self.max_hp,
                    "life":self.hp,
                    "atk":self.atk,
                    "def":self.defense,
                    "xp": self.xp,
                    "gold": self.gold,
                    "inventory":self.inventory,
                    "minlevel":self.minlevel
                }
                break
            x += 1
        jsonFile = open("json/enemy.json","w")
        jsonData["enemies"][x] = enemy
        jsonFile.seek(0)
        json.dump(jsonData, jsonFile, indent=4)
        return 1



    def EnemyToJson(self):
        jsonFile = open("json/enemy.json", "r+")
        jsonData = json.load(jsonFile)

        ## Vérification si le profil est déjà créé
        for data in jsonData["enemies"]:
            if data["name"] == self.name:
                return False


        enemy = {
            "isDead": bool(self.isDead),
            "name": str(self.name),
            "level":self.level,
            "max_life": self.max_hp,
            "life":self.hp,
            "atk":self.atk,
            "def":self.defense,
            "xp": self.xp,
            "gold": self.gold,
            "inventory":self.inventory,
            "minlevel": self.minlevel
        }
        jsonData["enemies"].append(enemy)
        jsonFile.seek(0)
        json.dump(jsonData, jsonFile, indent=4)
        
        return True
        
        

    

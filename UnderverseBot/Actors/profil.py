import json
import Actors.Actor as Actor
import math

class Profil(Actor.Actor):
    def __init__(self,name,id) -> None:

        super().__init__(name,1,100,100,15,5,{})
        self.combat = False
        self.tuto = False
        self.inFight = False
        self.id = id
        self.xp = 0
        self.max_xp = self.xpForLVLup(self.level)
        self.gold = 0


    @staticmethod
    def getProfil(id):
        dict = Profil.getProfilInJson(id)
        if type(dict) == bool:
            return False
        p = Profil.dictToProfil(dict,id)
        return p



    @staticmethod
    def getProfilInJson(id):
        jsonFile = open("json/profil.json","r")
        jsonData = json.load(jsonFile)

        profiles = jsonData["profiles"]
        
        x = 0
        for i in profiles:
            if str(id) in str(profiles[x]["id"]):
                return i
            else:
                x += 1
        return False


    @staticmethod
    def dictToProfil(dict,id):
        p = Profil(dict['name'],id)
        p.isDead = dict['isDead']
        p.xp = dict['xp']
        p.max_xp = dict['max_xp']
        p.tuto = dict['tuto']
        p.combat = dict['combat']
        p.inFight = dict['inFight']
        p.level = dict['level']
        p.max_hp = dict['max_hp']
        p.hp = dict['hp']
        p.atk = dict['atk']
        p.defense = dict['def']
        p.gold = dict['gold']
        p.inventory = dict['inventory'] 
        return p


    def xpForLVLup(self,level):
        if level == -1:
            return 0
        else:
            self.max_xp = math.floor(((50 + level) * (50 + level)) /math.pi) + self.xpForLVLup(level - 1)
            return self.max_xp
    
    def checkLVLup(self):
        if self.xp >= self.max_xp:
            self.level += 1
            self.atk += 2
            self.defense += 2
            self.xpForLVLup(self.level)
            self.modifJsonSave()
            return True
        return False



    def modifJsonSave(self):
        jsonFile = open("json/profil.json", "r")
        jsonData = json.load(jsonFile)
        jsonFile.close()

        profile = self.profilToJson()
        ## Vérification si le profil est déjà créé
        x = 0
        for data in jsonData["profiles"]:
            if data["id"] == self.id:
                profile = {
                    "id": int(self.id),
                    "tuto": bool(self.tuto),
                    "combat": bool(self.combat),
                    "inFight" : bool(self.inFight),
                    "isDead": bool(self.isDead),
                    "name": str(self.name),
                    "xp": int(self.xp),
                    "max_xp": int(self.max_xp),
                    "level":self.level,
                    "max_hp": self.max_hp,
                    "hp":self.hp,
                    "atk":self.atk,
                    "def":self.defense,
                    "gold": int(self.gold),
                    "inventory":self.inventory
                }
                break
            x += 1
        jsonFile = open("json/profil.json","w")
        jsonData["profiles"][x] = profile
        jsonFile.seek(0)
        json.dump(jsonData, jsonFile, indent=4)
        
        return 1



    def profilToJson(self):
        jsonFile = open("json/profil.json", "r+")
        jsonData = json.load(jsonFile)

        ## Vérification si le profil est déjà créé
        for data in jsonData["profiles"]:
            if data["id"] == self.id:
                return False


        profile = {
            "id": int(self.id),
            "tuto": bool(self.tuto),
            "combat": self.combat,
            "inFight": bool(self.inFight),
            "isDead": bool(self.isDead),
            "name": str(self.name),
            "xp": int(self.xp),
            "max_xp": int(self.max_xp),
            "level":self.level,
            "max_hp": self.max_hp,
            "hp":self.hp,
            "atk":self.atk,
            "def":self.defense,
            "gold": self.gold,
            "inventory":self.inventory
        }
        jsonData["profiles"].append(profile)
        jsonFile.seek(0)
        json.dump(jsonData, jsonFile, indent=4)
        
        return True
    

    @staticmethod
    def getAllProfiles():
        jsonFile = open("json/profil.json", "r+")
        jsonData = json.load(jsonFile)

        profiles = jsonData["profiles"]

        for i in profiles:
            p = Profil.dictToProfil(i,i["id"])
            p.inFight = False

            p.modifJsonSave()

        

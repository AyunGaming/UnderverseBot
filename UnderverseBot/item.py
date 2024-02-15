import json

class Item():
    def __init__(self,name,desc,effect = None,ampleur = None) -> None:
        self.nom = name
        self.description = desc

        self.effet = effect
        
        if self.effet == None:
             self.ampleur = "Aucun"
        else:
            self.ampleur = ampleur


    def addToInventory(self,joueur,number):
        if self.nom in joueur.inventory.keys():
            joueur.inventory[self.nom] = joueur.inventory[self.nom] + number
        else:
            joueur.inventory[self.nom] = number

    
    @staticmethod
    def getItem(name = None):
        jsonFile = open("json/items.json","r")
        jsonData = json.load(jsonFile)

        items = jsonData["items"]

        if name == None:
            itemList = []


            for i in range(len(items)):
                itemList.append(items[i]["nom"])


            return itemList

        else:

            name = name.lower()
            x = 0
            for i in items:
                if(str(name) == items[x]["nom"].lower()):
                    return i
                else:
                    x += 1
            return False
        



    @staticmethod
    def dictToItem(dict):
        if dict['effet'] == None or dict['ampleur'] == None:
            return Item(dict['nom'],dict['description'],None,None)
        return Item(dict['nom'],dict['description'],dict['effet'],int(dict['ampleur']))


    @staticmethod
    def itemExists(name):
        jsonFile = open("json/items.json","r")
        jsonData = json.load(jsonFile)
        jsonFile.close()

        items = jsonData["items"]

        x = 0
        for i in items:
            if str(name) in str(items[x]["nom"]):
                return True
            else:
                x += 1
        return False


    
        

    
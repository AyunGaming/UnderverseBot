import discord
from interactions import *
from discord.ui import *
import Actors.profil as profil
import item as i
import Actors.Enemy as Enemy
from random import randint
import os
import json
from UI.HelpView import *
from UI.HelpFightView import *
from UI.FightView import *
from UI.ShopView import *
import UI.ItemView as iv
import LogsWriter as log


class Bot(discord.Client):

    def __init__(self,prefixe):
        super().__init__(intents=discord.Intents.all())

        self.prefixe = prefixe
        self.logWriter = log.LogsWriter()

        return None


    async def on_ready(self):
        try:
            print(f"Logged as {self.user.name} {self.user.id}")
	    
            self.logWriter.addLog(1,"BOT","Undertale Bot est lancé !")
            profil.Profil.getAllProfiles()
            return None
        except Exception as e:
            self.logWriter.addCriticalLog(e)
    

    async def on_message(self,message):
        try:
            if(message.author == self.user):
                return "Bot message !"

            if(message.content.startswith(self.prefixe)):
                command = message.content.split(" ")[0]

                match command:
                    case "!help":
                        await self.help(message)
                    case "!ping":
                        await message.channel.send("pong !")
                    case "!aide":
                        await self.aide(message)
                    case "!start":
                        try:
                            self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                            param = message.content.split("start ")[1]
                            await self.StartAdventure(message,param)
                        except Exception as e:
                            await message.channel.send("Il faut rentrer un pseudo !")
                    case "!tuto":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                        await self.tutorial(message)
                    case "!inv":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                        await self.inv(message)
                    case "!profil":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                        await self.profil(message)
                    case "!combat":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                        await self.combat(message)
                    case "!magasin":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command} !")
                        await self.shop(message)
                    case "!admin-fight":
                        self.logWriter.addLog(2,"COMMAND",f"{message.author} a utilisé la commande {command}")
                        await self.AdminFight(message)
                    case _:
                        self.logWriter.addLog(2,"ERROR",f"{message.author} a entré la commande {command} qui est invalide !")
                        await message.channel.send("Cette commande n'existe pas !")
            else:
                return None
        except Exception as e:
            self.logWriter.addCriticalLog(e)


    """Envoie un embed fournissant les infos nécessaires au début de l'aventure + créer les informations du joueur dans un fichier JSON"""
    async def StartAdventure(self, message: discord.Message,name = None):
        p = profil.Profil(name,message.author.id)
        res = p.profilToJson()

        if res:

            embed=discord.Embed(title="Commence ton aventure !", description="Bienvenue dans le monde d'Undertale, ici tu pourras rencontrer des tas de personnes ! Mais attention, certaines personnes ne sont pas toutes aimables envers les étrangers.", color=0x11d438)
            embed.set_author(name="Papyrus")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1048703360552947742/464de1be067986373451f6ed1767a00d.webp?size=100")
            embed.add_field(name="Quelques astuces pour avoir les bases", value="Tu peux utiliser la commande '!tuto' afin d'obtenir les informations principales concernant l'aventure !",inline=False)
            embed.add_field(name="Tu as besoin de plus d'infos ?",value="Tu peux utiliser la commande '!help' afin d'obtenir la liste de toutes les commandes disponibles ainsi que leur utilité !",inline=False)
            embed.add_field(name="Un problème pendant ton jeu ?", value="Contacte Ayun#9191 ou créer un ticket dans la section 'RPG'", inline=False)
            embed.set_footer(text="Créé par Ayun#9191")

            await message.channel.send(embed=embed)

            self.logWriter.addLog(3,"SUCCESS",f"Le profil de {message.author} a bien été créé !")
            return True
        
        await message.channel.send("Compte déjà existant !")
        self.logWriter.addLog(3,"ERROR",f"{message.author} a déjà un profil !")
        return False


    async def tutorial(self,message):
        p = profil.Profil.getProfil(message.author.id)

        if not p.tuto:

            embed=discord.Embed(title="TuToriel", description="Salut moi c'est Toriel et je suis ici pour te guider dans ton aventure ! Pour cela je vais déjà te fournir les commandes de base pour commencer ton aventure !", color=0x11d438)
            embed.set_author(name="Toriel")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/978971253933232128/1048997639238201384/latest.png")
            embed.add_field(name="Commencer son aventure", value="Si ce n'est pas déjà fait tu dois utiliser la commande '!start' afin que ton profil soit créer !", inline=False)
            embed.add_field(name="Le profil", value="Sur ton profil tu pourras visionner tout un tas d'information te concernant comme ton pseudo, ton niveau, ton argent ou encore tes statistiques ! N'hésite pas à y jeter un oeil avec la commande '!profil' !", inline=False)
            embed.add_field(name="L'inventaire", value="C'est ici que tout les objets que tu pourras récupérer seront stockés, tu peux les voir en utilisant la commande '!inv'", inline=False)
            embed.add_field(name="Les combats", value="Les combats seront le coeur de ton aventure ! Prends garde, certains adversaire sont très puissant !", inline=False)
            embed.add_field(name="Récompense",value="Pour être venue me voir je souhaite t'offrir ma tarte !",inline=False)

            embed.set_footer(text="Créé par Ayun#9191")
            await message.channel.send(embed=embed,view=HelpView(message))

            # May be complete later
            # Offer a pie for checking the tutorial
            
            pie = i.Item("Tarte de Toriel","Une delicieuse tarte confectionnee par Toriel !","HEAL",75)
        
            if isinstance(p,profil.Profil):
                pie.addToInventory(p,1)
                p.modifJsonSave()
                self.logWriter.addLog(3,"SUCCESS",f"{p.name} a obtenu 1 {pie.nom}")
            else:
                self.logWriter.addLog(3,"ERROR",f"Le profil lié à l'id {message.author.id} n'existe pas !")
            
            p.tuto = True
            p.modifJsonSave()

            return None
        

        await message.channel.send("Tuto déjà effectué !")
        self.logWriter.addLog(3,"ERROR",f"{p.name} a déjà fait le tutoriel !")
        return -1 


    async def aide(self,message):
        embed=discord.Embed(title="Aide", description="En quoi puis-je t'aider ?")
        embed.set_author(name="Underverse Bot")
        
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1048703360552947742/464de1be067986373451f6ed1767a00d.webp?size=100")
        embed.set_footer(text="By Ayun#9191")
        await message.channel.send(embed=embed,view=HelpView(message))


    async def help(self,message):
        embed=discord.Embed(title="Liste des commandes", description="Voici les commandes à ta disposition !")
        
        embed.add_field(name="!start <pseudo>", value="Permet de commencer ton aventure ! **ATTENTION: Les commandes ci-dessous seront inutilisables sinon !**", inline=False)
        embed.add_field(name="!aide", value="Donne accès à tout les tutos !", inline=False)
        embed.add_field(name="!tuto", value="Permet de lancer le premier tuto (fortement conseillé) !", inline=False)
        embed.add_field(name="!inv", value="Permet d'afficher ton inventaire !", inline=False)
        embed.add_field(name="!profil", value="Permet d'afficher ton profil' !", inline=False)
        embed.add_field(name="!combat", value="Permet de lancer un combat !", inline=False)
        embed.add_field(name="!magasin", value="Permet d'ouvrir le magasin !", inline=False)

        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1048703360552947742/464de1be067986373451f6ed1767a00d.webp?size=100")
        embed.set_footer(text="By Ayun#9191")
        await message.channel.send(embed=embed)


    async def fight(self,message,player,enemy,oneAttack):
        if oneAttack:
            damage = enemy.attack(player)
            player.hp -= damage
            self.logWriter.addLog(4,"INFO", f"{player.name} a perdu {damage} PV !")
            if(player.hp < 0):
                player.hp = 0
        else:
            x = randint(0,10)
            if x > 5:
                    damage = player.attack(enemy)

                    if damage == 0:
                        await message.channel.send(f"{player.name} a loupé son attaque")
                        self.logWriter.addLog(4,"INFO", f"{player.name} a raté son attaque !")
                    else:
                        enemy.hp -= damage
                        self.logWriter.addLog(4,"INFO", f"{enemy.name} a perdu {damage} PV !")

                    if enemy.hp < 0:
                        enemy.hp = 0

                    else:
                        damage = enemy.attack(player)

                        if damage == 0:
                            await message.channel.send(f"{enemy.name} a loupé son attaque")
                            self.logWriter.addLog(4,"INFO", f"{enemy.name} a raté son attaque !")
                        else:
                            player.hp -= damage
                            self.logWriter.addLog(4,"INFO", f"{player.name} a perdu {damage} PV !")
                            
                        if player.hp < 0:
                            player.hp = 0

            else:

                    damage = enemy.attack(player)

                    if damage == 0:
                            await message.channel.send(f"{enemy.name} a loupé son attaque")
                            self.logWriter.addLog(4,"INFO", f"{enemy.name} a raté son attaque !")
                    else:
                        player.hp -= damage
                        self.logWriter.addLog(4,"INFO", f"{player.name} a perdu {damage} PV !")

                    if(player.hp < 0):
                        player.hp = 0

                    else:

                        damage = player.attack(enemy)
                        if damage == 0:
                            await message.channel.send(f"{player.name} a loupé son attaque")
                            self.logWriter.addLog(4,"INFO", f"{player.name} a raté son attaque !")
                        else:
                            enemy.hp -= damage
                            self.logWriter.addLog(4,"INFO", f"{enemy.name} a perdu {damage} PV !")
                        if(enemy.hp < 0):
                            enemy.hp = 0

        if player.hp <= 0:
            self.logWriter.addLog(4,"INFO", f"{player.name} est mort !")
            return "PlayerDead"
        if enemy.hp <= 0:
            self.logWriter.addLog(4,"INFO", f"{enemy.name} est mort !")
            return "EnemyDead"
        return None


    async def displayFightInfoEmbed(self,message,enemy,player,bot):
        embed= discord.Embed(title="Combat", description=f"Vous avez rencontré {enemy.name}.")
        embed.set_author(name="Underverse Bot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name=f"PV: {enemy.hp}/{enemy.max_hp} 🧡", value="", inline=False)
        embed.add_field(name=f"Vos PV: {player.hp}/{player.max_hp} 🧡", value="", inline=False)
        embed.add_field(name="", value="Attaquer ⚔️", inline=False)
        embed.add_field(name="", value="Objet 📦", inline=False)
        embed.add_field(name="", value="Fuir 🦶", inline=False)
        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed,view=FightView(message,player,enemy,bot))
            

    async def combat(self,message):
        ## Récupération du joueur
        p = profil.Profil.getProfil(message.author.id)
            
        if p.combat == True:
            if not p.inFight:
                
                ## Création de l'ennemi
                e = self.chooseEnemy(p)
                #x = randint(0,10)
                #if x < 5:
                #    e = Enemy.Enemy("ennemi 1",3,150,150,15,9,40,30)
                #else:
                #    e = Enemy.Enemy("ennemi 2",1,100,100,9,6,20,10)
                #e.EnemyToJson()
                self.logWriter.addLog(3,"INFO", f"{p.name} entre en combat !")
                p.inFight = True
                await self.displayFightInfoEmbed(message,e,p,self)
                p.modifJsonSave()

            else:
                self.logWriter.addLog(3,"ERROR", f"{p.name} est déjà en combat !")
                await message.channel.send("Vous êtes déjà en combat !")

        else:
            
            ## Jamais fais de combat
            embed=discord.Embed(title="Explications sur les combats", description="Salut l'ami, il semble que tu as rencontré mon frère Papyrus et mon amie Toriel ! Je suis venu te voir pour te prévenir des dangers de ce monde. Dis moi sur quels aspects tu veux en apprendre plus.", color=0xa70be0)
            embed.set_author(name="Sans")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
            embed.add_field(name="", value="Attaquer ⚔️", inline=False)
            embed.add_field(name="", value="Objet 📦", inline=False)
            embed.add_field(name="", value="Fuir 🦶", inline=False)
            embed.add_field(name="", value="Si tu veux à nouveau des explications utilise la commande (!aide) je te réexpliquerais avec plaisir !", inline=False)
            embed.set_footer(text="Créé par Ayun#9191")
            await message.channel.send(embed=embed,view=HelpFightView(message))
            
            p.combat = True
            
            ## Créer objet potion
            potion = i.Item("Petite potion de soin","Une potion utile pour te soigner 10 HP","HEAL",10)
            potion.addToInventory(p,10)
            p.modifJsonSave()

            self.logWriter.addLog(3,"SUCCESS", f"{player.name} a reçu 10 potions !")
            return None


    async def inv(self,message):

        p = profil.Profil.getProfil(message.author.id)

        embed=discord.Embed(title=f"Inventaire de {p.name}", description="Ici tu peux retrouver tout les objets que tu as récupéré au cours de ton aventure.", color=0x7320b6)
        
        for item in p.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            embed.add_field(name=f"{itemToDisplay.nom}: {p.inventory[item]}",value=f"{itemToDisplay.description}")

        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed,view=iv.ItemView(message,p))
        self.logWriter.addLog(3,"INFO", f"{player.name} a fait afficher son inventaire !")
     

    async def profil(self,message):
        p = profil.Profil.getProfil(message.author.id)

        if type(p) == bool:
            await message.channel.send("Tu n'as pas de profil !")
            self.logWriter.addLog(3,"ERROR", f"Le profil correspondant au membre d'id {message.author.id} n'existe pas !")
        else:
            embed=discord.Embed(title=f"Profil de {p.name}", description=f"Voici toutes les informations de {p.name}", color=0xb521c0)
            embed.set_author(name="Undertale Bot")
            embed.set_thumbnail(url=message.author.avatar)
            embed.add_field(name=f"Level: {p.level}", value="", inline=False)
            embed.add_field(name=f"xp: {p.xp}/{p.max_xp}", value="", inline=False)
            embed.add_field(name=f"Prochain niveau: {p.max_xp - p.xp}", value="", inline=False)
            embed.add_field(name=f"Atk: {p.atk}", value="", inline=False)
            embed.add_field(name=f"Def: {p.defense}", value="", inline=False)
            embed.add_field(name=f"Gold: {p.gold}", value="", inline=False)
            embed.set_footer(text="Créer par Ayun#9191")
            await message.channel.send(embed=embed)

   
    async def shop(self,message):
        p = profil.Profil.getProfil(message.author.id)
        shop = Shop(p,self)

        await shop.displayShop(message)
    
    async def AdminFight(self,message):
        if message.author.id == 777242155818680330:
            ## Récupération du joueur
            p = profil.Profil.getProfil(message.author.id)
            e = Enemy.Enemy.getEnemy("Sans")

            if p.combat == True:
                if not p.inFight:
                    
                    self.logWriter.addLog(3,"INFO", f"{p.name} entre en combat !")
                    p.inFight = True
                    await self.displayFightInfoEmbed(message,e,p,self)
                    p.modifJsonSave()

                else:
                    self.logWriter.addLog(3,"ERROR", f"{p.name} est déjà en combat !")
                    await message.channel.send("Vous êtes déjà en combat !")

            else:
                
                ## Jamais fais de combat
                embed=discord.Embed(title="Explications sur les combats", description="Salut l'ami, il semble que tu as rencontré mon frère Papyrus et mon amie Toriel ! Je suis venu te voir pour te prévenir des dangers de ce monde. Dis moi sur quels aspects tu veux en apprendre plus.", color=0xa70be0)
                embed.set_author(name="Sans")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
                embed.add_field(name="", value="Attaquer ⚔️", inline=False)
                embed.add_field(name="", value="Objet 📦", inline=False)
                embed.add_field(name="", value="Fuir 🦶", inline=False)
                embed.add_field(name="", value="Si tu veux à nouveau des explications utilise la commande (!aide) je te réexpliquerais avec plaisir !", inline=False)
                embed.set_footer(text="Créé par Ayun#9191")
                await message.channel.send(embed=embed,view=HelpFightView(message))
                
                p.combat = True
                
                ## Créer objet potion
                potion = i.Item("Petite potion de soin","Une potion utile pour te soigner 10 HP","HEAL",10)
                potion.addToInventory(p,10)
                p.modifJsonSave()

                self.logWriter.addLog(3,"SUCCESS", f"{player.name} a reçu 10 potions !")
                return None
        else:
            await message.channel.send("Not allowed !")


    def chooseEnemy(self,player):
        enemies = Enemy.Enemy.getAllEnemies()
        possibles = []
        for enemy in enemies:
            if enemy.minlevel <= player.level + 1:
                possibles.append(enemy)
            elif player.level > 5:
                possibles = enemies

        print(f"Possibilitées: {len(possibles)}")
        nb = len(possibles)
        x = randint(0,nb-1)

        return possibles[x]
    
    

if __name__ == "__main__":

    
    if os.path.exists(os.getcwd() + "/json/config.json"):
            with open("./json/config.json") as f:
                configData = json.load(f)

    else:
        configTemplate = {"Token":"", "Prefix": ""}

        with open(os.getcwd() + "/json/config.json","w+") as f:
            json.dump(configTemplate,f)
    
    token = configData["Token"]
    prefixe = configData["Prefix"]

    
    bot = Bot(prefixe)

    bot.run(token)

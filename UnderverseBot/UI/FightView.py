import discord.ui as dui
from discord import *
import Actors.profil as profil
import item as i
from random import *
from LogsWriter import *

class FightView(dui.View):

    def __init__(self,m,p,e,b):
        super().__init__()
        
        self.message = m
        self.player = p
        self.enemy = e
        self.bot = b

        self.logWriter = LogsWriter()

        self.attackButton = dui.Button(label="Attaquer",style=ButtonStyle.secondary)
        self.itemButton = dui.Button(label="Objet", style=ButtonStyle.secondary)
        self.fleeButton = dui.Button(label="Fuir", style=ButtonStyle.secondary)

        self.init_Buttons()


    async def attackButton_callback(self, interaction):
        self.attackButton.disabled = True
        self.itemButton.disabled = True
        self.fleeButton.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("Vous attaquez !")

        await self.attack(self.message,self.bot,self.player,self.enemy,False)
        


    async def itemButton_callback(self,interaction):
        self.attackButton.disabled = True
        self.itemButton.disabled = True
        self.fleeButton.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message("Vous souhaitez utiliser un objet !")

        await self.inv(self.message)
        


    async def fleeButton_callback(self,interaction):
        self.attackButton.disabled = True
        self.itemButton.disabled = True
        self.fleeButton.disabled = True
        await interaction.message.edit(view=self)
        x = randint(0,10)
        if x%2:
            await interaction.response.send_message("Vous avez réussi à fuir")
            self.player.inFight = False
            
            self.logWriter.addLog(4,"INFO",f"{self.player.name} a pris la fuite !")
            self.player.hp = self.player.max_hp
            self.player.modifJsonSave()
        else:
            await interaction.response.send_message("Vous n'avez pas réussi à fuir !")
            self.logWriter.addLog(4,"INFO",f"{self.player.name} n'a pas réussi à prendre la fuite !")
            await self.attack(self.message,self.bot,self.player,self.enemy,True)        



    def init_Buttons(self):

        self.attackButton.callback = self.attackButton_callback
        self.itemButton.callback = self.itemButton_callback
        self.fleeButton.callback = self.fleeButton_callback

        self.add_item(self.attackButton)
        self.add_item(self.itemButton)
        self.add_item(self.fleeButton)



    async def attack(self,message,bot,player,enemy,oneAttack):
        res = await bot.fight(message,player,enemy,oneAttack)
        match res:
            case "PlayerDead":
                await message.channel.send("Vous êtes mort !")
                player.isDead = True
                player.inFight = False
                player.hp = player.max_hp

            case "EnemyDead":
                await message.channel.send(f"{enemy.name} est mort !")
                enemy.isDead = True
                player.xp += enemy.xp
                player.gold += enemy.gold
                player.inFight = False
                res = player.checkLVLup()

                if res:

                    embed= Embed(title="Montée de niveau", description=f"GG tu es monté niveau {player.level}")
                    embed.set_author(name="Underverse Bot")
                    embed.set_thumbnail(url=message.author.avatar)
                    embed.add_field(name=f"Atk: {player.atk}", value="", inline=True)
                    embed.add_field(name=f"Def: {player.defense}", value="", inline=False)
                    embed.set_footer(text="By Ayun#9191")
                    await message.channel.send(embed=embed)

                player.hp = player.max_hp

                self.logWriter.addLog(5,"INFO",f"{player.name} a gagné {enemy.xp} xp et {enemy.gold} gold")
                await message.channel.send(f"Vous avez gagné {enemy.xp} xp et {enemy.gold} gold !")

            case _:
                await self.displayFightInfoEmbed(self.message,self.enemy,self.player,self.bot)

        player.modifJsonSave()
        return None


    async def inv(self,message):

        p = profil.Profil.getProfil(message.author.id)
        embed= Embed(title=f"Inventaire de {p.name}", description="Choisis l'objet que tu veux utiliser", color=0x7320b6)
        
        for item in p.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            embed.add_field(name=f"{itemToDisplay.nom}: {p.inventory[item]}",value=f"{itemToDisplay.description}")

        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed,view=ItemView(self.player,self.message,self.enemy,self.bot))



    async def displayFightInfoEmbed(self,message,enemy,player,bot):
        embed= Embed(title="Combat", description=f"Vous avez rencontré un {enemy.name}.")
        embed.set_author(name="Underverse Bot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name=f"PV: {enemy.hp}/{enemy.max_hp} 🧡", value="", inline=False)
        embed.add_field(name=f"Vos PV: {player.hp}/{player.max_hp} 🧡", value="", inline=False)
        embed.add_field(name="", value="Attaquer ⚔️", inline=False)
        embed.add_field(name="", value="Objet 📦", inline=False)
        embed.add_field(name="", value="Fuir 🦶", inline=False)
        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed,view=FightView(self.message,self.player,self.enemy,self.bot))










class ItemView(dui.View):
    
    def __init__(self,p,m,e,b):
        super().__init__()

        self.player = p
        self.message = m
        self.enemy = e
        self.bot = b

        self.getPlayerInventory()
        self.createInventoryButtons()
        self.initButtons()

    def getPlayerInventory(self):
        self.items = []
        for item in self.player.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)


    def createInventoryButtons(self):
        self.buttons = []
        index = 0
        for i in self.items:

            self.buttons.append(ItemButton(self.player,self.message, self.enemy, self.bot ,label=f"{i.nom}", style=ButtonStyle.primary, custom_id=str(index)))
            index += 1


    def initButtons(self):
        for button in self.buttons:
            self.add_item(button)












class ItemButton(dui.Button):
    def __init__(self, p, m, e, b, label: str, style: ButtonStyle, custom_id: str):
        super().__init__()

        self.player = p
        self.message = m
        self.enemy = e
        self.bot = b
        self.items = []
        self.log = LogsWriter()

        self.label = label
        self.style = style
        self.custom_id = custom_id

        self.getPlayerInventory()

    def getPlayerInventory(self):
        for item in self.player.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)


    async def useItem(self,id):
        if self.player.hp == self.player.max_hp:
            await self.message.channel.send("Vos PV sont déjà au maximum !")
        else:
            item = self.items[int(id)]

            match item.effet:
                case "HEAL":
                    if self.player.hp + item.ampleur > self.player.max_hp:
                        self.player.hp = self.player.max_hp
                    else:
                        self.player.hp += item.ampleur
                    await self.message.channel.send(f"{item.nom} a été utilisé !, {self.player.name} est maintenant a {self.player.hp}")
                    self.log.addLog(4,"INFO",f"{item.nom} a été utilisé par {self.player.name} il a gagné {item.ampleur} HP et a maintenant {self.player.hp} HP")
                case _:
                    await self.message.channel.send("Objet non utilisable")
                    await self.log.addLog(4,"INFO",f"{self.player.name} a tenté d'utiliser l'objet {item.nom} !")
            return item



    async def removeItemFromInventory(self,item):
        if self.player.inventory[item.nom] == 1:
            self.player.inventory.pop(item.nom)
        else:
            self.player.inventory[item.nom] -= 1



    async def callback(self,interaction: Interaction):
        
        await interaction.response.send_message("Vous utilisez l'item !")

        item = await self.useItem(self.custom_id)
        await self.removeItemFromInventory(item)

        self.player.modifJsonSave()

        self.disabled = True

        await self.displayFightInfoEmbed(self.message,self.enemy,self.player,self.bot)

    
    async def displayFightInfoEmbed(self,message,enemy,player,bot):
        embed= Embed(title="Combat", description=f"Vous avez rencontré un {enemy.name}.")
        embed.set_author(name="Underverse Bot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name=f"PV: {enemy.hp}/{enemy.max_hp} 🧡", value="", inline=False)
        embed.add_field(name=f"Vos PV: {player.hp}/{player.max_hp} 🧡", value="", inline=False)
        embed.add_field(name="", value="Attaquer ⚔️", inline=False)
        embed.add_field(name="", value="Objet 📦", inline=False)
        embed.add_field(name="", value="Fuir 🦶", inline=False)
        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed,view=FightView(self.message,self.player,self.enemy,self.bot))
    
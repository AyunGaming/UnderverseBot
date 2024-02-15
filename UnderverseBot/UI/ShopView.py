import discord.ui as dui
from discord import *
import Actors.profil as profil
import item as i
from random import *
from UI.FightView import *
from LogsWriter import *


class Shop():

    def __init__(self,p,b):

        self.player = p
        self.bot = b
        self.content = {

        }
        self.items = i.Item.getItem()
        self.addItemToShop(25,"petite potion de soin")
        self.addItemToShop(75,"potion de soin moyenne")

        self.logWriter = LogsWriter()


    def addItemToShop(self,price,item):
        itemName = item
        itemDict = i.Item.getItem(itemName)
        
        if type(itemDict) != bool: 

            item = i.Item.dictToItem(itemDict)

            if i.Item.itemExists(item.nom):
                self.content[item.nom] = price
            else:
                return False


    async def displayItems(self,message):
        await message.channel.send(f"Voici la liste des items disponibles dans le jeu: ")
        for i in self.items:
            await message.channel.send(i)


    async def displayShop(self,message):
        embed=Embed(title="Magasin", description="Veuillez choisir l'objet que vous souhaitez acheter", color=0x84ca1c)
        embed.set_author(name="Underverse Bot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1048703360552947742/464de1be067986373451f6ed1767a00d.png?size=512")
        for i in self.content.keys():
            embed.add_field(name=f"{i}: {self.content[i]} gold", value="", inline=False)
        embed.add_field(name="", value=f"Votre gold: {self.player.gold}", inline=True)
        embed.set_footer(text="Créé par Ayun#9191")
        await message.channel.send(embed=embed, view=ShopView(message,self.player,self.bot,self))


class ShopView(dui.View):

    def __init__(self,m,p,b,s):
        super().__init__()

        self.message = m
        self.player = p
        self.bot = b   
        self.shop = s                  

        self.getShopContent()
        self.createShopButtons()
        self.initButtons()

    def getShopContent(self):
        self.items = []
        for item in self.shop.content.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)


    def createShopButtons(self):
        self.buttons = []
        index = 0
        for i in self.items:

            self.buttons.append(ShopButton(self.player,self.message,self.bot,self.shop,label=f"{i.nom}",style=ButtonStyle.primary,custom_id=str(i.nom)))
            index += 1

    def initButtons(self):
        for button in self.buttons:
            self.add_item(button)



class ShopButton(dui.Button):

    def __init__(self,p,m,b,s, label: str, style: ButtonStyle, custom_id: str):
        super().__init__()

        self.message = m
        self.player = p
        self.bot = b
        self.shop = s

        self.label = label
        self.style = style
        self.custom_id = custom_id

        self.logWriter = LogsWriter()

        self.getShopContent()



    async def callback(self, interaction: Interaction):
        
        itemDict = i.Item.getItem(self.custom_id)
        item = i.Item.dictToItem(itemDict)
        if self.shop.content[self.custom_id] < self.player.gold:

            item.addToInventory(self.player,1)
            self.player.gold -= self.shop.content[self.custom_id]
            
            self.logWriter.addLog(3,"INFO",f"{self.player.name} a acheté {item.nom} au prix de {self.shop.content[self.custom_id]}")

            self.player.modifJsonSave()

            await interaction.response.send_message(f"Vous avez acheter l'item {item.nom}.\nIl vous reste {self.player.gold} gold") 
        else:
            self.logWriter.addLog(3,"ERROR",f"{self.player.name} a tenté d'acheté {item.nom} au prix de {self.shop.content[self.custom_id]} alors qu'il n'avait que {self.player.gold}")
            await interaction.response.send_message(f"Vous n'avez pas assez de gold pour acheter {item.nom}, il vous en manque {self.shop.content[self.custom_id] - self.player.gold}")


    def getShopContent(self):
        self.items = []
        for item in self.shop.content.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)

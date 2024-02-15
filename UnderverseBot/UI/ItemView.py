import discord.ui as dui
from discord import *
import Actors.profil as profil
import item as i
from random import *
from LogsWriter import *


class ItemView(dui.View):

    def __init__(self,m,p):
        super().__init__()

        self.message = m
        self.player = p              

        self.getInvContent()
        self.createItemButtons()
        self.initButtons()

    def getInvContent(self):
        self.items = []
        for item in self.player.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)


    def createItemButtons(self):
        self.buttons = []
        index = 0
        for i in self.items:

            self.buttons.append(ItemButton(self.player,self.message,label=f"{i.nom}",style=ButtonStyle.primary,custom_id=str(i.nom)))
            index += 1

    def initButtons(self):
        for button in self.buttons:
            self.add_item(button)



class ItemButton(dui.Button):

    def __init__(self,p,m, label: str, style: ButtonStyle, custom_id: str):
        super().__init__()

        self.message = m
        self.player = p

        self.label = label
        self.style = style
        self.custom_id = custom_id

        self.logWriter = LogsWriter()

        self.getInvContent()



    async def callback(self, interaction: Interaction):
        self.disabled = True
        await interaction.message.edit(view=self)
        itemDict = i.Item.getItem(self.custom_id)
        item = i.Item.dictToItem(itemDict)
        
        embed=Embed(title=f"{item.nom}", description=f"{item.description}")
        embed.set_author(name="Underverse Bot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1048703360552947742/464de1be067986373451f6ed1767a00d.png?size=512")
        embed.add_field(name=f"{item.effet}: {item.ampleur}", value="", inline=True)
        embed.set_footer(text="By Ayun#9191")
        await interaction.response.send_message(embed=embed)

    def getInvContent(self):
        self.items = []
        for item in self.player.inventory.keys():
            itemDict = i.Item.getItem(item)
            itemToDisplay = i.Item.dictToItem(itemDict)
            self.items.append(itemToDisplay)
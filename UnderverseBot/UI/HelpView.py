import discord.ui as dui
from discord import *
import Actors.profil as profil
import item as i
from random import *
from LogsWriter import *
from UI.HelpFightView import *


class HelpView(dui.View):

    def __init__(self,m):
        super().__init__()

        self.message = m

        self.profilButton = dui.Button(label="Le profil",style=ButtonStyle.secondary)
        self.inventoryButton = dui.Button(label="L'inventaire",style=ButtonStyle.secondary)
        self.combatButton = dui.Button(label="Les combats",style=ButtonStyle.secondary)

        self.init_Buttons()



    async def profilButton_callback(self,interaction: Interaction):
        embed = Embed(title="Le profil", description="Le profil est l'endroit où tu pourras retrouver les principales informations sur ton compte !")
        embed.set_author(name="Toriel")
        embed.add_field(name="Le niveau", value="Tu pourras voir ton niveau ainsi que ton exp en cours et l'exp nécessaire pour que tu passes au niveau suivant.")
        embed.add_field(name="Les statistiques", value="Tu pourras également voir tes statistiques d'attaque et de défense, qui augmente à chaque montée de niveau.")
        embed.add_field(name="L'or",value="Tu peux également voir ton montant d'or qui te permettra de t'acheter différents objets.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/978971253933232128/1048997639238201384/latest.png")
        embed.set_footer(text="By Ayun#9191")
        await interaction.response.send_message(embed=embed)

    
    async def inventoryButton_callback(self,interaction: Interaction):
        embed = Embed(title="L'inventaire", description="L'inventaire est l'endroit où tu pourras retrouver tout tes objets !")
        embed.set_author(name="Toriel")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/978971253933232128/1048997639238201384/latest.png")
        embed.set_footer(text="By Ayun#9191")
        await interaction.response.send_message(embed=embed)


    async def combatButton_callback(self,interaction: Interaction):
        embed = Embed(title="Le combat",description="Les combats sont le coeur de ton aventure, dis moi quels points t'intéresse.")
        embed.set_author(name="Toriel")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/978971253933232128/1048997639238201384/latest.png")
        embed.set_footer(text="By Ayun#9191")
        await interaction.response.send_message(embed=embed,view=HelpFightView(self.message))


    def init_Buttons(self):

        self.profilButton.callback = self.profilButton_callback
        self.inventoryButton.callback = self.inventoryButton_callback
        self.combatButton.callback = self.combatButton_callback

        self.add_item(self.profilButton)
        self.add_item(self.inventoryButton)
        self.add_item(self.combatButton)
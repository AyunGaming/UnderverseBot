import discord.ui as dui
from discord import *
import Actors.profil as profil
import item as i
from random import *
from LogsWriter import *


class HelpFightView(dui.View):
    
    def __init__(self,m):
        super().__init__()

        self.message = m

        self.attackButton = dui.Button(label="L'attaque",style=ButtonStyle.secondary)
        self.itemButton = dui.Button(label="Les objets", style=ButtonStyle.secondary)
        self.fleeButton = dui.Button(label="La fuite", style=ButtonStyle.secondary)

        self.init_Buttons()


    async def attackButton_callback(self, interaction: Interaction):
        embed=Embed(title="L'attaque", description="Voici quelques informations sur les attaques")
        embed.set_author(name="Sans")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name="Les attaques classiques", value="Ton attaque touche l'adversaire et lui inflige des dégâts !", inline=False)
        embed.add_field(name="Les coups critiques", value="Les coups critique ont une chance d'apparaître lorsque tu attaques ton adversaire, lui infligeant plus de dégats.", inline=False)
        embed.add_field(name="L'attaque ratée", value="Ton attaque a une faible chance de rater ton adversaire et lui infliger aucun dégât.", inline=True)
        embed.add_field(name="", value="J'espère que tu as compris comment fonctionnait l'attaque.", inline=False)
        embed.set_footer(text="Créé par Ayun#9191")
        await interaction.response.send_message(embed=embed)
        
    async def itemButton_callback(self, interaction: Interaction):
        embed=Embed(title="Les objets", description="Les objets te seront utiles si tu souhaites te soigner. Attention à ne pas trop en utiliser tu pourrais en avoir besoin contre de puissants ennemis.")
        embed.set_author(name="Sans")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name="", value="Les objets que tu peux acheter dans le magasin te permet d'être utilisé durant tes combats", inline=True)
        embed.set_footer(text="Créé par Ayun#9191")
        await interaction.response.send_message(embed=embed)
    
    async def fleeButton_callback(self, interaction: Interaction):
        embed=Embed(title="La fuite", description="Si par malheur tu venais à rencontrer un ennemi trop puissant pour toi, tu peux toujours tenté la fuite mais attention ça marche pas à tout les coups.")
        embed.set_author(name="Sans")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1049004116464107591/1065982515476713543/favpng_undertale-sprite-sans-comic-sans-pixel-art.png")
        embed.add_field(name="", value="Voilà pour la fuite, si tu as besoin d'autre chose n'hésite pas !", inline=True)
        embed.set_footer(text="Créé par Ayun#9191")
        await interaction.response.send_message(embed=embed)


    def init_Buttons(self):

        self.attackButton.callback = self.attackButton_callback
        self.itemButton.callback = self.itemButton_callback
        self.fleeButton.callback = self.fleeButton_callback

        self.add_item(self.attackButton)
        self.add_item(self.itemButton)
        self.add_item(self.fleeButton)

import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from main import embed_color
import aiosqlite

class Confirm(nextcord.ui.View):
    def __init__(self, guild_id):
        super().__init__()
        self.value = None
        self.guild_id = guild_id

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        async with aiosqlite.connect("server_security.db") as db:
            await db.execute("INSERT OR IGNORE INTO anti_raid (server_id) VALUES (?)", (self.guild_id,))
            await db.commit()

        await interaction.response.send_message("Anti-raid has been enabled for this server.", ephemeral=True)
    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Cancelled", ephemeral=True)

class Anti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="anti", description="Anti Commands")
    async def anti(self, interaction: nextcord.Interaction):
        pass

    @anti.subcommand(name="link", description="Enable anti-link")
    async def link(self, interaction: nextcord.Interaction):
        guild_id = interaction.guild.id

        async with aiosqlite.connect("server_security.db") as db:
            await db.execute("INSERT OR IGNORE INTO anti_link (server_id) VALUES (?)", (guild_id,))
            await db.commit()

        await interaction.response.send_message("Anti-link has been enabled for this server.", ephemeral=True)

    @anti.subcommand(name="raid", description="Enable anti-raid")
    async def raid(self, interaction: nextcord.Interaction):
        guild_id = interaction.guild.id
        view = Confirm(guild_id)
        embed = nextcord.Embed(
            title="Wait!",
            description="Activating the anti-raid feature would do the following:\n• Accounts younger than a week are kicked\nAre you sure?",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(Anti(bot))
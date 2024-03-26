import nextcord
import random
import sqlite3
import aiosqlite
from nextcord.ext import commands
from main import embed_color

class Beg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_balance(self, user_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?",
                (user_id, amount, amount)
            )
            await db.commit()

    @nextcord.slash_command(name="beg", description="Earn a couple dollars by begging!")
    async def beg(self, interaction: nextcord.Interaction):
        earnings = random.randint(20, 250)
        await self.update_balance(interaction.user.id, earnings)
        embed = nextcord.Embed(
            description=f"A generous person gave you {earnings}$",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Beg(bot))
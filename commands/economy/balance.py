import nextcord

import sqlite3
import aiosqlite
from nextcord.ext import commands, application_checks
from main import embed_color

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_balance(self, user_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    @nextcord.slash_command(name="balance", description="View your balance")
    async def balance(self, interaction: nextcord.Interaction, user: nextcord.Member):
        if user == None:
            user = interaction.user
        user_balance = await self.get_balance(user.id)

        embed = nextcord.Embed(
            title=f"{user.display_name}'s Balance",
            description=f"Coins : {user_balance}$",
            color=embed_color
        )

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Balance(bot))
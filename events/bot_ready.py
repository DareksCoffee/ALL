import nextcord
from nextcord.ext import commands
import sqlite3
import aiosqlite
from main import embed_color, RESET, GREEN

class BotReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is ready")
        await self.bot.change_presence(activity=nextcord.Game(name="/help | command list"))

        async with aiosqlite.connect("warnings.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS warnings (
                    warning_id TEXT PRIMARY KEY,
                    guild_id INTEGER,
                    user_id INTEGER,
                    moderator_id INTEGER,
                    reason TEXT
                )
                """
            )
            await db.commit()
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0
                )
                """
            )
            await db.commit()

        async with aiosqlite.connect("server_security.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS anti_link (
                    server_id INTEGER PRIMARY KEY
                )
                """
            )
            await db.commit()
            
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS anti_raid (
                    server_id INTEGER PRIMARY KEY
                )
                """
            )
            await db.commit()
def setup(bot):
    bot.add_cog(BotReady(bot))
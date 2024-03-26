import nextcord
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
import asyncio

load_dotenv() ## Loading dotenv ##

## GLOBAL VARIABLES ##
TOKEN = os.getenv("BOT_TOKEN")
intents = nextcord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='a!', intents=intents)

## EMBED VARIABLES ##
embed_color = 0x5865f2
default_footer = "ALL Bot"

## ANSI COLORS ##
RESET = "\033[0m" ## Reset the ANSI color ##
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"


async def ThrowError(interaction: nextcord.Interaction, *, error, error_type=None):
    title = f"Error: {error_type}" if error_type else "Error"
    embed = nextcord.Embed(
        title=title,
        description=f"{error}",
        color=embed_color
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

def load_cogs():
    print("Loading cogs...")
    loaded_cogs = set()
    for root, dirs, files in os.walk('commands'):
        for file in files:
            if file.endswith('.py'):
                cog_path = os.path.join(root, file)
                cog_module = cog_path.replace(os.sep, '.')[:-3]
                if cog_module not in loaded_cogs:
                    try:
                        bot.load_extension(cog_module)
                        loaded_cogs.add(cog_module)
                        print(f'{GREEN}[+] Loaded cog: {cog_module}{RESET}')
                    except Exception as e:
                        print(f'{RED}[-] Failed to load cog {cog_module}: {e}{RESET}')
    print("Loading event cogs...")
    for root, dirs, files in os.walk('events'):
        for file in files:
            if file.endswith('.py'):
                cog_path = os.path.join(root, file)
                cog_module = cog_path.replace(os.sep, '.')[:-3]
                if cog_module not in loaded_cogs:
                    try:
                        bot.load_extension(cog_module)
                        loaded_cogs.add(cog_module)
                        print(f'{GREEN}[+] Loaded event cog: {cog_module}{RESET}')
                    except Exception as e:
                        print(f'{RED}[-] Failed to load event cog {cog_module}: {e}{RESET}')
if __name__ == "__main__":
    load_cogs()
    bot.run(TOKEN)
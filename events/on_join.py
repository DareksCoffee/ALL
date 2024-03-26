import nextcord
from nextcord.ext import commands
from main import embed_color

class OnJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        last_server = len(self.bot.guilds)
        channel = None
        for text_channel in guild.text_channels:
            if not text_channel.permissions_for(guild.me).send_messages:
                continue
            if text_channel.type == nextcord.ChannelType.text:
                channel = text_channel
                break

        if channel:
            embed = nextcord.Embed(
                title="",
                description=f"Hi!\nI am ALL, a security/moderation bot who aims to make your server more secure and active!\nYou are the {last_server}th server that invited me!"
                            "\nUse `/help` to get a list of all the commands available in ALL!\n",
                color=embed_color
            )
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(OnJoin(bot))
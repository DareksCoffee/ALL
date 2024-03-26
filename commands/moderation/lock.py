import nextcord
from nextcord.ext import commands

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="lock", description="Lock a channel.")
    async def lock(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):

        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully locked.")

def setup(bot):
    bot.add_cog(Lock(bot))
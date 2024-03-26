import nextcord
from nextcord.ext import commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unlock", description="Unlock a channel.")
    async def unlock(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):

        channel = channel or interaction.channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message(f"<#{channel.id}> has been successfully unlocked.")

def setup(bot):
    bot.add_cog(Unlock(bot))
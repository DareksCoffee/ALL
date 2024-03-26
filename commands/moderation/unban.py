import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="unban", description="unban a user")
    @application_checks.has_permissions(ban_members=True)
    async def unban(self, interaction: nextcord.Interaction, user: nextcord.Member):
        embed = nextcord.Embed(
            title=f"Success",
            description=f"{user.name} has been successfully unbanned",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)
        await interaction.guild.unban(user)

def setup(bot):
    bot.add_cog(Unban(bot))
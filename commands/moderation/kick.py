import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="kick", description="Kick a user.")
    @application_checks.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member, reason= "No reason provided."):
        if user == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot kick yourself!")
        elif user == self.bot.user:
            await ThrowError(interaction=interaction, error="You cannot kick me!")
        elif not interaction.guild.me.top_role > user.top_role:
            await ThrowError(interaction=interaction, error="I cannot kick this user due to role hierarchy.")
        else:
            kicked = "The user " if not user.bot else "The bot "
            embed = nextcord.Embed(
                title=f"Success!",
                description=f"{kicked}{user.name} has been successfully kicked.\n**Username**: {user.name}\n**User ID**: {user.id}\n**Reason**: {reason}",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed)
            await user.kick(reason=reason)

def setup(bot):
    bot.add_cog(Kick(bot))
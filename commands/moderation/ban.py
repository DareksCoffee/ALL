import nextcord
from nextcord.ext import commands, application_checks
from main import embed_color, default_footer, ThrowError

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ban", description="ban a user.")
    @application_checks.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member, reason= "No reason provided."):
        if user == interaction.user:
            await ThrowError(interaction=interaction, error="You cannot ban yourself!")
        elif user == self.bot.user:
            await ThrowError(interaction=interaction, error="You cannot ban me!")
        elif not interaction.guild.me.top_role > user.top_role:
            await ThrowError(interaction=interaction, error="I cannot ban this user due to role hierarchy.")
        
        banned = "The user " if not user.bot else "The bot "
        embed = nextcord.Embed(
            title="Succes!",
            description=f"{banned}{user.name} has been successfully banned\n**Username**: {user.name}\n**User ID**: {user.id}\n**Reason**: {reason}",
            color=embed_color
        )
        await user.ban(reason=reason)
        await interaction.response.send_message(embed=embed)

    #@ban.subcommand(name="list", description="List all banned users")
    #async def list_bans(self, interaction: nextcord.Interaction):
    #    banned_users = interaction.guild.bans()
    #    users = ""
    #    async for ban_entry in banned_users:
    #        user = ban_entry.user
    #        users += f"{user.name} | {user.id}\n"
    #    
    #    embed = nextcord.Embed(
    #        title="Ban List",
    #        description=f"There are {len(ban_entry) - 1} banned users\n{users}",
    #        color=embed_color
    #    )
    #    await interaction.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(Ban(bot))
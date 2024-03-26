import nextcord
from nextcord.ext import commands
from main import embed_color
import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_thumbnail = "https://i.imgur.com/hdtXYbj.png"

    @nextcord.slash_command(name="server", description="server commands")
    async def server(self, interaction: nextcord.Interaction):
        pass

    @server.subcommand(name="info", description="Display information about the server")
    async def info(self, interaction: nextcord.Interaction):
        guild = interaction.guild

        server_name = guild.name
        server_id = guild.id
        server_owner = guild.owner
        server_region = guild.region
        member_count = guild.member_count
        creation_date = guild.created_at.strftime("%B %d, %Y")

        embed = nextcord.Embed(
            title="Server Information",
            color=embed_color
        )
        embed.add_field(name="Server Name", value=server_name, inline=True)
        embed.add_field(name="Server ID", value=server_id, inline=True)
        embed.add_field(name="Server Owner", value=server_owner.mention, inline=True)
        embed.add_field(name="Server Region", value=server_region, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)
        embed.add_field(name="Creation Date", value=creation_date, inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not guild.icon else guild.icon.url)

        await interaction.response.send_message(embed=embed)

    @server.subcommand(name="count", description="User/Bot count for the server")
    async def count(self, interaction: nextcord.Interaction):
        guild = interaction.guild

        bot_count = sum(1 for member in guild.members if member.bot)
        user_count = guild.member_count - bot_count

        embed = nextcord.Embed(
            title="Member count",
            description=f"Server count for {guild.name}\n**Members**: {user_count}\n**Bots**: {bot_count}\n**Total** : {guild.member_count}",
            color=embed_color
        )
        embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not guild.icon else guild.icon.url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))
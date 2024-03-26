import nextcord
from nextcord.ext import commands
from main import embed_color

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_results_requested = set()

    async def calculate_poll_result(self, message):
        one_count = 0
        two_count = 0
        for reaction in message.reactions:
            if reaction.emoji == "1️⃣":
                one_count = reaction.count - 1
            elif reaction.emoji == "2️⃣":
                two_count = reaction.count - 1

        total_votes = one_count + two_count
        if total_votes > 0:
            one_percentage = (one_count / total_votes) * 100
            two_percentage = (two_count / total_votes) * 100
            result_embed = nextcord.Embed(
                title="Poll Result",
                description=f"Option 1: {one_percentage:.2f}%\nOption 2: {two_percentage:.2f}%",
                color=embed_color
            )
            await message.channel.send(embed=result_embed)
        else:
            await message.channel.send("No votes recorded for this poll.")

    @nextcord.slash_command(name="poll", description="Create a poll!")
    async def poll(self, interaction: nextcord.Interaction):
        pass

    @poll.subcommand(name="create", description="Create a poll")
    async def create(self, interaction: nextcord.Interaction, message: str, choice1: str, choice2: str):
        poll = nextcord.Embed(
            title=f"Poll: {message}",
            description=f":one: {choice1}\n\n:two: {choice2}",
            color=embed_color
        )
        poll.set_footer(text=f"Poll by {interaction.user}")
        embed = nextcord.Embed(
            description="Successfully created poll.",
            color=embed_color
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        poll_message = await interaction.send(embed=poll)

        await poll_message.add_reaction("1️⃣")
        await poll_message.add_reaction("2️⃣")

    @poll.subcommand(name="result", description="Get the result of a poll")
    async def poll_result(self, interaction: nextcord.Interaction, message_id: str):
        channel = interaction.channel
        message = await channel.fetch_message(message_id)

        if message.author == self.bot.user and len(message.embeds) > 0 and message.embeds[0].title.startswith("Poll:"):
            self.poll_results_requested.add(message.id)
            await self.calculate_poll_result(message)
            embed = nextcord.Embed(
                title="Success",
                description="Here are the poll results",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Invalid poll message ID or no poll found.", ephemeral=True)

def setup(bot):
    bot.add_cog(Poll(bot))
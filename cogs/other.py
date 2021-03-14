import discord
from discord.ext import commands, tasks

class other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def partners(self, ctx):
            embed = discord.Embed(
                author="Cube Club",
                title="Cube Club",
                description="cube club is our partner becaause coobs are pog"
            )
            await ctx.message.reply(embed=embed)


def setup(client):
    client.add_cog(other(client))
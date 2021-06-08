import discord
from discord.ext import commands, tasks

class other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dev(self, ctx):
            embed = discord.Embed(
                author="Developer",
                title="Developers",
                description="Connor!#0800 made me ~~with a lot of fun because he totally isn't a JS fanboy~~"
            )
            await ctx.message.reply(embed=embed)


def setup(client):
    client.add_cog(other(client))
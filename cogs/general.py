import discord
from discord.ext import commands, tasks

class general(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Invite me!", aliases=["inv", "i"])
    async def invite(self, ctx):
            embed = discord.Embed(
                author="ZeroTwo.py",
                title="Invite me!",
                description="Invite me by pressing [here](https://discord.com/api/oauth2/authorize?client_id=817837195578048522&permissions=0&scope=bot)",
                footer="I love you"
            )
            await ctx.message.reply(embed=embed)

def setup(client):
    client.add_cog(general(client))
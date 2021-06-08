import discord
from discord.ext import commands, tasks
import aiohttp
hug = ["https://media1.tenor.com/images/faf29ddc23059c5740751a3fecc2f303/tenor.gif?itemid=13533690",
       "https://media1.tenor.com/images/f20151a1f7e003426ca7f406b6f76c82/tenor.gif?itemid=13985247",
       "https://media1.tenor.com/images/8ac5ada8524d767b77d3d54239773e48/tenor.gif?itemid=16334628",
       "https://media1.tenor.com/images/68f16d787c2dfbf23a4783d4d048c78f/tenor.gif?itemid=9512793",
       "https://media1.tenor.com/images/3fee00811a33590e4ee490942f233c78/tenor.gif?itemid=14712845",
       "https://media1.tenor.com/images/2d13ede25b31d946284eaa3b8a4e6b31/tenor.gif?itemid=11990658",
       "https://media1.tenor.com/images/37df0fae36f9cce061c3cec84fc97a08/tenor.gif?itemid=17781844",
       "https://media1.tenor.com/images/ece75ca15b715aacd86724ee23604569/tenor.gif?itemid=16796068",
       "https://media2.giphy.com/media/gl8ymnpv4Sqha/giphy.gif"]
import random

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

    @commands.command(help="get a link to the support server", aliases=["helpmeplease", "ineedsupportplox"])
    async def support(self, ctx):
        embed = discord.Embed(
            author="ZeroTwo.py",
            title="Support server",
            description="You may join our [support server](https://dsc.gg/connor) :D"
        )
        await ctx.message.reply(embed=embed)

    @commands.command(help="hug someone!", aliases=["hog"])
    async def hug(self, ctx, members: commands.Greedy[discord.Member]):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/animu/hug") as r:
                js = await r.json()
                
                if not members:
                    return await ctx.send("Please specify someone to hug.")
                e = discord.Embed(color=0xff0000, description=f"**{ctx.message.author.display_name}** hugs " + "**" + '**, **'.join(x.display_name for x in members) + "**")
                
                manual = hug
                manual.append(js['link'])
                image = random.choice(manual)
                
                e.set_image(url=image)
                await ctx.send(embed=e)

def setup(client):
    client.add_cog(general(client))
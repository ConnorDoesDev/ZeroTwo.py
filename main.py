import discord
from discord.ext import commands, tasks
from config import *
import os

client = commands.Bot(
    command_prefix = ["py ", "bruh ", "hi "], 
        case_insensitive = True, 
        intents = discord.Intents.all(),
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False),
        owner_ids = DEVELOPER
)

client.remove_command('help')

client.cmd_edits = {}

class EditingContext(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=discord.AllowedMentions.none()):
        if file or files:
            return await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)
        reply = None
        try:
            reply = client.cmd_edits[self.message.id]
        except KeyError:
            pass
        if reply:
            try:
                reply.edit(content=content, embed=embed, delete_after=delete_after, allowed_mentions=allowed_mentions)
            except:
                return
        msg = await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)
        self.bot.cmd_edits[self.message.id] = msg
        return msg

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')

@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    client.load_extension('jishaku')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        ie = discord.Embed()
        ie.add_field(name='error while processing', value='Please fill in all the required arguments.\nUse `exo info <command`> for usage.')
        await ctx.send(embed=ie)
        e = discord.Embed()
        e.description = f"{ctx.message.author} had an error while using a command:\n`Required arguments were not specified.`"
        channel = client.get_channel(820659051007967232)
        await channel.send(embed=e)

    if isinstance(error, commands.MissingPermissions):
        ie = discord.Embed()
        ie.add_field(name='error while processing', value='You do not have the sufficient permissions.')
        await ctx.send(embed=ie)
        e = discord.Embed()
        e.description = f"{ctx.message.author} had an error while using a command:\n`User permissions are too low.`"
        channel = client.get_channel(820659051007967232)
        await channel.send(embed=e)

    if isinstance(error, commands.NotOwner):
        ie = discord.Embed()
        ie.add_field(name='error while processing', value='Only bot owners can use this command.')
        await ctx.send(embed=ie)
        e = discord.Embed()
        e.description = f"{ctx.message.author} had an error while using a command:\n`Command can only be used by bot owners.`"
        channel = client.get_channel(820659051007967232)
        await channel.send(embed=e)
    
    if isinstance(error, commands.CommandOnCooldown):
        cdamount = '{:.2f}'.format(error.retry_after)
        ie = discord.Embed()
        ie.description=f"This command is on cooldown for **{cdamount}** more seconds, please wait."
        await ctx.send(embed=ie, delete_after=5)
        e = discord.Embed()
        e.description=f"Cooldown (`{cdamount}s`) occured for {ctx.message.author} in {ctx.guild.name} (`{ctx.guild.id}`)."
        channel = client.get_channel(820659051007967232)
        await channel.send(embed=e)
        
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        ie = discord.Embed(title="⚠️ An error occured")
        ie.description="```{}```".format(error)
        await ctx.send(embed=ie)
        channel = client.get_channel(820659051007967232)
        e = discord.Embed(title="⚠️ An error occured")
        e.description="```{}```".format(error)

@client.command()
@commands.is_owner()
async def load(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to load next time you idiot")
        return
    client.load_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Loaded {extension}")

@client.command()
@commands.is_owner()
async def unload(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to unload next time you idiot")
        return
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Unloaded {extension}")

@client.command()
@commands.is_owner()
async def reload(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to reload next time you idiot")
        return
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Reloaded {extension}")


client.run(TOKEN)

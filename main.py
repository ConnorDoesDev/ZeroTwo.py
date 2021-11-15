import discord
from discord.ext import commands, tasks
from config import *
import os

client = commands.Bot(
    command_prefix = ["ztpy-", "<@817837195578048522> ", "<@!817837195578048522> "], 
        case_insensitive = True, 
        intents = discord.Intents.all(),
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False),
        owner_ids = DEVELOPER
)

client.remove_command('help')

class EditingContext(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=discord.AllowedMentions(users=False, roles=False, everyone=False, replied_user=True)):
        if file or files:
            return await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)
        reply = None
        try:
            reply = self.bot.cmd_edits[self.message.id]
        except KeyError:
            pass
        if reply:
            return await reply.edit(content=content, embed=embed, delete_after=delete_after, allowed_mentions=allowed_mentions)
        reference = self.message.reference
        if reference and isinstance(reference.resolved, discord.Message):
            msg = await reference.resolved.reply(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)
        else:
            msg = await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions)
        self.bot.cmd_edits[self.message.id] = msg
        return msg

async def on_message(self, message):
        if message.author.bot:
            return
        try:
            ctx = await self.get_context(message, cls=EditingContext)
            if message.guild:
                if ctx.valid:
                    await self.invoke(ctx)
        except Exception as e:
            print(e)
            return

async def on_message_edit(self, before, after):

        if before.author.bot:
            return

        if after.content != before.content:
            try:
                ctx = await self.get_context(after, cls=EditingContext)
                if after.guild:
                    if ctx.valid:
                        await self.invoke(ctx)
            except discord.NotFound:
                return


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
        ie.add_field(name='error while processing', value='fill in all the required arguments.\nUse `ztpy-info <command`> for usage.')
        await ctx.send(embed=ie)
        e = discord.Embed()
        e.description = f"{ctx.message.author} had an error while using a command:\n`Required arguments were not specified.`"
        channel = client.get_channel(820659051007967232)
        await channel.send(embed=e)

    if isinstance(error, commands.MissingPermissions):
        ie = discord.Embed()
        ie.add_field(name='error while processing', value='You do not have the right permissions.')
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
        ie.description=f"this command is on cooldown, wait **{cdamount}** more seconds, please wait."
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

    cmd_edits = {}

@client.command()
@commands.is_owner()
async def load(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to load next time")
        return
    client.load_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Loaded {extension}")

@client.command()
@commands.is_owner()
async def unload(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to unload next time")
        return
    client.unload_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Unloaded {extension}")

@client.command()
@commands.is_owner()
async def reload(ctx, extension = None):
    if extension == None:
        await ctx.message.reply("tell me what to reload next time ")
        return
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.message.reply(f"Reloaded {extension}")

@client.command()
@commands.is_owner()
async def meow(ctx, meowdat = None):
    if meowdat == None:
        await ctx.message.reply("who should i meow at?")
        return
    embed = discord.Embed(
    title="ZeroTwo.py",
    description=f"meow meow {meowdat}"
)
    await ctx.message.reply(embed=embed)


client.run(TOKEN)

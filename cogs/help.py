import discord 
from discord.ext import commands 
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Shows this message", aliases=['halp', 'commands'])
    async def help(self, ctx, *commands: str):
        bot = ctx.bot

        PREFIX = "py "
        MAIN_COLOR = 0xff0000
        embed = discord.Embed(
            title=f"ZeroTwo.py ({len(self.client.all_commands)} commands)",
            description=f'If you need more info on a command, execute`{PREFIX}help <cmd>`',
            color = MAIN_COLOR
        )

        def generate_usage(command_name):
            """ Generates a string of how to use a command """
            temp = f'{PREFIX}'
            command = bot.get_command(command_name)
            # Aliases
            if len(command.aliases) == 0:
                temp += f'{command_name}'
            elif len(command.aliases) == 1:
                temp += f'[{command.name}|{command.aliases[0]}]'
            else:
                t = '|'.join(command.aliases)
                temp += f'[{command.name}|{t}]'
            # Parameters
            params = f' '
            for param in command.clean_params:
                params += f'<{command.clean_params[param]}> '
            temp += f'{params}'
            return temp

        def generate_command_list(cog):
            # Determine longest word
            max = 0
            for command in bot.get_cog(cog).get_commands():
                if not command.hidden:
                    if len(f'{command}') > max:
                        max = len(f'{command}')
            # Build list
            temp = ""
            for command in bot.get_cog(cog).get_commands():
                if command.hidden:
                    temp += ''
                elif command.help is None:
                    temp += f'{command}\n'
                else:
                    temp += f'`{command}`'
                    for i in range(0, max - len(f'{command}') + 1):
                        temp += '   '
                    temp += f'- {command.help}\n'
            return temp

        embeds = [embed]

        if len(commands) == 0:
            for cog in bot.cogs:
                temp = generate_command_list(cog)
                if temp != "":
                    embed = discord.Embed(title=f'**{cog}**', description=temp, color=MAIN_COLOR)
                    embeds.append(embed)

        elif len(commands) == 1:
            # Try to see if it is a cog name
            name = commands[0].capitalize()
            command = None

            if name in bot.cogs:
                cog = bot.get_cog(name)
                msg = generate_command_list(name)
                embed.add_field(name=name, value=msg, inline=False)
                msg = f'{cog.description}\n'
                embed.set_footer(text=msg)

            # Must be a command then
            else:
                command = bot.get_command(name)
                if command is not None:
                    help = f''
                    if command.help is not None:
                        help = command.help
                    embed.add_field(name=f'**{command}**',
                                    value=f'{command.description}```{generate_usage(name)}```\n{help}',
                                    inline=False)
                else:
                    msg = ' '.join(commands)
                    embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')
        else:
            msg = ' '.join(commands)
            embed.add_field(name="Not found", value=f'Command/category `{msg}` not found.')

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

def setup(client):
    client.add_cog(Help(client))
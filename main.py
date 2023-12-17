import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot conectado como {0.user}'.format(bot))

@bot.command()
async def send_files(ctx):
    directory = '/caminho/para/seu/diretorio'

    for filename in os.listdir(directory):
        if filename.startswith("Python"):
            # Substitua pelo ID do canal Python
            channel = bot.get_channel(1184522501439623179)
        elif filename.startswith("Javascript"):
            # Substitua pelo ID do canal Javascript
            channel = bot.get_channel(1184522419348701285)
        else:
            continue

        await channel.send(file=discord.File(os.path.join(directory, filename)))

bot.run('MTE4NTIxOTI2NjY2NTAwOTIwMw.GgLR_l.bnnibbhW0wt6BulRjNJ5vwPmCA6j3R01SCszEw')

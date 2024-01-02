import discord
import keyring
from discord.ext import commands
from config import setup_commands

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')
    try:
        synced = await bot.tree.sync()
        print(f'sincronizando {len(synced)} comando(s)')
    except Exception as e:
        print(e)

setup_commands(bot)

bot.run(keyring.get_password('bot_book', 'token'))

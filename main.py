import discord
import keyring
from discord.ext import commands
import config as config

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_command(config.comandos)
bot.add_command(config.categoria)
bot.add_command(config.livro)
bot.add_command(config.proxima)
bot.add_command(config.anterior)

bot.run(keyring.get_password('bot_book', 'token'))
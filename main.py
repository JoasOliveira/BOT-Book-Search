import os
import keyring
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot online')
    await check_files_in_directory('E:/Livros')


async def send_file_to_discord(file_path, channel_id):
    channel = bot.get_channel(channel_id)
    with open(file_path, 'rb') as fp:
        await channel.send(file=discord.File(fp, os.path.basename(file_path)))

async def check_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.startswith('java'):
            await send_file_to_discord(os.path.join(directory, filename), 1184522501439623179)
        elif filename.startswith('python'):
            await send_file_to_discord(os.path.join(directory, filename), 1186401484431171614)

bot.run(keyring.get_password('bot_book', 'token'))
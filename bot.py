import discord
import keyring
from discord.ext import commands
from discord.ui import View, Button

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')
    try:
        synced = await bot.tree.sync()
        print(f'sincronizando {len(synced)} comando(s)')
    except Exception as e:
        print(e)

    # Mensagem de inicialização
    startup_message = (
        "Olá! Eu sou o seu assistente de leitura.\n"
        "Estou aqui para ajudá-lo a encontrar livros sobre várias categorias e tópicos.\n"
        "Por favor, selecione uma ação abaixo:"
    )
    
    # Cria uma view 
    view = View()

    # Adicione botões à view
    button = Button(style=discord.ButtonStyle.primary, label="Mostrar Categorias", custom_id="show_categories")
    button.callback = show_categories_callback  # Atribuindo o callback method
    view.add_item(button)
    
    # Enviar mensagem com os botões no Canal especifico do Bot no Servidor Discord
    channel = bot.get_channel(1231763443128864832)  # Substitua pelo ID do canal desejado
    if channel:
        await channel.send(content=startup_message, view=view)
    else:
        print("Canal não encontrado. Certifique-se de substituir o ID do canal pelo correto.")

# Callback method para o botão
async def show_categories_callback(interaction: discord.Interaction):
    # Cuide da interação aqui
    await interaction.response.send_message("As categorias serão mostradas aqui.")

bot.run(keyring.get_password('discord_book', 'token'))

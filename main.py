import os
import discord
import keyring
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Mapeamento de prefixos para IDs de canais
help_options = {
    '1': {
        'category': 'Linguagens de Programação',
        'options': ['Angular', 'C++', 'C#', 'Elixir', 'GO', 'Java', 'JavaScript', 'Linguagem R', 'Pascal', 'PHP', 'Python', 'Ruby', 'VueJS']
    },
    '2': {
        'category': 'Ferramentas e Tecnologias',
        'options': ['APis', 'Arduino', 'Doker', 'GIT _ GITHUB', 'HTML e CSS', 'Markdown', 'MongoDB', 'NodeJS', 'React', 'Redis', 'SQL', 'Shell Script', 'Virtual Box']
    },
    '3': {
        'category': 'Conceitos e Metodologias',
        'options': ['Agile', 'Algoritmo e Programação', 'Aprimoramento de Skills', 'Arquitetura de Computadores', 'BI', 'BITCOIN _ BLOCKCHAIN', 'Banco de Dados', 'Big Data', 'ChatGPT', 'Ciência da Computação', 'Compiladores', 'Computação Gráfica', 'Computação Quântica', 'Computação em Nuvem', 'Crypto e Mineração', 'Data Science', 'Deep Learning', 'Design Thinking', 'Design', 'Eletronica', 'Engenharia de Software', 'Estatística e Ciência de Dados', 'Fonética e Ortografia', 'Games', 'Inteligência Artificial', 'IoT', 'Lógica', 'Machine Learning', 'Orientação a Objetos', 'Redes de Computadores', 'Requisitos de Software', 'SCRUM', 'Segurança da Informação', 'Sistemas Operacionais', 'Startup', 'Teoria da Computação', 'Teoria dos Grafos', 'UX Design', 'WebDesign']
    }
}
OPTIONS_PER_PAGE = 10
current_page = 0
current_category = None
selected_option = None


@bot.command(name='comandos')
async def help_book(ctx):
    global current_page
    global current_category
    current_page = 0
    current_category = None
    help_message = "Aqui estão as categorias disponíveis:\n"
    for key, value in help_options.items():
        help_message += f"{key}_{value['category']}\n"
    await ctx.send(help_message)


@bot.command(name='categoria')
async def select_category(ctx, category):
    global current_category
    if category in help_options:
        current_category = help_options[category]
        await ctx.send(f"Categoria {current_category['category']} selecionada.")
        await send_help_page(ctx)
    else:
        await ctx.send("Categoria inválida. Por favor, selecione uma categoria válida.")


@bot.command(name='livro')
async def select_option(ctx, option):
    global selected_option
    if current_category is not None and option in current_category['options']:
        selected_option = option
        await ctx.send(f"Opção {selected_option} selecionada.")
        await check_files_in_directory('G:/Livros', ctx.author)
    else:
        await ctx.send("Opção inválida. Por favor, selecione uma opção válida.")


@bot.command(name='proxima')
async def help_book_next(ctx):
    global current_page
    current_page += 1
    await send_help_page(ctx)


@bot.command(name='anterior')
async def help_book_previous(ctx):
    global current_page
    current_page = max(0, current_page - 1)
    await send_help_page(ctx)


async def send_help_page(ctx):
    if current_category is None:
        await ctx.send("Por favor, selecione uma categoria primeiro.")
        return

    start_index = current_page * OPTIONS_PER_PAGE
    end_index = start_index + OPTIONS_PER_PAGE
    page_options = current_category['options'][start_index:end_index]
    help_message = f"Aqui estão as opções disponíveis para 
    {current_category['category']}:\n"
    for option in page_options:
        help_message += f"- {option}\n"
    await ctx.send(help_message)


async def check_files_in_directory(directory, user):
    global selected_option
    if selected_option is None:
        print("Nenhuma opção selecionada.")
        return

    for filename in os.listdir(directory):
        if selected_option in filename:
            await send_file_to_discord(os.path.join(directory, filename), user)


async def send_file_to_discord(filepath, user):
    with open(filepath, 'rb') as f:
        await user.send(file=discord.File(f))

bot.run(keyring.get_password('bot_book', 'token'))

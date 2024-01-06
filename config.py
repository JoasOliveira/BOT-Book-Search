import os
import discord
from discord.ext import commands

help_options = {
    '1': {
        'category': 'Linguagens de Programação',
        'options': ['1 - Angular', '2 - C++', '3 - C#', '4 - Elixir', '5 - GO', '6 - Java', '7 - JavaScript', '8 - Linguagem R', '9 - Pascal', '10 - PHP', '11 - Python', '12 - Ruby', '13 - VueJS', '14 - .NET']
    },
    '2': {
        'category': 'Ferramentas e Tecnologias',
        'options': ['1 - APis', '2 - Arduino', '3 - Doker', '4 - GIT _ GITHUB', '5 - HTML e CSS', '6 - Markdown', '7 - MongoDB', '8 - NodeJS', '9 - React', '10 - Redis', '11 - SQL', '12 - Shell Script', '13 - Virtual Box']
    },
    '3': {
        'category': 'Conceitos e Metodologias',
        'options': ['1 - Agile', '2 - Algoritmo e Programação', '3 - Android', '4 - Aplicações Web e Mobile', '5 - primoramento de Skills', '6 - Arquitetura de Computadores', '7 - BI', '8 - BITCOIN _ BLOCKCHAIN', '9 - Banco de Dados', '10 - Big Data', '11 - ChatGPT', '12 - Ciência da Computação', '13 - Compiladores', '14 - Computação Gráfica', '15 - Computação Quântica', '16 - Computação em Nuvem', '17 - Crypto e Mineração', '18 - Data Science', '19 - Deep Learning', '20 - Design Thinking', '21 - Design', '22 - Eletronica', '23 - Engenharia de Software', '24 - Estatística e Ciência de Dados', '25 - Fonética e Ortografia', '26 - Games', '27 - Inteligência Artificial', '28 - IoT', '29 - Lógica', '30 - Machine Learning', '31 - Orientação a Objetos', '32 - Redes de Computadores', '33 - Requisitos de Software', '34 - SCRUM', '35 - Segurança da Informação', '36 - Sistemas Operacionais', '37 - Startup', '38 - Teoria da Computação', '39 - Teoria dos Grafos', '40 - UX Design', '41 - WebDesign']
    },
}

OPTIONS_PER_PAGE = 35
current_page = 0
current_category = None
selected_option = None

mensage_comandos = 'Lista todos as categorias disponiveis para seleção | digite o comando /categorias'
mensage_categoria = 'Selecionar uma das categorias | digite o comando /categoria <numero>'
mensage_livro = 'Escolher um dos livros | digite o comando /livro <nome do livro>'
mensage_proxima = 'Passa para a proxima pagina | digite o comando /proxima'
mensage_anterior = 'Volta para a pagina anterior | digite o comando /anterior'

def setup_commands(bot):
  @bot.tree.command(name='categorias', description=f'{mensage_comandos}')
  async def comandos(interaction: discord.Interaction):
    global current_page
    global current_category
    current_page = 0
    current_category = None
    categories = [f"{key} - {value['category']}" for key,
                  value in help_options.items()]
    max_length = max(len(category) for category in categories)
    border = "-" * (max_length + 4)
    title = "-- Categorias --"
    title_padding = " " * ((max_length - len(title)) // 2)  # Adicionado espaços para centralizar o título
    help_message = title_padding + title + "\n" + border + "\n"
    for category in categories:
        category_line = f"| {category.ljust(max_length)} |"
        help_message += category_line + "\n"
    help_message += border
    await interaction.response.send_message(f"```\n{help_message}\n```")

  @bot.tree.command(name='selecionar_categorias', description=f'{mensage_categoria}')
  async def categoria(interaction: discord.Interaction, category: str):
      global current_category
      if category in help_options:
          current_category = help_options[category]
          await interaction.response.send_message(f"Categoria {current_category['category']} selecionada.")
          await send_help_page(interaction)
      else:
          await interaction.response.send_message("Categoria inválida. Por favor, selecione uma categoria válida.")

  @bot.tree.command(name='escolher_livro', description=f'{mensage_livro}')
  async def livro(interaction: discord.Interaction, option: str):
    global selected_option
    if current_category is not None:
        try:
            # Subtrai 1 porque a lista de opções é baseada em zero
            option_index = int(option) - 1
            if 0 <= option_index < len(current_category['options']):
                # Pega o texto da opção correspondente ao número
                selected_option = current_category['options'][option_index].split('- ')[1]
                await interaction.response.send_message(f"Opção {selected_option} selecionada.")
                await check_files_in_directory('G:/Livros', interaction.user)
            else:
                await interaction.response.send_message("Opção inválida. Por favor, selecione uma opção válida.")
        except ValueError:
            await interaction.response.send_message("Por favor, insira um número válido.")
    else:
        await interaction.response.send_message("Categoria inválida. Por favor, selecione uma categoria válida.")

  @bot.tree.command(name='proxima', description=f'{mensage_proxima}')
  async def proxima(interaction: discord.Interaction):
      global current_page
      current_page += 1
      await send_help_page(interaction)

  @bot.tree.command(name='anterior', description=f'{mensage_anterior}')
  async def anterior(interaction: discord.Interaction):
      global current_page
      current_page = max(0, current_page - 1)
      await send_help_page(interaction)

  async def send_help_page(interaction: discord.Interaction):
      if current_category is None:
          message = "Por favor, selecione uma categoria primeiro."
      else:
          start_index = current_page * OPTIONS_PER_PAGE
          end_index = start_index + OPTIONS_PER_PAGE
          options_to_display = current_category['options'][start_index:end_index]
          category_name = f" Escolha seu livro: {current_category['category']} "
          max_length = max(len(option)
                           for option in options_to_display + [category_name])
          options_message = "\n".join(
              f"| 📖{option.ljust(max_length)} |" for option in options_to_display)
          border = "-" * (max_length + 6)  # Ajustado para acomodar o emoji
          category_name = category_name.center(len(border), "-")
          options_message = f"{category_name}\n{border}\n{options_message}\n{border}"
          # Calcula o número total de páginas
          total_pages = - \
              (-len(current_category['options']) // OPTIONS_PER_PAGE)
          # Adiciona a contagem de páginas
          page_count = f"Página <{current_page + 1}/{total_pages}>"
          # Centraliza a contagem de páginas
          page_count = page_count.center(len(border))
          message = f"```\n{options_message}\n{page_count}\n```"
      if not interaction.response.is_done():
          await interaction.response.send_message(message)
      else:
          await interaction.followup.send(message)

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
        await user.send(file=discord.File(f, filename='Comunidade Developers ' + os.path.basename(filepath)))

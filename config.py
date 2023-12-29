import os
import discord
from discord.ext import commands

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
        'options': ['Agile', 'Algoritmo e Programação', 'primoramento de Skills', 'Arquitetura de Computadores', 'BI', 'BITCOIN _ BLOCKCHAIN', 'Banco de Dados', 'Big Data', 'ChatGPT', 'Ciência da Computação', 'Compiladores', 'Computação Gráfica', 'Computação Quântica', 'Computação em Nuvem', 'Crypto e Mineração', 'Data Science', 'Deep Learning', 'Design Thinking', 'Design', 'Eletronica', 'Engenharia de Software', 'Estatística e Ciência de Dados', 'Fonética e Ortografia', 'Games', 'Inteligência Artificial', 'IoT', 'Lógica', 'Machine Learning', 'Orientação a Objetos', 'Redes de Computadores', 'Requisitos de Software', 'SCRUM', 'Segurança da Informação', 'Sistemas Operacionais', 'Startup', 'Teoria da Computação', 'Teoria dos Grafos', 'UX Design', 'WebDesign']
    },
    '4': {
        'category': 'Solicitar Conteudo',
        'options': ['Solicitar Conteudo']
    },
}

OPTIONS_PER_PAGE = 10
current_page = 0
current_category = None
selected_option = None

mensage_comandos = 'Lista todos os comandos disponiveis para seleção | digite o comando /comandos'
mensage_categoria = 'Lista todos as categorias disponiveis para seleção | digite o comando /categoria <numero da categoria>'
mensage_livro = 'Lista todos os livros disponiveis para seleção | digite o comando /livro <nome do livro>'
mensage_proxima = 'Passa para a proxima pagina | digite o comando /proxima'
mensage_anterior = 'Volta para a pagina anterior | digite o comando /anterior'


def setup_commands(bot):
  @bot.tree.command(name='comandos', description=f'{mensage_comandos}')
  async def comandos(interaction: discord.Interaction):
      global current_page
      global current_category
      current_page = 0
      current_category = None
      categories = [f"{key} - {value['category']}" for key,
                    value in help_options.items()]
      max_length = max(len(category) for category in categories)
      border = "-" * (max_length + 4)
      help_message = border + "\n"
      for category in categories:
          category_line = f"| {category.ljust(max_length)} |"
          help_message += category_line + "\n"
      help_message += border
      await interaction.response.send_message(f"```\n{help_message}\n```")

  @bot.tree.command(name='categoria', description=f'{mensage_categoria}')
  async def categoria(interaction: discord.Interaction, category: str):
      global current_category
      if category in help_options:
          current_category = help_options[category]
          await interaction.response.send_message(f"Categoria {current_category['category']} selecionada.")
          await send_help_page(interaction)
      else:
          await interaction.response.send_message("Categoria inválida. Por favor, selecione uma categoria válida.")

  @bot.tree.command(name='livro', description=f'{mensage_livro}')
  async def livro(interaction: discord.Interaction, option: str):
      global selected_option
      if current_category is not None and option in current_category['options']:
          selected_option = option
          await interaction.response.send_message(f"Opção {selected_option} selecionada.")
          await check_files_in_directory('G:/Livros', interaction.user)
      else:
          await interaction.response.send_message("Opção inválida. Por favor, selecione uma opção válida.")

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
          category_name = f" Categoria: {current_category['category']} "
          max_length = max(len(option)
                           for option in options_to_display + [category_name])
          options_message = "\n".join(
              f"| {option.ljust(max_length)} |" for option in options_to_display)
          border = "-" * (max_length + 4)
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
          await user.send(file=discord.File(f))

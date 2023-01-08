# ToDo
# X (3) - Modificar onde que a função de salvar histórico é chamada (adicionar depois de modificar o arquivo banco_de_dados)
# X (5) - Modificar formatação do historico.txt e adicionar quem que executou (ex. Fuguetero#9379 adicionou "lavar roupas")
# X (5) - Adicionar função de mostrar histórico completo
# (5) - Adicionar salvamento de horário no histórico
# (2) - Salvar unix sem decimal
# (18) mandar "como voce está" pro namorado durante o dia
# (8) - Adicionar filtro de tarefa no comando de ver histórico (Ex. //historico adicionar)
# (13) - Adicionar filtro de pessoa no comando de ver histórico (Ex. //historico @nathalia)
# (8) - Adicionar filtros múltiplos no comando de ver histórico (Ex. //historico @nathalia adicionar)
# (5) - Adicionar caso usuário insira mais de um usuário (Ex. //historico @nathalia @victor) as ações dos 2

from discord.ext import commands
from discord import Intents
import datetime

# Constantes
with open('token.txt', 'r') as arquivo:
    # Lendo o token do bot do arquivo toke.txt
    TOKEN = arquivo.read()
PREFIX = '//'

CROSS_EMOJI = ':x:'
CHECK_EMOJI = ':white_check_mark:'

# Configura o bot
bot = commands.Bot(command_prefix=PREFIX, intents=Intents.all(), self_bot=False)
bot.remove_command('help')


def conteudo(ctx):
    # 1 - Pega o conteudo inteiro da mensagem
    texto = ctx.message.content
    # 2 - remover tudo antes do primeiro espaço
    texto = texto.split(' ', 1)
    # 3 - retornar restante
    if len(texto) == 1:
        return ''

    return texto[1]


def pegar_autor(ctx):
    autor = ctx.author
    return autor


def adicionar_historico(tarefa):
    # Formatar ações
    tarefa = tarefa.split('//', 1)
    mensagem = ''
    for texto in tarefa:
        mensagem += f'{texto}\n'
    # Adiciona as ações dentro da tarefa
    with open('historico.txt', 'a') as arquivo:
        arquivo.write(f'{mensagem}')


def formatar_tarefas(tarefas):
    # Constroi mensagem para enviar no estilo "-> (nome da tarefa)\n"
    mensagem = 'Tarefas adicionadas:\n'
    for tarefa in tarefas:
        mensagem += f'-> {tarefa}\n'

    return mensagem


def ler_tarefas():
    # Lê banco de dados
    with open('banco_de_dados.txt', 'r') as arquivo:
        texto = arquivo.read().strip().split('\n')

    return texto


def adicionar_tarefa(tarefa):
    # Adiciona tarefa no banco de dados
    with open('banco_de_dados.txt', 'a') as arquivo:
        arquivo.write(f'{tarefa}\n')


def sobrescrever_tarefas(tarefas):
    texto = '\n'.join(tarefas)

    with open('banco_de_dados.txt', 'w') as arquivo:
        arquivo.write(texto)


def mostrar_historico():
    # Ler historico
    aux = ''
    with open('historico.txt', 'r') as arquivo:
        texto = arquivo.read().strip().split('\n')

    lista = []
    for i in texto:
        aux = i.split(' ', 1)
        lista.append(aux)

        print(lista)

    return lista


@bot.event
async def on_ready():
    print('Ready!')


@bot.command(pass_context=True)
async def teste(ctx):
    print(f'Fui testado por {ctx.author.name}')

    await ctx.send(f'Fui testado por {ctx.author.name}')


@bot.command(pass_context=True)
async def mostrar(ctx):
    # Lê banco de dados
    tarefas = ler_tarefas()

    tarefas = formatar_tarefas(tarefas)

    data = datetime.datetime.now()
    unix_data = datetime.datetime.timestamp(data)

    autor = pegar_autor(ctx)

    texto = f'{unix_data} {autor} vizualizou as tarefas'
    adicionar_historico(texto)

    await ctx.send(tarefas)


@bot.command(pass_context=True)
async def adicionar(ctx):
    tarefa = conteudo(ctx)

    if not tarefa:
        await ctx.send('Digite a tarefa junto do comando!')
        return

    # Lê banco de dados
    tarefas = ler_tarefas()

    # Checa se a tarefa já foi adicionada
    if tarefa in tarefas:
        await ctx.send(f'{CROSS_EMOJI} "{tarefa}" já foi adicionado!')
        return

    # Adiciona tarefa no banco de dados
    with open('banco_de_dados.txt', 'a') as arquivo:
        arquivo.write(f'{tarefa}\n')

    data = datetime.datetime.now()
    unix_data = datetime.datetime.timestamp(data)

    autor = pegar_autor(ctx)

    texto = f'{unix_data} - {autor} adicionou "{tarefa}"'
    adicionar_historico(texto)

    await ctx.send(f'{CHECK_EMOJI} "{tarefa}" adicionado com sucesso!')


@bot.command(pass_context=True)
async def concluir(ctx):
    tarefa = conteudo(ctx)

    if not tarefa:
        await ctx.send('Digite a tarefa junto do comando!')
        return

    # Lê banco de dados
    tarefas = ler_tarefas()

    # Se a tarefa não estiver na lista
    if tarefa not in tarefas:
        await ctx.send(f'"{tarefa}" não faz parte da sua lista de tarefas')
        return

    tarefas.remove(tarefa)

    sobrescrever_tarefas(tarefas)

    string_tarefas = formatar_tarefas(tarefas)

    data = datetime.datetime.now()
    unix_data = datetime.datetime.timestamp(data)

    autor = pegar_autor(ctx)

    texto = f'{unix_data} {autor} concluiu "{tarefa}"'
    adicionar_historico(texto)

    await ctx.send(f'"{tarefa}" concluído.\n{string_tarefas}')


@bot.command(pass_context=True)
async def excluir(ctx):
    tarefa = conteudo(ctx)

    if not tarefa:
        await ctx.send('Digite a tarefa junto do comando!')
        return

    tarefas = ler_tarefas()

    if tarefa not in tarefas:
        await ctx.send(f'"{tarefa}" não faz parte da sua lista de tarefas')
        return

    tarefas.remove(tarefa)

    sobrescrever_tarefas(tarefas)

    string_tarefas = formatar_tarefas(tarefas)

    data = datetime.datetime.now()
    unix_data = datetime.datetime.timestamp(data)

    autor = pegar_autor(ctx)

    texto = f'{unix_data} {autor} excluiu "{tarefa}"'
    adicionar_historico(texto)

    await ctx.send(f'"{tarefa}" excluído.\n{string_tarefas}')


@bot.command(pass_context=True)
async def historico(ctx):
    string_historico = mostrar_historico()

    await ctx.send('----- Histórico -----')
    await ctx.send(string_historico)

    data = datetime.datetime.now()
    unix_data = datetime.datetime.timestamp(data)

    autor = pegar_autor(ctx)
    texto = f'{unix_data} {autor} vizualizou o historico'
    adicionar_historico(texto)


# Roda o bot
bot.run(TOKEN)

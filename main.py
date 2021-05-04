import discord
import json
import requests
import inspect
import random
import os
import ast
import platform
import time 
from discord import gateway
import discord
from discord.ext import tasks
from discord.utils import get
import sqlite3 
from tabulate import tabulate 
from config import settings
from discord.ext import commands
from config import settings
import asyncio
import io


import textwrap
from traceback import format_exception

bot = commands.Bot(command_prefix = settings['prefix'])
bot.remove_command( "help" )

print("Бот загружается...")

@bot.event
async def on_ready():
		await bot.change_presence(status = discord.Status.online, activity= discord.Activity(name=f'Музыку || d!helps', type= discord.ActivityType.listening))
		for guild in bot.guilds:
				print ("      Сервера На Которых Есть Бот:")
				print ("   SERVER:", guild.name)
				print ("   ID:", guild.id)
print (" Bot connected to discord")
					
def insert_returns(body):
 
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])


    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)


    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

@bot.command()
async def avatar(ctx, *, avamember: discord.Member):
    emb = discord.Embed(title = f"Аватар {avamember.name}", colour = discord.Color.red())
    emb.set_image(url = avamember.avatar_url)
    await ctx.send(embed = emb)

@avatar.error
async def Avatar_error(ctx, error):
     if isinstance(error, commands.MissingRequiredArgument):
         emb = discord.Embed(title = f"Аватар {ctx.author.name}", colour = discord.Color.red())
         emb.set_image(url = ctx.author.avatar_url)
         await ctx.send(embed = emb)


@bot.command()
async def info(ctx):
    guilds = await bot.fetch_guilds(limit = None).flatten()    # Получение всех серверов где есть бот
    emb = discord.Embed(title = "Статистика", colour = discord.Color.red())
    emb.add_field(name = "Основная:", value = f"Серверов: **{len(guilds)}**\nУчастников: **{len(set(bot.get_all_members()))}**")    # 1: Количество серверов, 2: количество уникальных участников на всех серверах
    emb.add_field(name = "Бот:", value = f"Задержка: **{int(bot.latency * 1000)} мс**") # Скорость соединения бота с API дискорда
    await ctx.send(embed = emb)

@bot.command()
async def server(ctx):
    bot, human = 0, 0
    for member in  ctx.message.guild.members:
        if member.bot:
            bot += 1
        else:
            human += 1
    emojic = 0
    for emoji in ctx.message.guild.emojis:
        emojic += 1
    text, voice = len(ctx.message.guild.text_channels), len(ctx.message.guild.voice_channels)
    emb = discord.Embed(title = "Инфо о сервере", colour = discord.Color.red())
    emb.set_thumbnail(url = ctx.message.guild.icon_url)
    emb.description = f"Название: **{ctx.message.guild.name}**"
    emb.add_field(name = "Участники:", value = f"Всего: **{bot + human}**\nЛюдей: **{human}**\nБотов: **{bot}**")
    emb.add_field(name = "Эмоций:", value = emojic)
    emb.add_field(name = "Каналы:", value = f"Всего: **{text + voice}**\nТекстовых: **{text}**\nГолосовых: **{voice}**")
    emb.add_field(name = "Владелец:", value = ctx.message.guild.owner)
    emb.add_field(name = "Регион:", value = ctx.message.guild.region)
    emb.add_field(name = "Уровень проверки:", value = ctx.message.guild.verification_level)
    emb.add_field(name = "AFK:", value = f"Канал: **{ctx.message.guild.afk_channel}**\nТаймаут: **{ctx.message.guild.afk_timeout}**")
    emb.set_footer(text = f"ID: {ctx.message.guild.id}")
    await ctx.send(embed = emb)


log = gateway.log

async def identify(self):
    """Sends the IDENTIFY packet."""
    payload = {
        "op": self.IDENTIFY,
        "d": {
            "token": self.token,
            "properties": {
                "$os": "android",
                "$browser": "Discord Android",
                "$device": "discord.py",
                "$referrer": "",
                "$referring_domain": "",
            },
            "compress": True,
            "large_threshold": 250,
            "guild_subscriptions": self._connection.guild_subscriptions,
            "v": 3,
        },
    }

    if not self._connection.is_bot:
        payload["d"]["synced_guilds"] = []

    if self.shard_id is not None and self.shard_count is not None:
        payload["d"]["shard"] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload["d"]["presence"] = {
            "status": state._status,
            "game": state._activity,
            "since": 0,
            "afk": False,
        }

    if state._intents is not None:
        payload["d"]["intents"] = state._intents.value

    await self.call_hooks(
        "before_identify", self.shard_id, initial=self._initial_identify
    )
    await self.send_as_json(payload)
    log.info("Shard ID %s has sent the IDENTIFY payload.", self.shard_id)


gateway.DiscordWebSocket.identify = identify
discord.gateway.DiscordWebSocket.identify = identify

@bot.command()
async def ping(ctx):
     await ctx.send(f'Пинг бота:  {round(bot.latency * 1000)}ms')

@bot.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))
    embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name='Bot Version:', value='1.2')
    embed.add_field(name='Версия питона:', value=pythonVersion)
    embed.add_field(name='Discord.Py версия', value=dpyVersion)
    embed.add_field(name='Число серверов:', value=serverCount)
    embed.add_field(name='Число всех учасников:', value=memberCount)
    embed.add_field(name='Разработчик бота:', value="BrokenInk#1212")
    embed.set_footer(text=f"{bot.user.name}")
    await ctx.send(embed=embed)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 599667143075823683
    return commands.check(predicate)

@bot.command(name='eval')
@is_owner()
async def _eval(ctx, *, code):
    """A bad example of an eval command"""
    await ctx.send(eval(code))



@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Рандом Лис') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    print("Выполнена команда d!fox")
    await ctx.send(embed = embed) # Отправляем Embed


@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Рандом Собачки') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    print("Выполнена команда d!dog")
    await ctx.send(embed = embed) # Отправляем Embed    



@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Рандом Котёнка') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    print("Выполнена команда d!cat")
    await ctx.send(embed = embed) # Отправляем Embed



@bot.command()
@commands.has_permissions(manage_messages=True, kick_members=True)
async def clear(ctx, amount=1):
    channel = ctx.message.channel
    await ctx.send(f'Очищено {amount} сообщений')
    if ctx.message.author.guild_permissions.manage_messages:
        await channel.purge(limit=amount, check=None, bulk=True)
        print(f'Выполнена комманда d!clear {amount}')
@clear.error
async def clear_error(ctx, error):
    await ctx.send( 'У Вас недостаточно прав для использования этой команды!' '\n' 'Недостающее право: Управлять сообщениями.' )



@bot.command()
async def helps(ctx):
    message_help = discord.Embed(
        description = '''
        **Основное**

        `d!cat` - Рандомное изображение кота😸
        `d!dog` - Рандомное изображение собаки🐕
        `d!fox` - Рандомное изображение лисы🦊
        `d!avatar` - Аватар пользователя

        **Информация**

        `d!stats` - Статистика бота
        `d!ping` - Информация о пинге бота
        `d!info` - Информация о боте
        `d!server` - Информация о сервере
        `d!invite` - Узнать ссылку приглашения бота на сервер

        **Модерационное **

        `d!mute <@user> reason` - Дать наказание участнику в виде мута
        `d!unmute <@user>` - Снять наказание в виде мута
        `d!clear` - Очищение сообщений
        `d!say <message>` - Отправить сообщение от бота 🌐

        **Для Создателя**
        `d!eval` - eval command
        *©Автор BrokenInk, все права замяуканны. 2021-2022*''',
        colour = discord.Colour.from_rgb(106, 192, 245))
    await ctx.send(embed = message_help)
#        `#botserver` - оффициальный сервер бота 🏙
async def is_owner(ctx):
    return ctx.author.id == 599667143075823683

def user_is_me(ctx):
    return ctx.message.author.id == "599667143075823683" 


@bot.command()
@commands.has_permissions( manage_messages = True )
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount);
    await ctx.send(arg)

@say.error
async def say_error(ctx, error):
    await ctx.send( 'У Вас недостаточно прав для использования этой команды!' '\n' 'Недостающее право: Управлять сообщениями' '\n' 'Либо вы забыли указать аргументы(тоесть текст) - d!say text')



@bot.command()
async def invite(ctx):
    message_help = discord.Embed(
        description = '''
        Чтобы добавить меня на свой сервер, [Нажми сюда!](https://discord.com/api/oauth2/authorize?client_id=823153310152261634&permissions=8&scope=bot)
        *©Автор BrokenInk, все права замяуканны. 2021-2022*''',
        colour = discord.Colour.from_rgb(106, 192, 245))
    await ctx.send(embed = message_help)


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True, kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="「🛑」Наказан")

    if not mutedRole:
        mutedRole = await guild.create_role(name="「🛑」Наказан")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Авто-Модерация", description=f"Участнику: {member.mention} было выдано наказание ввиде мута", colour=discord.Colour.red())
    embed.add_field(name="Причина:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" Вам выдали мут на сервере: {guild.name}, Причина: {reason}")
@mute.error
async def mute_error(ctx, error):
    await ctx.send( 'У Вас недостаточно прав для использования этой команды!' '\n' 'Недостающее право: Управлять сообщениями, Кикать участников.' )

@bot.command(description="Участник размьючен")
@commands.has_permissions(manage_messages=True, kick_members=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="「🛑」Наказан")

   await member.remove_roles(mutedRole)
   embed = discord.Embed(title="Авто-Модерация", description=f" С участника: {member.mention} Сняты все наказания",colour=discord.Colour.blue())
   await member.send(f"С вас была снята блокировка чата на сервере: {ctx.guild.name}")
   await ctx.send(embed=embed)
@unmute.error
async def unmute_error(ctx, error):
    await ctx.send( 'У Вас недостаточно прав для использования этой команды!' '\n' 'Недостающее право: Управлять сообщениями, Кикать участников.' )


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

bot.run(settings['token'])
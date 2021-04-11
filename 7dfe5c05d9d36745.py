
#импорт библиотек
import json
import random
import discord 
import asyncio
from discord.ext import commands
from discord.utils import get
import sqlite3 
from tabulate import tabulate 
from config import settings
PREFIX = ['.']

bot = commands.Bot(command_prefix= PREFIX)

conn = sqlite3.connect("Discord.db")
cursor = conn.cursor()

#самостоятельный ввод и активация бд
cursor.execute("""CREATE TABLE IF NOT EXISTS "shop" (
	"id"	INT,
	"type"	TEXT,
	"name"	TEXT,
	"cost"	INT
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"id"	INT,
	"nickname"	TEXT,
	"mention"	TEXT,
	"money"	INT,
	"rep_rank"	TEXT,
	"inventory"	TEXT,
	"lvl"	INT,б
	"xp"	INT,
	"server_id"	INT
)""")

@bot.event 
async def on_ready():
	print("я запустився")
	vibor1 = int (input ("Введите пароль: "))
	if vibor1 == 767676:
		vibor = int (input ("Выбери 1, чтобы писать в чат. Введи 2, чтобы просматривать сообщения и активировать бд. "))
		if vibor == 1:
			while True:
				channel = bot.get_channel(813791811809181710)
				say = str (input ("Введи, что хочешь сказать: "))
				await channel.send(say)
		elif vibor == 2:
			for guild in bot.guilds:
				print ("сервера, на которых есть бот:")
				print (guild.name, guild.id)
				for member in guild.members:
					cursor.execute(f"SELECT id FROM users where id={member.id}")
					if cursor.fetchone()==None:
						cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@{member.id}>', 50000, 'S','[]',1, 0, {guild.id})")
					else:
						pass
					conn.commit()
		else:
			pass
	else:
		print("Неверный пароль! Доступ заблокирован!" )


#деньги за актив


#аккаунт





#стим



#отправка сообщений в консоль

@bot.command()
async def email(ctx, text):
	print(f'вам написал: {ctx.author}' )
	print(text)
	await ctx.message.add_reaction('✅')


#запуск бота

bot.run(settings['token'])


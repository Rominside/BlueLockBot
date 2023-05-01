from webserver import keep_alive
from bs4 import BeautifulSoup
from config import settings
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from replit import db
import discord
import time
import asyncio
import requests

keep_alive()
link = "https://w17.readbluelock.com/?2023-03-28"
flag_new_chapter = False
last_chapter = ""
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
Client = commands.Bot(command_prefix=settings["prefix"], intents=intents)


@Client.event
async def on_ready():
    print("Bot is ready")
    Check_last_chapter.start()
    


guild = discord.Object(id="254625044993409024")


@Client.slash_command(name="get_page", guild_ids=[254625044993409024])
@commands.guild_only()
async def Get_page(self):
    await self.response.send_message(settings["url"], ephemeral=True)

@Client.slash_command(name="get_time", guild_ids=[254625044993409024])
@commands.guild_only()
async def Get_time(self):
    actual_time = time.ctime()
    dt_1 = datetime.strptime(str(db["time_"]), "%a %b %d %H:%M:%S %Y")
    dt_2 = datetime.strptime(actual_time, "%a %b %d %H:%M:%S %Y")
    await self.response.send_message(dt_2 - dt_1, ephemeral=True)

@tasks.loop(seconds=300)
async def Check_last_chapter(self=Client):
      global counter
      global flag_new_chapter
      global last_chapter
      await self.wait_until_ready()
      channel = self.get_channel(254625044993409024)
    # while not self.is_closed():
      loc_counter = 0
      page = requests.get(link)
      soup = BeautifulSoup(page.text, "html.parser")
      chapters = soup.find("li", class_="widget ceo_latest_comics_widget")
      for chapter in reversed(chapters.findAll("li")):
        if chapter is not None:
          loc_counter += 1
          last_chapter = chapter.findNext("a").get("href")

      print(loc_counter)
      print(last_chapter)
      

      if loc_counter != db["last_chapter_number"]:
        db["last_chapter_number"] = loc_counter
        flag_new_chapter = True
      else:
        flag_new_chapter = False
        print("Chapter is not ready")
        print(loc_counter)
      if flag_new_chapter:
        db["time_"] = time.ctime()
        await channel.send("@everyone" + "  " + "new chapter is ready")
        await channel.send(last_chapter)
        flag_new_chapter = False
      # await asyncio.sleep(300)
      # github actions -- try two


Client.run(settings['token'])

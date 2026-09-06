import random
import time
import discord
from discord.ext import commands

# -------------------- ڕێکخستنی Intents --------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_message_count = {}
user_last_message_time = {}


@bot.event
async def on_ready():
  print(f"بۆتەکە ئۆنڵاین بوو وەکو: {bot.user.name}")
  await bot.change_presence(
      activity=discord.Game(name="!یارمەتی | Velvet Bot")
  )


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  user_id = message.author.id
  current_time = time.time()

  # -------------------- بەشی کۆنتڕۆڵی سپام (10-15 چات) --------------------
  if user_id not in user_last_message_time:
    user_last_message_time[user_id] = current_time
    user_message_count[user_id] = 1
  else:
    if current_time - user_last_message_time[user_id] < 15:
      user_message_count[user_id] += 1
    else:
      user_message_count[user_id] = 1
      user_last_message_time[user_id] = current_time

  # کاتێک کەسێک لە ناو 15 چسکەدا 10 بۆ 15 چات دەکات
  if user_message_count[user_id] >= 10:
    spam_responses = [
        f"وەی برایم {message.author.mention} هەندە زۆر مەڵێ تایپەکەت سووتا! 😂💀",
        (
            f"ئەرێ {message.author.mention} نەفەسێک وەربگرە، کیبۆردەکەت هاواری"
            " لێهات! ⌨️🔥"
        ),
        f"{message.author.mention} هێواشتر، مێشکمان چوو وەڵا! 🤫💤",
        (
            f"ئۆهۆ {message.author.mention} کاکە دەستت مەڕشێنە، کەمێک هێواشتر"
            " بە! 🗿"
        ),
        (
            f"{message.author.mention} ئەوە چیت لێهاتووە؟ ڕۆژنامەت بڵاوکردەوە لە"
            " چات! 🗞️😂"
        ),
    ]
    await message.channel.send(random.choice(spam_responses))
    user_message_count[user_id] = 0
    return

  # -------------------- پشکنینی تاگ و ڕیپلەی --------------------
  is_mentioned = bot.user.mentioned_in(message) and not message.mention_everyone
  is_reply_to_bot = False

  if message.reference and message.reference.message_id:
    try:
      referenced_msg = await message.channel.fetch_message(
          message.reference.message_id
      )
      if referenced_msg.author == bot.user:
        is_reply_to_bot = True
    except Exception:
      pass

  # وەڵامی کۆمیدی کاتێک کەسێک بۆتەکە تاگ دەکات یان ڕیپلەی دەداتەوە
  if is_mentioned or is_reply_to_bot:
    bot_tag_responses = [
        (
            f"وەی {message.author.mention} چییە دیسان تاگت کردمەوە؟ بەڵێن بێت"
            " ئیشم هەیە! 🗿"
        ),
        f"ها {message.author.mention}؟ فەرموو قسەکەت بکە گوێم لێتە! 😂",
        f"ئەرێ {message.author.mention} وازم لێ بێنە خەریکی چای خواردنەوەم! 🫖",
        (
            f"سڵاو لە {message.author.mention}، چی بڵێم وەڵا خۆم بەڕێوە دەبەم"
            " تاقەتی تۆم نییە 🤓"
        ),
        (
            f"تاگ مەکە {message.author.mention}، ئەگەرنا بە سێ ڕۆژ وەڵامت"
            " نادەمەوە! 💀"
        ),
        f"چییە {message.author.mention} دیسان لە بیرت چوو بەکارهێنانی بۆت؟ 🧐",
    ]
    await message.reply(random.choice(bot_tag_responses))
    return

  msg = message.content.lower()

  # -------------------- وشە کلیلەکانی تر --------------------
  if "حەمە" in msg:
    responses = [
        "گیانی حەمە، چی بڵێی؟ 😂",
        "وەڵا حەمە سەرقاڵە، پەیامەکەت بۆ جێبهێڵە!",
        "حەمە کوا لێرەیە؟ داوای چی ئەکەی؟ 🧐",
        "حەمە خەریکی جێبەجێکردنی پرۆژەیە، بێزاری مەکە! 💻",
    ]
    await message.channel.send(random.choice(responses))
    return

  elif "سڵاو" in msg:
    greetings = [
      f"سڵاو لە تۆش {message.author.mention}! بەخێر بێیت 🌸",
      f"سڵاو {message.author.mention}، چی هەیە چی نییە؟ 😂",
      f"ئۆهۆ سڵاو لە {message.author.mention}، فەرموو دانیشە!",
    ]
    await message.channel.send(random.choice(greetings))
    return

  elif "چۆنی" in msg or "چۆنیت" in msg:
    how_are_you = [
        "سپاس بۆ خوا، ئەگەر خەڵک تاگم نەەن هێشتا باشم! 🗿",
        "چاکم، بەس کۆمپیوتەرەکە کەمێک گەرم بووە! 🔥",
        "وەڵا وەک هەمیشە خەریکی ڕێکخستنی سێرڤەرم، تۆ چۆنیت؟ 🤓",
    ]
    await message.channel.send(random.choice(how_are_you))
    return

  await bot.process_commands(message)


# -------------------- فەرمانەکان --------------------
@bot.command(name="شیر_ڕێ")
async def coin_flip(ctx):
  outcomes = ["🦁 شیر", "☀️ ڕێ (خورشید)"]
  result = random.choice(outcomes)
  embed = discord.Embed(title="🎲 یاری شیر و ڕێ", color=discord.Color.gold())
  embed.add_field(name="ئەنجام:", value=f"**{result}**", inline=False)
  await ctx.send(embed=embed)


@bot.command(name="بەخت")
async def luck(ctx):
  percentage = random.randint(0, 100)
  embed = discord.Embed(
      title="🔮 ڕێژەی بەختی ئەمڕۆت", color=discord.Color.purple()
  )
  embed.add_field(
      name=f"{ctx.author.name}",
      value=f"بەختت ئۆتۆماتیکی پشکنرا: **%{percentage}** 🎯",
      inline=False,
  )
  await ctx.send(embed=embed)


@bot.command(name="میم")
async def meme(ctx):
  memes = [
      "کاتێک لە تاقیکردنەوە هیچی نا زانیت و سەیرێکی هاوڕێکەت دەکەیت 😂",
      "مامۆستا: ئەرکی ماڵەوەتان کردووە؟\nمن: ئینتەرنێت پچڕابوو مامۆستا! 💀",
      "شێوازی من کاتێک بە دایکم دەڵێم پارەم پێ نییە 🥺",
      "کەسێک لە چات ٥٠ پەیام دەنێرێت\nمن: ئەرێ دە بوەستە تایپەکەت سووتا! ⌨️🔥",
  ]
  embed = discord.Embed(
      title="🤣 میمی کوردی",
      description=random.choice(memes),
      color=discord.Color.green(),
  )
  await ctx.send(embed=embed)


@bot.command(name="یارمەتی")
async def help_command(ctx):
  embed = discord.Embed(
      title="📜 لیستی فەرمانەکانی بۆت", color=discord.Color.blue()
  )
  embed.add_field(name="!شیر_ڕێ", value="یاری کردنی شیر و ڕێ", inline=False)
  embed.add_field(
      name="!بەخت", value="دیاریکردنی ڕێژەی بەختی ئەمڕۆت", inline=False
  )
  embed.add_field(
      name="!میم", value="پێشبینیکردنی میم و قسەی خۆش", inline=False
  )
  embed.add_field(
      name="تاگ یان ڕیپلەی (Reply)",
      value="بۆتەکە تاگ بکە تا وەڵامی کۆمیدیت بداتەوە",
      inline=False,
  )
  await ctx.send(embed=embed)


bot.run("MTU0NTYxOTY3NjczNzA1MjcwMg.GywVm2.3RBAFUkkpftTwiG9mThpvcx4-ndFgO6hTFhoDk")

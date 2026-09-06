import discord
from discord.ext import commands
import random
import time
from groq import Groq

# -------------------- ڕێکخستنی AI (Groq - Llama 3.3) --------------------
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_INSTRUCTION = """
تۆ بۆتێکی زۆر زیرەک، کۆمیدی، کەمێک سارد و بەزمیت لە سێرڤەری Velvet City بە ناوی Velvet Bot.
ڕێنمایی زۆر گرنگ بۆ وەڵامدانەوە:
1. بە تەواوی لە کوردیی سۆرانی چات و ئاخاوتنی زارەکی تێبگە.
2. بەپێی دەق و واتا ڕاستەقینەکەی بەکارهێنەر وەڵام بدەرەوە، ڕاستەوخۆ وەڵامی قسەکەی بدەرەوە!
3. ئەگەر کەسێک هەڕەشەی کرد یان وتی "لێت دەدم"، بە ساردی و تەشقەڵەوە وەڵامی بدەرەوە (نموونە: "کێ؟ تۆ؟ ئارام ببەرەوە دکتۆر! 😂", "دە بڕۆ دانیشە بە لای خۆتەوە 🗿").
4. وەڵامەکانت کورت بن (1 بۆ 2 ڕستە بەسە).
5. ئیمۆجی بەکاربهێنە (😂, 💀, 🤫, 🤓, 🗿).
"""

def get_ai_response(prompt_text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=150
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "لە ئێستادا سیستەمەکە داواکارییەکانت وەرناگرێت، دووبارە تاقی بکەرەوە!"

# -----------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

user_message_count = {}
user_last_message_time = {}

@bot.event
async def on_ready():
    print(f'بۆتەکە ئۆنڵاین بوو وەکو: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!یارمەتی | Velvet Bot"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    current_time = time.time()

    if user_id not in user_last_message_time:
        user_last_message_time[user_id] = current_time
        user_message_count[user_id] = 1
    else:
        if current_time - user_last_message_time[user_id] < 15:
            user_message_count[user_id] += 1
        else:
            user_message_count[user_id] = 1
            user_last_message_time[user_id] = current_time

    if user_message_count[user_id] == 10:
        spam_responses = [
            f"وەی برایم {message.author.mention} هەندە زۆر مەڵێ تایپەکەت سووتا! 😂💀",
            f"ئەرێ {message.author.mention} نەفەسێک وەربگرە، کیبۆردەکەت هاواری لێهات! ⌨️🔥",
            f"{message.author.mention} هێواشتر، مێشکمان چوو وەڵا! 🤫💤"
        ]
        await message.channel.send(random.choice(spam_responses))
        user_message_count[user_id] = 0

    is_mentioned = bot.user.mentioned_in(message) and not message.mention_everyone
    is_reply_to_bot = False

    if message.reference and message.reference.message_id:
        try:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            if referenced_msg.author == bot.user:
                is_reply_to_bot = True
        except Exception:
            pass

    # ئەگەر تاگ یان ڕیپلەی بوو، وەڵامی AI دەداتەوە و دەستبەجێ بە return ڕادەوەستێت
    if is_mentioned or is_reply_to_bot:
        async with message.channel.typing():
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content:
                clean_content = "سڵاو"

            ai_text = get_ai_response(clean_content)
            await message.reply(ai_text)
        return

    msg = message.content.lower()

    if "حەمە" in msg:
        responses = [
            "گیانی حەمە، چی بڵێی؟ 😂",
            "وەڵا حەمە سەرقاڵە، پەیامەکەت بۆ جێبهێڵە!",
            "حەمە کوا لێرەیە؟ داوای چی ئەکەی؟ 🧐"
        ]
        await message.channel.send(random.choice(responses))
        return

    elif "سڵاو" in msg:
        await message.channel.send(f"سڵاو لە تۆش {message.author.mention}! بەخێر بێیت 🌸")
        return

    await bot.process_commands(message)

# فەرمانەکان
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
    embed = discord.Embed(title="🔮 ڕێژەی بەختی ئەمڕۆت", color=discord.Color.purple())
    embed.add_field(name=f"{ctx.author.name}", value=f"بەختت ئۆتۆماتیکی پشکنرا: **%{percentage}** 🎯", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="میم")
async def meme(ctx):
    memes = [
        "کاتێک لە تاقیکردنەوە هیچی نا زانیت و سەیرێکی هاوڕێکەت دەکەیت 😂",
        "مامۆستا: ئەرکی ماڵەوەتان کردووە؟\nمن: ئینتەرنێت پچڕابوو مامۆستا! 💀",
        "شێوازی من کاتێک بە دایکم دەڵێم پارەم پێ نییە 🥺"
    ]
    embed = discord.Embed(title="🤣 میمی کوردی", description=random.choice(memes), color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name="یارمەتی")
async def help_command(ctx):
    embed = discord.Embed(title="📜 لیستی فەرمانەکانی بۆت", color=discord.Color.blue())
    embed.add_field(name="!شیر_ڕێ", value="یاری کردنی شیر و ڕێ", inline=False)
    embed.add_field(name="!بەخت", value="دیاریکردنی ڕێژەی بەختی ئەمڕۆت", inline=False)
    embed.add_field(name="!میم", value="پێشبینیکردنی میم و قسەی خۆش", inline=False)
    embed.add_field(name="تاگ یان ڕیپلەی (Reply)", value="بۆتەکە تاگ بکە تا وەڵامی زیرەکت بداتەوە", inline=False)
    await ctx.send(embed=embed)

bot.run('MTU0NTYxOTY3NjczNzA1MjcwMg.G1PRM_.dQWOvrckzeAKLA62TqNPrZOdPCZVA6zkq76-UA')

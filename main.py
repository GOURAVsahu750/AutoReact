import subprocess, sys, time, random, threading
from datetime import datetime

# ---------- AUTO INSTALL ----------
def install(pkg):
    try:
        __import__(pkg if pkg != "pyTelegramBotAPI" else "telebot")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install("pyTelegramBotAPI")

# ---------- IMPORTS ----------
import telebot
from telebot import types
from telebot.types import ReactionTypeEmoji

# ---------- CONFIG ----------
MAIN_BOT_TOKEN = "8524165654:AAEzAoGynkcKJfHDHgFf35xZCoev95aI1jk"

OWNER_ID = 8453291493
OWNER_USERNAME = "g0ztg"

FORCE_JOIN = "@TITANXBOTMAKING"
FORCE_JOIN_LINK = "https://t.me/TITANXBOTMAKING"
UPDATE_CHANNEL = "https://t.me/TITANXBOTMAKING"
CREDIT = "@TITANXBOTMAKING"

REACTIONS = ["❤️", "🔥", "👍", "😍", "⚡"]
START_TIME = time.time()

USERS = set()
CLONES = []

# ---------- BOT ----------
bot = telebot.TeleBot(MAIN_BOT_TOKEN, threaded=True)

# ---------- HELPERS ----------
def uptime():
    s = int(time.time() - START_TIME)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def is_joined(uid):
    try:
        m = bot.get_chat_member(FORCE_JOIN, uid)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

def force_join(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 Join Channel", url=FORCE_JOIN_LINK))
    bot.send_message(
        chat_id,
        "🚫 *Pehle channel join karo*",
        parse_mode="Markdown",
        reply_markup=kb
    )

def buttons(bot_username, owner_username):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot_username}?startgroup=true"),
        types.InlineKeyboardButton("📢 Add to Channel", url=f"https://t.me/{bot_username}?startchannel=true")
    )
    kb.row(
        types.InlineKeyboardButton("🔔 Update Channel", url=UPDATE_CHANNEL),
        types.InlineKeyboardButton("👤 Owner", url=f"https://t.me/{owner_username}")
    )
    return kb

def react(b, chat_id, msg_id):
    try:
        b.set_message_reaction(
            chat_id,
            msg_id,
            [ReactionTypeEmoji(random.choice(REACTIONS))]
        )
    except:
        pass

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(m):
    if not is_joined(m.from_user.id):
        force_join(m.chat.id)
        return

    new = m.from_user.id not in USERS
    USERS.add(m.from_user.id)

    if new:
        bot.send_message(
            OWNER_ID,
            f"🆕 *New User Started Bot*\n\n"
            f"👤 Name: {m.from_user.first_name}\n"
            f"🆔 ID: `{m.from_user.id}`\n"
            f"🔗 @{m.from_user.username if m.from_user.username else 'NoUsername'}",
            parse_mode="Markdown"
        )

    me = bot.get_me().username
    bot.send_message(
        m.chat.id,
        f"🤖 *Auto Reaction Bot*\n\n"
        f"❤️ Single Reaction Mode\n"
        f"🧬 Clone System Enabled\n"
        f"⏱ Uptime: `{uptime()}`\n\n"
        f"🧪 `/clone BOT_TOKEN`",
        parse_mode="Markdown",
        reply_markup=buttons(me, OWNER_USERNAME)
    )

# ---------- STATS ----------
@bot.message_handler(commands=["stats"])
def stats(m):
    if m.from_user.id != OWNER_ID:
        return
    bot.reply_to(
        m,
        f"📊 *Bot Stats*\n\n"
        f"👥 Users: `{len(USERS)}`\n"
        f"🤖 Clones: `{len(CLONES)}`\n"
        f"⏱ Uptime: `{uptime()}`",
        parse_mode="Markdown"
    )

# ---------- BROADCAST ----------
@bot.message_handler(commands=["broadcast"])
def broadcast(m):
    if m.from_user.id != OWNER_ID:
        return
    try:
        msg = m.text.split(" ", 1)[1]
    except:
        bot.reply_to(m, "❌ Usage:\n/broadcast message")
        return

    sent = 0
    for uid in USERS:
        try:
            bot.send_message(uid, msg)
            sent += 1
        except:
            pass

    bot.reply_to(m, f"✅ Broadcast sent to `{sent}` users", parse_mode="Markdown")

# ---------- CLONE ----------
@bot.message_handler(commands=["clone"])
def clone(m):
    if not is_joined(m.from_user.id):
        force_join(m.chat.id)
        return

    if not m.from_user.username:
        bot.reply_to(m, "❌ Clone ke liye username zaroori hai")
        return

    try:
        token = m.text.split(" ", 1)[1].strip()
    except:
        bot.reply_to(m, "❌ Usage:\n/clone BOT_TOKEN")
        return

    try:
        cb = telebot.TeleBot(token, threaded=True)
        info = cb.get_me()
        CLONES.append(info.username)

        @cb.message_handler(commands=["start"])
        def cstart(x):
            cb.send_message(
                x.chat.id,
                f"🤖 *Auto Reaction Bot*\n\n"
                f"👤 Owner: @{m.from_user.username}\n"
                f"🔗 *This bot is cloned of* {CREDIT}",
                parse_mode="Markdown",
                reply_markup=buttons(info.username, m.from_user.username)
            )

        @cb.channel_post_handler(content_types=["text","photo","video","audio","document"])
        def ch(x):
            react(cb, x.chat.id, x.id)

        @cb.message_handler(content_types=["text","photo","video","audio","document"])
        def gr(x):
            if x.chat.type != "private":
                react(cb, x.chat.id, x.id)

        threading.Thread(
            target=lambda: cb.infinity_polling(skip_pending=True),
            daemon=True
        ).start()

        bot.reply_to(
            m,
            f"✅ *Clone Started Successfully*\n\n🤖 @{info.username}",
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.reply_to(m, f"❌ Invalid Bot Token\n`{e}`", parse_mode="Markdown")

# ---------- MAIN REACTIONS ----------
@bot.channel_post_handler(content_types=["text","photo","video","audio","document"])
def mch(m):
    react(bot, m.chat.id, m.id)

@bot.message_handler(content_types=["text","photo","video","audio","document"])
def mgr(m):
    if m.chat.type != "private":
        react(bot, m.chat.id, m.id)

# ---------- RUN ----------
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 BOT STARTED | OWNER: @g0ztg")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
bot.infinity_polling(timeout=10, long_polling_timeout=5)

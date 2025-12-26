import subprocess
import sys
import time
import random
import threading
from datetime import datetime

# ---------- AUTO INSTALL ----------
def install_package(pkg):
    try:
        __import__(pkg if pkg != "pyTelegramBotAPI" else "telebot")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_package("pyTelegramBotAPI")

# ---------- IMPORTS ----------
import telebot
from telebot import types
from telebot.types import ReactionTypeEmoji

# ---------- SETTINGS ----------
BOT_TOKEN = "8524165654:AAEzAoGynkcKJfHDHgFf35xZCoev95aI1jk"

OWNER_USERNAME = "@g0ztg"
OWNER_LINK = "https://t.me/g0ztg"
SUPPORT_CHANNEL_LINK = "https://t.me/TITANXBOTMAKING"

REACTION_LIST = [
    "👍", "🔥", "❤️", "😍", "🥰", "👏",
    "😁", "🤩", "⚡", "💯", "🎉"
]

START_TIME = time.time()

# ---------- BOT INIT ----------
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# ---------- HELPERS ----------
def get_uptime():
    s = int(time.time() - START_TIME)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def log(chat, count, ctype):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] ❤️ {count} reactions | {chat} ({ctype})")

# ---------- COMMANDS ----------
@bot.message_handler(commands=["start"])
def start_cmd(message):
    user = message.from_user.first_name
    bot_user = bot.get_me().username

    text = (
        f"⚡ *Hello {user}*\n\n"
        f"🤖 *Auto Reaction Bot*\n"
        f"━━━━━━━━━━━━━━\n"
        f"🟢 Status: Online\n"
        f"❤️ Reactions: Multi (+)\n"
        f"⏱ Uptime: {get_uptime()}\n"
        f"👑 Owner: {OWNER_USERNAME}\n"
        f"━━━━━━━━━━━━━━"
    )

    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton(
            "➕ Add to Group",
            url=f"https://t.me/{bot_user}?startgroup=true"
        ),
        types.InlineKeyboardButton(
            "📢 Add to Channel",
            url=f"https://t.me/{bot_user}?startchannel=true"
        )
    )
    kb.row(
        types.InlineKeyboardButton("💬 Support Channel", url=SUPPORT_CHANNEL_LINK),
        types.InlineKeyboardButton("👤 Owner", url=OWNER_LINK)
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=kb
    )

@bot.message_handler(commands=["status", "ping"])
def status_cmd(message):
    ping = int((time.time() - message.date) * 1000)
    if ping < 0:
        ping = 10

    bot.reply_to(
        message,
        f"📊 *Bot Status*\n\n"
        f"📶 Ping: `{ping}ms`\n"
        f"⏱ Uptime: `{get_uptime()}`\n"
        f"❤️ Reaction Mode: `Telegram Safe (3)`",
        parse_mode="Markdown"
    )

# ---------- ❤️ REACTION ENGINE ----------
def perform_reaction(chat_id, msg_id, title, ctype):
    try:
        time.sleep(1.5)

        emojis = random.sample(REACTION_LIST, 3)  # SAFE LIMIT

        bot.set_message_reaction(
            chat_id,
            msg_id,
            [ReactionTypeEmoji(e) for e in emojis]
        )

        log(title, len(emojis), ctype)

    except Exception as e:
        print("❌ Reaction error:", e)

# ---------- LISTENERS ----------
@bot.channel_post_handler(
    content_types=["text", "photo", "video", "audio", "document", "voice"]
)
def channel_post(message):
    threading.Thread(
        target=perform_reaction,
        args=(message.chat.id, message.id, message.chat.title, "Channel")
    ).start()

@bot.message_handler(
    content_types=["text", "photo", "video", "audio", "document", "voice"]
)
def group_message(message):
    if message.chat.type == "private":
        return

    threading.Thread(
        target=perform_reaction,
        args=(message.chat.id, message.id, message.chat.title, "Group")
    ).start()

# ---------- START ----------
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 AUTO REACTION BOT STARTED")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

bot.infinity_polling(timeout=10, long_polling_timeout=5)

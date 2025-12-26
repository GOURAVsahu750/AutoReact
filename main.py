import subprocess
import sys
import time
import random
import threading
from datetime import datetime

# ---------- 🔄 AUTO INSTALL ----------
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

# ---------- ⚙️ SETTINGS ----------
BOT_TOKEN = "8524165654:AAEzAoGynkcKJfHDHgFf35xZCoev95aI1jk"

OWNER_USERNAME = "@g0ztg"
SUPPORT_CHANNEL_LINK = "https://t.me/TITANXBOTMAKING"
OWNER_LINK = "https://t.me/g0ztg"

REACTION_LIST = [
    "👍", "🔥", "❤️", "😍", "🥰", "👏", "😁",
    "🤩", "⚡", "💯", "🎉", "😎", "🚀", "🙌"
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

# ---------- COMMANDS ----------
@bot.message_handler(commands=["start"])
def start_cmd(message):
    bot.send_message(
        message.chat.id,
        f"🤖 *Auto Reaction Bot*\n\n"
        f"🔥 Multi-Reaction Mode\n"
        f"❤️ Reactions: Telegram Allowed\n"
        f"⏱ Uptime: {get_uptime()}\n"
        f"👑 Owner: {OWNER_USERNAME}",
        parse_mode="Markdown"
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
        f"❤️ Reaction Mode: `3 emojis (Telegram limit)`",
        parse_mode="Markdown"
    )

# ---------- ❤️ REACTION ENGINE ----------
def perform_reaction(chat_id, msg_id, title, ctype):
    try:
        time.sleep(1)

        # 🔒 Telegram-safe reaction count
        emojis = random.sample(REACTION_LIST, 3)

        bot.set_message_reaction(
            chat_id,
            msg_id,
            [ReactionTypeEmoji(e) for e in emojis]
        )

        t = datetime.now().strftime("%H:%M:%S")
        print(f"[{t}] ✅ {len(emojis)} reactions | {title} ({ctype})")

    except Exception as e:
        print("❌ Reaction error:", e)

# ---------- LISTENERS ----------
@bot.channel_post_handler(content_types=["text", "photo", "video", "audio", "document", "voice"])
def channel_post(message):
    threading.Thread(
        target=perform_reaction,
        args=(message.chat.id, message.id, message.chat.title, "Channel")
    ).start()

@bot.message_handler(content_types=["text", "photo", "video", "audio", "document", "voice"])
def group_msg(message):
    if message.chat.type == "private":
        return

    threading.Thread(
        target=perform_reaction,
        args=(message.chat.id, message.id, message.chat.title, "Group")
    ).start()

# ---------- START ----------
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 AUTO MULTI-REACTION BOT STARTED")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

bot.infinity_polling(timeout=10, long_polling_timeout=5)

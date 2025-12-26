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
MAIN_BOT_TOKEN = "8524165654:AAEzAoGynkcKJfHDHgFf35xZCoev95aI1jk"

FORCE_JOIN_CHANNEL = "@TITANXBOTMAKING"
FORCE_JOIN_LINK = "https://t.me/TITANXBOTMAKING"
CLONE_CREDIT = "@TITANXBOTMAKING"

REACTION_LIST = ["❤️", "🔥", "👍", "😍", "⚡"]
START_TIME = time.time()

# ---------- BOT ----------
main_bot = telebot.TeleBot(MAIN_BOT_TOKEN, threaded=True)

# ---------- HELPERS ----------
def get_uptime():
    s = int(time.time() - START_TIME)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

def single_react(bot, chat_id, msg_id):
    try:
        bot.set_message_reaction(
            chat_id,
            msg_id,
            [ReactionTypeEmoji(random.choice(REACTION_LIST))]
        )
    except:
        pass

def is_joined(user_id):
    try:
        member = main_bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def force_join_msg(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 Join Channel", url=FORCE_JOIN_LINK))
    main_bot.send_message(
        chat_id,
        "🚫 *Access Denied*\n\n"
        "Bot use karne ke liye pehle channel join karo 👇",
        parse_mode="Markdown",
        reply_markup=kb
    )

def build_buttons(bot_username, owner_username, channel_link):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot_username}?startgroup=true"),
        types.InlineKeyboardButton("📢 Channel", url=channel_link)
    )
    kb.row(
        types.InlineKeyboardButton("👤 Owner", url=f"https://t.me/{owner_username}")
    )
    return kb

# ---------- MAIN /START ----------
@main_bot.message_handler(commands=["start"])
def start_cmd(message):
    if not is_joined(message.from_user.id):
        force_join_msg(message.chat.id)
        return

    bot_user = main_bot.get_me().username
    text = (
        f"🤖 *Auto Reaction Bot*\n\n"
        f"❤️ Single Reaction Mode\n"
        f"🧬 Clone System Enabled\n"
        f"⏱ Uptime: {get_uptime()}\n\n"
        f"🧪 `/clone BOT_TOKEN`"
    )

    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot_user}?startgroup=true"),
        types.InlineKeyboardButton("📢 Channel", url=FORCE_JOIN_LINK)
    )

    main_bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=kb
    )

# ---------- CLONE COMMAND ----------
@main_bot.message_handler(commands=["clone"])
def clone_cmd(message):
    if not is_joined(message.from_user.id):
        force_join_msg(message.chat.id)
        return

    if not message.from_user.username:
        main_bot.reply_to(message, "❌ Clone ke liye username zaroori hai")
        return

    try:
        token = message.text.split(" ", 1)[1].strip()
    except:
        main_bot.reply_to(message, "❌ Usage:\n/clone BOT_TOKEN")
        return

    cloner_username = message.from_user.username
    cloner_profile = f"https://t.me/{cloner_username}"

    try:
        clone_bot = telebot.TeleBot(token, threaded=True)
        info = clone_bot.get_me()
        clone_username = info.username

        # ----- CLONE /START -----
        @clone_bot.message_handler(commands=["start"])
        def clone_start(msg):
            text = (
                f"🤖 *Auto Reaction Bot*\n\n"
                f"❤️ Single Reaction Mode\n"
                f"⏱ Uptime: {get_uptime()}\n\n"
                f"👤 Owner: @{cloner_username}\n"
                f"🔗 *This bot is cloned of* {CLONE_CREDIT}"
            )
            clone_bot.send_message(
                msg.chat.id,
                text,
                parse_mode="Markdown",
                reply_markup=build_buttons(
                    clone_username,
                    cloner_username,
                    cloner_profile
                )
            )

        # ----- CLONE LISTENERS -----
        @clone_bot.channel_post_handler(content_types=["text", "photo", "video", "audio", "document"])
        def clone_channel(msg):
            single_react(clone_bot, msg.chat.id, msg.id)

        @clone_bot.message_handler(content_types=["text", "photo", "video", "audio", "document"])
        def clone_group(msg):
            if msg.chat.type != "private":
                single_react(clone_bot, msg.chat.id, msg.id)

        threading.Thread(
            target=lambda: clone_bot.infinity_polling(skip_pending=True),
            daemon=True
        ).start()

        main_bot.reply_to(
            message,
            f"✅ *Clone Bot Started!*\n\n"
            f"🤖 @{clone_username}\n"
            f"👤 Owner: @{cloner_username}",
            parse_mode="Markdown"
        )

    except Exception as e:
        main_bot.reply_to(message, f"❌ Invalid Bot Token\n{e}")

# ---------- MAIN BOT REACTION ----------
@main_bot.channel_post_handler(content_types=["text", "photo", "video", "audio", "document"])
def main_channel(msg):
    single_react(main_bot, msg.chat.id, msg.id)

@main_bot.message_handler(content_types=["text", "photo", "video", "audio", "document"])
def main_group(msg):
    if msg.chat.type != "private":
        single_react(main_bot, msg.chat.id, msg.id)

# ---------- START ----------
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 MAIN + CLONE BOT WITH FORCE JOIN RUNNING")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

main_bot.infinity_polling(timeout=10, long_polling_timeout=5)

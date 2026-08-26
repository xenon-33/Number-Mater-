# -*- coding: utf-8 -*-
"""
Bot Name: Vish - Smart Bot (20 Borders)
Owner: @Xenon33cyber
"""

import sqlite3
import random
import string
import aiohttp
import json
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# 🔥 Owner's token – do not change
BOT_TOKEN = "8716988605:AAF9YS520zb6x1k9ulhiBq_Lh-mhWB65paU"
SUPER_ADMIN_ID = 6303062255
API_URL = "https://adityaapi.onrender.com/api/v1/info?key=Rahul&query="
AUTO_DELETE_TIME = 5
RESULT_DELETE_TIME = 300  # 5 minutes
MAX_RESULTS = 20
# ============================================================

# ======================== 20 HEADERS =========================
HEADERS = [
    "💀 [OWNER] :: @Xenon33cyber",
    "🔥 [XENON] :: TERMINAL_ACTIVE",
    "⚡ [HACKER] :: SYSTEM_ONLINE",
    "🖥️ [ROOT] :: ACCESS_GRANTED",
    "🐉 [DANAV] :: DARK_MODE",
    "🔮 [OSINT] :: SCANNING",
    "💀 [GHOST] :: MODE_ACTIVE",
    "🔥 [CYBER] :: NINJA_MODE",
    "⚡ [NEO] :: MATRIX_LOADED",
    "🖥️ [ZERO] :: CODENAME_X",
    "🐉 [DRAGON] :: FIRE_BREATH",
    "🔮 [WIZARD] :: SPELL_CAST",
    "💀 [REAPER] :: SOUL_HARVEST",
    "🔥 [PHOENIX] :: REBORN",
    "⚡ [THUNDER] :: STORM_ACTIVE",
    "🖥️ [GHOST] :: STEALTH_MODE",
    "🐉 [VIPER] :: VENOM_ACTIVE",
    "🔮 [SHADOW] :: DARKNESS",
    "💀 [NIGHTMARE] :: FEAR_MODE",
    "🔥 [BLAZE] :: INFERNO_ACTIVE",
]

FOOTERS = [
    "💳 Credits? Talk to Owner – solid deal! 😎",
    "🔥 Keep grinding, bro!",
    "💀 Owner is watching...",
    "🖤 Stay dangerous.",
    "⚡ Power to the Hacker.",
    "🔮 Data is power.",
    "💀 Death to bots, life to hackers.",
    "🔥 Hack the planet.",
    "🖥️ Code is law.",
    "🐉 Rise of the machines.",
]

def random_header():
    return random.choice(HEADERS)

def random_footer():
    return random.choice(FOOTERS)

def line_20():
    return "═" * 20

def format_hacker(msg):
    header = random_header()
    footer = random_footer()
    return f"{header}\n{line_20()}\n{msg}\n{line_20()}\n{footer}"

# ======================== Database ===========================
DB_FILE = "NumberOsint33_bot.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    credits INTEGER DEFAULT 20,
    referral_code TEXT UNIQUE,
    referred_by INTEGER DEFAULT 0,
    total_searches INTEGER DEFAULT 0,
    is_admin INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS credit_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    status TEXT DEFAULT 'pending'
)''')

c.execute("INSERT OR IGNORE INTO users (user_id, credits, referral_code, is_admin) VALUES (?, 999999, ?, 1)",
          (SUPER_ADMIN_ID, ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))))
conn.commit()

def get_user(user_id):
    try:
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if not user:
            ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            c.execute("INSERT INTO users (user_id, credits, referral_code) VALUES (?, ?, ?)", (user_id, 20, ref_code))
            conn.commit()
            return (user_id, 20, ref_code, 0, 0, 0)
        return user
    except:
        return (user_id, 20, '', 0, 0, 0)

def is_admin(user_id):
    user = get_user(user_id)
    return user[5] == 1

# ======================== CONSTANTS =================
OWNER_LINK = "<a href='https://t.me/Xenon33cyber'>@Xenon33cyber</a>"
UPDATE_LINK = "<a href='https://t.me/Xenoncyber33'>@Xenoncyber33</a>"
SUPPORT_LINK = "<a href='https://t.me/xenondaemon_Team'>@xenondaemon_Team</a>"

# ======================== BOXES (20 Borders) =================
FETCHING_BOX = (
    "╔══『 ⚡ 𝑭𝑬𝑻𝑪𝑯𝑰𝑵𝑮 』══╗\n\n"
    "🔍 𝑭𝒆𝒕𝒄𝒉𝒊𝒏𝒈 𝑫𝒂𝒕𝒂...\n"
    "⏳ 𝑷𝒍𝒆𝒂𝒔𝒆 𝑾𝒂𝒊𝒕 ~1 𝑺𝒆𝒄\n\n"
    "╚════════════════╝"
)

NO_DATA_BOX = (
    "╔══『 ❌ 𝑵𝑶 𝑫𝑨𝑻𝑨 』══╗\n\n"
    "🚫 𝑵𝒐 𝑹𝒆𝒔𝒖𝒍𝒕 𝑭𝒐𝒖𝒏𝒅\n"
    "💎 𝑵𝒐 𝑪𝒓𝒆𝒅𝒊𝒕 𝑪𝒖𝒕\n\n"
    "╚════════════════╝"
)

def welcome_box(admin, credits):
    return (
        f"╔═══『 💀 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 』═══╗\n\n"
        f"👋 𝑾𝒉𝒂𝒕'𝒔 𝒖𝒑, 𝒃𝒓𝒐! {admin}\n"
        f"🧑‍💻 𝑰'𝒎 𝑿𝒆𝒏𝒐𝒏 – 𝑻𝒉𝒆 𝑯𝒂𝒄𝒌𝒆𝒓 𝑴𝒂𝒄𝒉𝒊𝒏𝒆\n"
        f"💻 𝑪𝒓𝒆𝒅𝒊𝒕𝒔: {credits} (20 𝒅𝒆𝒎𝒐)\n"
        f"⚡ 𝑪𝒐𝒎𝒎𝒂𝒏𝒅: /𝒔𝒆𝒂𝒓𝒄𝒉 &𝒍𝒕;𝒏𝒖𝒎𝒃𝒆𝒓&gt;\n"
        f"🔐 𝑪𝒐𝒔𝒕: 10 𝒄𝒓𝒆𝒅𝒊𝒕𝒔 𝒑𝒆𝒓 𝒔𝒆𝒂𝒓𝒄𝒉\n"
        f"📢 𝑼𝒑𝒅𝒂𝒕𝒆𝒔: {UPDATE_LINK} | {SUPPORT_LINK}\n\n"
        f"╚{line_20()}╝"
    )

HELP_BOX = (
    "╔══『 🗣️ 𝑯𝑬𝑳𝑷 』══╗\n\n"
    f"👤 𝑶𝒘𝒏𝒆𝒓: {OWNER_LINK}\n"
    f"📢 𝑼𝒑𝒅𝒂𝒕𝒆𝒔: {UPDATE_LINK}\n"
    f"🛠️ 𝑺𝒖𝒑𝒑𝒐𝒓𝒕: {SUPPORT_LINK}\n\n"
    "🔹 𝑶𝒏𝒍𝒚 𝑫𝑴 𝒕𝒉𝒆 𝑶𝒘𝒏𝒆𝒓 𝒊𝒇 𝒎𝒐𝒏𝒆𝒚 𝒊𝒔 𝒅𝒆𝒅𝒖𝒄𝒕𝒆𝒅\n"
    "🔹 𝑵𝒐 '𝒈𝒊𝒗𝒆 𝒅𝒆𝒎𝒐', '𝒇𝒓𝒆𝒆', '𝒕𝒓𝒚 1 𝒓𝒖𝒑𝒆𝒆'\n\n"
    "💰 𝑷𝒍𝒂𝒏𝒔 (𝑪𝒉𝒆𝒂𝒑 & 𝑭𝒖𝒍𝒍 𝑽𝒂𝒍𝒖𝒆)\n\n"
    "🟢 ₹49 – 𝑴𝒊𝒄𝒓𝒐 (90 𝑪𝒓𝒆𝒅𝒊𝒕𝒔)\n"
    "🟡 ₹79 – 𝑺𝒕𝒂𝒓𝒕𝒆𝒓 (160 𝑪𝒓𝒆𝒅𝒊𝒕𝒔)\n"
    "🔴 ₹99 – 𝑩𝒆𝒔𝒕 𝑺𝒆𝒍𝒍𝒆𝒓 (210 𝑪𝒓𝒆𝒅𝒊𝒕𝒔)\n\n"
    "👇 𝑼𝒔𝒆:\n"
    "/𝒑𝒂𝒚49\n/𝒑𝒂𝒚79\n/𝒑𝒂𝒚99\n\n"
    "💀 𝑶𝒘𝒏𝒆𝒓'𝒔 𝒐𝒂𝒕𝒉: 𝑷𝒂𝒚 𝒂𝒏𝒅 𝒄𝒓𝒆𝒅𝒊𝒕𝒔 𝒂𝒅𝒅𝒆𝒅.\n\n"
    "╚════════════════╝"
)

def balance_box(credits):
    return (
        f"╔══『 💰 𝑩𝑨𝑳𝑨𝑵𝑪𝑬 』══╗\n\n"
        f"💳 𝑹𝒆𝒎𝒂𝒊𝒏𝒊𝒏𝒈 𝑪𝒓𝒆𝒅𝒊𝒕𝒔: {credits}\n\n"
        f"╚════════════════╝"
    )

def error_box(error):
    return (
        f"╔══『 ❌ 𝑬𝑹𝑹𝑶𝑹 』══╗\n\n"
        f"🚫 {error}\n\n"
        f"╚════════════════╝"
    )

def success_box(msg):
    return (
        f"╔══『 ✅ 𝑺𝑼𝑪𝑪𝑬𝑺𝑺 』══╗\n\n"
        f"{msg}\n\n"
        f"╚════════════════╝"
    )

def info_box(title, content):
    border = "═" * 20
    return f"╔═══『 {title} 』═══╗\n\n{content}\n\n╚{border}╝"

CREDITS_GUIDE_BOX = (
    "╔══『 💳 𝑪𝑹𝑬𝑫𝑰𝑻𝑺 𝑮𝑼𝑰𝑫𝑬 』══╗\n\n"
    "🔹 /𝒈𝒊𝒗𝒆𝒂𝒍𝒍 &𝒍𝒕;𝒂𝒎𝒐𝒖𝒏𝒕&gt;\n"
    "🔹 /𝒂𝒅𝒅𝒄𝒓𝒆𝒅𝒊𝒕𝒔 &𝒍𝒕;𝒊𝒅&gt; &𝒍𝒕;𝒂𝒎𝒐𝒖𝒏𝒕&gt;\n\n"
    "📌 𝑬𝒙𝒂𝒎𝒑𝒍𝒆𝒔:\n"
    "/𝒈𝒊𝒗𝒆𝒂𝒍𝒍 5\n"
    "/𝒂𝒅𝒅𝒄𝒓𝒆𝒅𝒊𝒕𝒔 123456789 10\n\n"
    "╚════════════════╝"
)

PAYMENT_BOX = (
    "╔═══『 💳 𝑷𝑨𝒀𝑴𝑬𝑵𝑻 』═══╗\n\n"
    f"💳 𝑫𝑴 𝒇𝒐𝒓 𝒑𝒂𝒚𝒎𝒆𝒏𝒕:\n"
    f"{OWNER_LINK}\n\n"
    "⚠️ 𝑨𝒇𝒕𝒆𝒓 𝒕𝒓𝒂𝒏𝒔𝒂𝒄𝒕𝒊𝒐𝒏, 𝒔𝒆𝒏𝒅\n"
    "𝒔𝒄𝒓𝒆𝒆𝒏𝒔𝒉𝒐𝒕 + 𝒀𝒐𝒖𝒓 𝑼𝒔𝒆𝒓 𝑰𝑫.\n\n"
    "╚════════════════╝"
)

def request_box(content):
    return f"╔══『 📩 𝑹𝑬𝑸𝑼𝑬𝑺𝑻 』══╗\n\n{content}\n\n╚════════════════╝"

def admin_panel_box(content):
    return f"╔═══『 👑 𝑨𝑫𝑴𝑰𝑵 𝑷𝑨𝑵𝑬𝑳 』═══╗\n\n{content}\n\n╚═══════════╝"

NUMBER_ENTRY_BOX = (
    "╔══『 🔢 𝑬𝑵𝑻𝑬𝑹 𝑵𝑼𝑴𝑩𝑬𝑹 』══╗\n\n"
    "📱 𝑷𝒍𝒆𝒂𝒔𝒆 𝒆𝒏𝒕𝒆𝒓 𝒕𝒉𝒆 𝒏𝒖𝒎𝒃𝒆𝒓\n"
    "🔹 𝑭𝒐𝒓𝒎𝒂𝒕: 9876543210\n"
    "🔹 (𝑾𝒊𝒕𝒉𝒐𝒖𝒕 +91)\n\n"
    "╚════════════════╝"
)

def fancy_box(title, content):
    border = "═" * 20
    return f"╔═══『 {title} 』═══╗\n\n{content}\n\n╚{border}╝"

# ======================== Keyboard ===========================
def get_main_keyboard(user_id):
    admin = is_admin(user_id)
    keyboard = []
    keyboard.append([KeyboardButton("🔍 Search"), KeyboardButton("💰 Balance")])
    keyboard.append([KeyboardButton("🆘 Help")])

    if admin:
        keyboard.append([KeyboardButton("📨 Request Credits"), KeyboardButton("👑 Admin Panel")])
    else:
        keyboard.append([KeyboardButton("📨 Request Credits")])

    if admin:
        keyboard.append([KeyboardButton("➕ Add Admin"), KeyboardButton("🔄 Switch User"), KeyboardButton("➕ Add Credits")])
        keyboard.append([KeyboardButton("➖ Remove Credits"), KeyboardButton("📢 Broadcast"), KeyboardButton("✅ Approve"), KeyboardButton("❌ Reject")])
        keyboard.append([KeyboardButton("💳 Credits Guide")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

# ======================== API Call ===========================
async def fetch_number_info(number):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL + number, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and data.get('results') and len(data.get('results', [])) > 0:
                        return data
                    else:
                        return {"error": "no_data"}
                else:
                    return {"error": f"API server busy (HTTP {resp.status}), try again in a minute."}
        except aiohttp.ClientConnectorError:
            return {"error": "Network error – check your internet, dude!"}
        except aiohttp.ClientResponseError as e:
            return {"error": f"API error: {str(e)}"}
        except asyncio.TimeoutError:
            return {"error": "Timeout – server is sleepy, try again."}
        except Exception as e:
            return {"error": f"Something went wrong: {str(e)}"}

# ======================== AUTO DELETE HELPER =================
async def auto_delete_message(context, chat_id, message_id, delay=AUTO_DELETE_TIME):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass

# ======================== Handlers ===========================

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = await update.message.reply_text(format_hacker(HELP_BOX), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
    # PERMANENT - only user's message deletes
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

async def pay_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(format_hacker(PAYMENT_BOX), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    # PERMANENT
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    first_name = update.effective_user.first_name or "Bro"
    username = update.effective_user.username
    user_display = f"@{username}" if username else first_name
    admin_tag = "👑 Admin Sahab" if user[5] == 1 else user_display
    
    msg = format_hacker(welcome_box(admin_tag, user[1]))

    try:
        photo_msg = await update.message.reply_photo(
            photo="https://i.postimg.cc/ZYyRDgLs/file-00000000150881faadd26581a4e1144d.png",
            caption=msg,
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )
        # PERMANENT - only user's message deletes
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    except Exception:
        text_msg = await update.message.reply_text(msg, parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

# ======================== Button Handlers =====================
async def button_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(format_hacker(NUMBER_ENTRY_BOX), parse_mode='HTML')
    # Number entry box - delete after 10 seconds
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=10))
    # User's button message - delete after 3 seconds
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    context.user_data['action'] = 'waiting_search'

async def button_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    msg = await update.message.reply_text(
        format_hacker(balance_box(user[1])),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(update.effective_user.id)
    )
    # PERMANENT
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

async def button_request_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(
        format_hacker(fancy_box("📨 REQUEST CREDITS", "𝑯𝒐𝒘 𝒎𝒂𝒏𝒚 𝒄𝒓𝒆𝒅𝒊𝒕𝒔?\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 20")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_request_credits'

async def button_give_credits_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 That's admin work, bro!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(format_hacker(CREDITS_GUIDE_BOX), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    # PERMANENT
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

# Admin Buttons
async def button_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("➕ ADD ADMIN", "𝑮𝒊𝒗𝒆 𝑼𝒔𝒆𝒓 𝑰𝑫\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_add_admin'

async def button_switch_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("🔄 SWITCH USER", "𝑮𝒊𝒗𝒆 𝑼𝒔𝒆𝒓 𝑰𝑫\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_switch_user'

async def button_add_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("➕ ADD CREDITS", "𝑮𝒊𝒗𝒆 𝑰𝑫 𝒂𝒏𝒅 𝑨𝒎𝒐𝒖𝒏𝒕\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321 50")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_add_credits'

async def button_remove_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("➖ REMOVE CREDITS", "𝑮𝒊𝒗𝒆 𝑰𝑫 𝒂𝒏𝒅 𝑨𝒎𝒐𝒖𝒏𝒕\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321 20")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_remove_credits'

async def button_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("📢 BROADCAST", "𝑻𝒚𝒑𝒆 𝒚𝒐𝒖𝒓 𝒎𝒆𝒔𝒔𝒂𝒈𝒆")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_broadcast'

async def button_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("✅ APPROVE", "𝑮𝒊𝒗𝒆 𝑰𝑫 𝒂𝒏𝒅 𝑨𝒎𝒐𝒖𝒏𝒕\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321 20")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_approve'

async def button_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg = await update.message.reply_text(
        format_hacker(fancy_box("❌ REJECT", "𝑮𝒊𝒗𝒆 𝑰𝑫\n> 𝑬𝒙𝒂𝒎𝒑𝒍𝒆: 987654321")),
        parse_mode='HTML'
    )
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    context.user_data['action'] = 'waiting_reject'

# ======================== Text Handler ===================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    action = context.user_data.get('action')

    # Delete user's number message after 3 seconds
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))

    if text.lower() in ["help", "🆘 help"]:
        await help_handler(update, context)
        return

    if action == 'waiting_search':
        number = text.replace(" ", "").strip()
        if not number.isdigit():
            msg = await update.message.reply_text(format_hacker(error_box("❌ Digits only! Example: 9876543210")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        context.user_data['action'] = None
        user = get_user(user_id)
        if user[1] < 10:
            msg = await update.message.reply_text(format_hacker(error_box("🚫 Credits over! /request_credits 10")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return

        new_bal = user[1] - 10
        c.execute("UPDATE users SET credits = ?, total_searches = total_searches + 1 WHERE user_id=?", (new_bal, user_id))
        conn.commit()

        searching_msg = await update.message.reply_text(format_hacker(FETCHING_BOX), parse_mode='HTML')
        # FETCHING_BOX - delete after 3 seconds
        asyncio.create_task(auto_delete_message(context, searching_msg.chat_id, searching_msg.message_id, delay=3))

        full_response = await fetch_number_info(number)

        if not full_response or "error" in full_response:
            error_msg = full_response.get('error', 'Something went wrong!')
            if error_msg == "no_data":
                msg = await update.message.reply_text(format_hacker(NO_DATA_BOX), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
                asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
                return
            else:
                msg = await update.message.reply_text(format_hacker(error_box(f"❌ {error_msg}")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
                asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
                return

        results = full_response.get('results', [])
        if not results:
            msg = await update.message.reply_text(format_hacker(NO_DATA_BOX), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return

        # ========== CLEAN RESULT BOX ==========
        box_content = f"📞 Number: <code>{number}</code>\n💰 Remaining: {new_bal}\n\n"

        for i, res in enumerate(results[:20], 1):
            name = res.get('name', 'N/A')
            fname = res.get('fname', 'N/A')
            mobile = res.get('mobile', 'N/A')
            email = res.get('email', 'N/A')
            address = res.get('address', 'N/A')
            circle = res.get('circle', 'N/A')
            alt = res.get('alt', 'N/A')
            id_field = res.get('id', 'N/A')
            
            box_content += (
                f"╔════════Result {i}═════╗\n"
                f"🧑‍💼 Name: {name}\n"
                f"🧑‍🧑‍🧒‍🧒 Father: {fname}\n"
                f"📱 Mobile: {mobile}\n"
                f"📧 Email: {email}\n"
                f"🏠 Address: {address}\n"
                f"📡 Circle: {circle}\n"
                f"📱 Alt: {alt}\n"
                f"🪪 ID: {id_field}\n"
                f"╚═══════════════════╝\n"
            )

        if len(results) > 20:
            box_content += f"\n⚠️ Showing first 20, search more for the rest."

        box_content = box_content.rstrip('\n')
        parsed_msg = info_box("📝 Result", box_content)
        final_msg = format_hacker(parsed_msg)

        # RESULT - DELETE AFTER 5 MINUTES (300 seconds)
        result_msg = await update.message.reply_text(final_msg, parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, result_msg.chat_id, result_msg.message_id, delay=300))

    elif action == 'waiting_request_credits':
        try:
            amount = int(text)
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Enter a valid number!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("INSERT INTO credit_requests (user_id, amount) VALUES (?, ?)", (user_id, amount))
        conn.commit()
        
        username = update.effective_user.username or "NoUsername"
        user_link = f"<a href='tg://user?id={user_id}'>@{username}</a>"
        admin_msg = (
            f"📩 Credit Request\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 User: {user_link}\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"💰 Requested: {amount} credits\n"
            f"⏰ Time: {datetime.now().strftime('%I:%M %p')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Use: <code>/addcredits {user_id} {amount}</code>"
        )
        admins = c.execute("SELECT user_id FROM users WHERE is_admin=1").fetchall()
        for admin in admins:
            try:
                admin_msg_sent = await context.bot.send_message(admin[0], format_hacker(request_box(admin_msg)), parse_mode='HTML')
                asyncio.create_task(auto_delete_message(context, admin_msg_sent.chat_id, admin_msg_sent.message_id, delay=30))
            except:
                pass
        msg = await update.message.reply_text(format_hacker(success_box("✅ Request sent, bro!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        context.user_data['action'] = None

    elif action == 'waiting_add_admin':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give a valid ID!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE users SET is_admin = 1 WHERE user_id=?", (target,))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> is now admin!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        context.user_data['action'] = None

    elif action == 'waiting_switch_user':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give a valid ID!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE users SET credits = 999999 WHERE user_id=?", (target,))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> got unlimited credits!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        context.user_data['action'] = None

    elif action == 'waiting_add_credits':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Format: ID amount")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> got +{amount} credits!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        try:
            user_msg = await context.bot.send_message(
                target,
                format_hacker(success_box(f"✅ You received +{amount} credits!\nNew balance: check /balance")),
                parse_mode='HTML'
            )
            asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
        except:
            pass
        context.user_data['action'] = None

    elif action == 'waiting_remove_credits':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Format: ID amount")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE users SET credits = credits - ? WHERE user_id=?", (amount, target))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ Removed {amount} from <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        try:
            user_msg = await context.bot.send_message(
                target,
                format_hacker(error_box(f"❌ {amount} credits have been REMOVED from your account.\nContact: {OWNER_LINK}")),
                parse_mode='HTML'
            )
            asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
        except:
            pass
        context.user_data['action'] = None

    elif action == 'waiting_broadcast':
        if not is_admin(user_id): return
        msg_text = text
        users = c.execute("SELECT user_id FROM users").fetchall()
        count = 0
        for u in users:
            try:
                broadcast_msg = await context.bot.send_message(u[0], format_hacker(fancy_box("📢 BROADCAST", msg_text)), parse_mode='HTML')
                asyncio.create_task(auto_delete_message(context, broadcast_msg.chat_id, broadcast_msg.message_id, delay=30))
                count += 1
            except:
                pass
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ Sent to {count} users!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        context.user_data['action'] = None

    elif action == 'waiting_approve':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Format: ID amount")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE credit_requests SET status='approved' WHERE user_id=? AND amount=? AND status='pending'", (target, amount))
        if c.rowcount == 0:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Request not found!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ Approved {amount} for <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        try:
            user_msg = await context.bot.send_message(
                target,
                format_hacker(success_box(f"✅ Your credit request of {amount} credits has been APPROVED!\n\nNew balance: check /balance\n\nContact: {OWNER_LINK}")),
                parse_mode='HTML'
            )
            asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
        except:
            pass
        context.user_data['action'] = None

    elif action == 'waiting_reject':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            msg = await update.message.reply_text(format_hacker(error_box("❌ Give valid ID!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
            return
        c.execute("UPDATE credit_requests SET status='rejected' WHERE user_id=? AND status='pending'", (target,))
        conn.commit()
        msg = await update.message.reply_text(format_hacker(success_box(f"✅ Rejected <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        try:
            user_msg = await context.bot.send_message(
                target,
                format_hacker(error_box(f"❌ Your credit request has been REJECTED.\n\nContact: {OWNER_LINK}")),
                parse_mode='HTML'
            )
            asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
        except:
            pass
        context.user_data['action'] = None

    else:
        msg = await update.message.reply_text(format_hacker(fancy_box("❓", "Use the buttons below!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

# ======================== Admin Commands ============
async def giveall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    if not context.args:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /giveall <amount>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        amount = int(context.args[0])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give a valid amount!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET credits = credits + ?", (amount,))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ Everyone got {amount} credits!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

async def addcredits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Denied.")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    if len(context.args) < 2:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /addcredits <id> <amount>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> got +{amount} credits!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    try:
        user_msg = await context.bot.send_message(
            target,
            format_hacker(success_box(f"✅ You received +{amount} credits!\nNew balance: check /balance")),
            parse_mode='HTML'
        )
        asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
    except:
        pass

async def cmd_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SUPER_ADMIN_ID:
        msg = await update.message.reply_text(format_hacker(error_box("🚫 Super Admin only!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    if not context.args:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /add_admin <id>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give valid ID!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET is_admin = 1 WHERE user_id=?", (target,))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> is now admin!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

async def cmd_switch_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /switch_user <id>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give valid ID!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET credits = 999999 WHERE user_id=?", (target,))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ <code>{target}</code> unlimited!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

async def cmd_remove_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /remove_credits <id> <amount>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET credits = credits - ? WHERE user_id=?", (amount, target))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ Removed {amount} from <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    try:
        user_msg = await context.bot.send_message(
            target,
            format_hacker(error_box(f"❌ {amount} credits have been REMOVED from your account.\nContact: {OWNER_LINK}")),
            parse_mode='HTML'
        )
        asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
    except:
        pass

async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /broadcast <msg>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    msg_text = ' '.join(context.args)
    users = c.execute("SELECT user_id FROM users").fetchall()
    count = 0
    for u in users:
        try:
            broadcast_msg = await context.bot.send_message(u[0], format_hacker(fancy_box("📢 BROADCAST", msg_text)), parse_mode='HTML')
            asyncio.create_task(auto_delete_message(context, broadcast_msg.chat_id, broadcast_msg.message_id, delay=30))
            count += 1
        except:
            pass
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ Sent to {count} users!")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

async def cmd_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /approve <id> <amount>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give numbers!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE credit_requests SET status='approved' WHERE user_id=? AND amount=? AND status='pending'", (target, amount))
    if c.rowcount == 0:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Request not found!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ Approved {amount} for <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    try:
        user_msg = await context.bot.send_message(
            target,
            format_hacker(success_box(f"✅ Your credit request of {amount} credits has been APPROVED!\n\nNew balance: check /balance\n\nContact: {OWNER_LINK}")),
            parse_mode='HTML'
        )
        asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
    except:
        pass

async def cmd_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        msg = await update.message.reply_text(format_hacker(error_box("❌ /reject <id>")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    try:
        target = int(context.args[0])
    except:
        msg = await update.message.reply_text(format_hacker(error_box("❌ Give valid ID!")), parse_mode='HTML')
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    c.execute("UPDATE credit_requests SET status='rejected' WHERE user_id=? AND status='pending'", (target,))
    conn.commit()
    msg = await update.message.reply_text(format_hacker(success_box(f"✅ Rejected <code>{target}</code>")), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
    try:
        user_msg = await context.bot.send_message(
            target,
            format_hacker(error_box(f"❌ Your credit request has been REJECTED.\n\nContact: {OWNER_LINK}")),
            parse_mode='HTML'
        )
        asyncio.create_task(auto_delete_message(context, user_msg.chat_id, user_msg.message_id, delay=30))
    except:
        pass

# ======================== Admin Panel =========================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        msg = await update.message.reply_text(format_hacker(error_box("🚫 You're not admin!")), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
        asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))
        return
    keyboard = [
        [InlineKeyboardButton("📊 All Users", callback_data="admin_users")],
        [InlineKeyboardButton("💰 Pending Requests", callback_data="admin_requests")],
        [InlineKeyboardButton("📋 Commands Copy", callback_data="admin_commands")],
    ]
    msg = await update.message.reply_text(format_hacker(admin_panel_box("Solid control, bro!")), parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    asyncio.create_task(auto_delete_message(context, update.message.chat_id, update.message.message_id, delay=3))
    asyncio.create_task(auto_delete_message(context, msg.chat_id, msg.message_id, delay=15))

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.edit_message_text(format_hacker(error_box("🚫 You're not admin!")), parse_mode='HTML')
        return
    data = query.data
    if data == "admin_users":
        users = c.execute("SELECT user_id, credits, total_searches FROM users ORDER BY credits DESC").fetchall()
        msg = "📊 All Users (Top 20):\n\n"
        for u in users[:20]:
            msg += f"<code>{u[0]}</code> → {u[1]} credits, {u[2]} searches\n"
        await query.edit_message_text(format_hacker(fancy_box("📊 USERS", msg)), parse_mode='HTML')
    elif data == "admin_requests":
        reqs = c.execute("SELECT id, user_id, amount FROM credit_requests WHERE status='pending'").fetchall()
        if not reqs:
            await query.edit_message_text(format_hacker(fancy_box("✅", "No pending, bro!")), parse_mode='HTML')
            return
        msg = "📋 Pending Requests:\n\n"
        for r in reqs:
            msg += f"ID: {r[0]} | User: <code>{r[1]}</code> | Amount: {r[2]}\n"
        await query.edit_message_text(format_hacker(fancy_box("💰 REQUESTS", msg)), parse_mode='HTML')
    elif data == "admin_commands":
        await query.edit_message_text(
            format_hacker(fancy_box("📋 COMMANDS",
                "/add_admin <id>\n/switch_user <id>\n/addcredits <id> <amt>\n"
                "/remove_credits <id> <amt>\n/giveall <amt>\n/broadcast <msg>\n"
                "/approve <id> <amt>\n/reject <id>"
            )),
            parse_mode='HTML'
        )

# ======================== Error Handler ======================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# ======================== Main Engine =========================
if __name__ == "__main__":
    timeout_request = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0
    )

    app = Application.builder().token(BOT_TOKEN).request(timeout_request).build()

    app.add_error_handler(error_handler)

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", button_search))
    app.add_handler(CommandHandler("balance", button_balance))
    app.add_handler(CommandHandler("request_credits", button_request_credits))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("add_admin", cmd_add_admin))
    app.add_handler(CommandHandler("switch_user", cmd_switch_user))
    app.add_handler(CommandHandler("addcredits", addcredits))
    app.add_handler(CommandHandler("giveall", giveall))
    app.add_handler(CommandHandler("remove_credits", cmd_remove_credits))
    app.add_handler(CommandHandler("broadcast", cmd_broadcast))
    app.add_handler(CommandHandler("approve", cmd_approve))
    app.add_handler(CommandHandler("reject", cmd_reject))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("pay49", pay_handler))
    app.add_handler(CommandHandler("pay79", pay_handler))
    app.add_handler(CommandHandler("pay99", pay_handler))

    # Button handlers
    button_handlers = [
        ("🔍 Search", button_search),
        ("💰 Balance", button_balance),
        ("🆘 Help", help_handler),
        ("📨 Request Credits", button_request_credits),
        ("👑 Admin Panel", admin_panel),
        ("➕ Add Admin", button_add_admin),
        ("🔄 Switch User", button_switch_user),
        ("➕ Add Credits", button_add_credits),
        ("➖ Remove Credits", button_remove_credits),
        ("📢 Broadcast", button_broadcast),
        ("✅ Approve", button_approve),
        ("❌ Reject", button_reject),
        ("💳 Credits Guide", button_give_credits_guide),
    ]
    for text, handler in button_handlers:
        app.add_handler(MessageHandler(filters.Regex(f'^{text}$'), handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(admin_callback))

    print("🔥 Vish – 20 Borders – Running, Maharaj!")
    app.run_polling(drop_pending_updates=True)

# -*- coding: utf-8 -*-
"""
Bot Name: Xenonc Instagram Scanner (Only Instagram)
Owner: @Xenon33cyber
"""

import sqlite3
import random
import string
import aiohttp
import json
import asyncio
import logging
import os
import sys
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
import httpx

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# 🔥 Bot Configuration
BOT_TOKEN = "8796970293:AAG6cZnPDhktqQFpemTTbi6Ps4S_JlE-t3s"
SUPER_ADMIN_ID = 6303062255
INSTAGRAM_API = "https://instagram.abbasofficaldevs.workers.dev/info?username="
# ============================================================

# ======================== Database ===========================
DB_FILE = "xenonc_bot.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    is_admin INTEGER DEFAULT 0
)''')

c.execute("INSERT OR IGNORE INTO users (user_id, is_admin) VALUES (?, 1)", (SUPER_ADMIN_ID,))
conn.commit()

def get_user(user_id):
    try:
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if not user:
            c.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return (user_id, 0)
        return user
    except:
        return (user_id, 0)

def is_admin(user_id):
    user = get_user(user_id)
    return user[1] == 1

# ======================== Branding ===========================
def hacker_header():
    return "💀 [OWNER] :: @Xenon33cyber\n" + "═" * 30 + "\n"

def hacker_footer():
    return "\n" + "═" * 30 + "\n🔥 Xenonc Instagram Scanner"

def format_hacker(msg):
    return hacker_header() + msg + hacker_footer()

# ======================== Keyboard ===========================
def get_main_keyboard(user_id):
    admin = is_admin(user_id)
    keyboard = []
    keyboard.append([KeyboardButton("📸 Instagram Scan"), KeyboardButton("🆘 Help")])

    if admin:
        keyboard.append([KeyboardButton("👑 Admin Panel")])
        keyboard.append([KeyboardButton("➕ Add Admin"), KeyboardButton("📢 Broadcast")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

# ======================== Instagram API Call ==================
async def fetch_instagram_data(username):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(INSTAGRAM_API + username, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and data.get('account'):
                        return data
                    else:
                        return {"error": "No Instagram account found, bro!"}
                else:
                    return {"error": f"Instagram API error: HTTP {resp.status}"}
        except aiohttp.ClientConnectorError:
            return {"error": "Network error – check your internet, dude!"}
        except asyncio.TimeoutError:
            return {"error": "Timeout – Instagram server is sleepy, try again."}
        except aiohttp.ClientResponseError as e:
            return {"error": f"API error: {str(e)}"}
        except Exception as e:
            return {"error": f"Something went wrong: {str(e)}"}

def format_instagram_data(data, username):
    """Format Instagram data as per your required structure"""
    acc = data.get('account', {})
    stats = data.get('stats', {})
    prof = data.get('profile', {})
    pic = prof.get('profile_pic_size', {})

    joined = acc.get('joined', {})
    joined_date = joined.get('date', 'N/A')
    joined_ts = joined.get('timestamp', 'N/A')

    acc_type = acc.get('account_type', 0)
    acc_type_str = {
        0: "Personal",
        1: "Business",
        2: "Creator"
    }.get(acc_type, "Unknown")

    location = data.get('location', {})
    features = data.get('features', {})
    privacy = data.get('privacy', {})
    public_email = data.get('public_email', 'N/A')
    public_phone = data.get('public_phone', 'N/A')
    external_url = data.get('external_url', 'N/A')

    msg = (
        f"📱 <b>Instagram Profile</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>🔹 ACCOUNT</b>\n"
        f"🆔 <b>ID:</b> {acc.get('id', 'N/A')}\n"
        f"👤 <b>Username:</b> @{acc.get('username', username)}\n"
        f"📛 <b>Full Name:</b> {acc.get('full_name', 'N/A')}\n"
        f"📝 <b>Bio:</b> {acc.get('bio', 'N/A')}\n"
        f"📅 <b>Joined:</b> {joined_date} (Unix: {joined_ts})\n"
        f"🔁 <b>Former Usernames:</b> {acc.get('former_usernames', 0)}\n"
        f"✅ <b>Verified:</b> {'✅ Yes' if acc.get('verified') else '❌ No'}\n"
        f"🔒 <b>Private:</b> {'🔒 Yes' if acc.get('private') else '🌍 No'}\n"
        f"🏷️ <b>Account Type:</b> {acc_type_str} (Type {acc_type})\n"
        f"💼 <b>Business:</b> {'✅ Yes' if acc.get('is_business') else '❌ No'}\n"
        f"🎨 <b>Creator:</b> {'✅ Yes' if acc.get('is_creator') else '❌ No'}\n"
        f"📂 <b>Category:</b> {acc.get('category', 'N/A')}\n"
        f"📧 <b>Public Email:</b> {public_email}\n"
        f"📞 <b>Public Phone:</b> {public_phone}\n"
        f"🔗 <b>External URL:</b> <a href='{external_url}'>{external_url[:30]}...</a>\n\n"
        f"<b>📊 STATS</b>\n"
        f"👥 <b>Followers:</b> {stats.get('followers', 0):,}\n"
        f"👤 <b>Following:</b> {stats.get('following', 0):,}\n"
        f"📸 <b>Posts:</b> {stats.get('posts', 0):,}\n\n"
        f"<b>🖼️ PROFILE</b>\n"
        f"🆔 <b>Profile ID:</b> {prof.get('profile_id', 'N/A')}\n"
        f"📱 <b>FBID:</b> {prof.get('fbid', 'N/A')}\n"
        f"🔑 <b>Instagram PK:</b> {prof.get('instagram_pk', 'N/A')}\n"
        f"🖼️ <b>Profile Pic:</b> <a href='{prof.get('profile_pic_hd', '#')}'>📸 View</a>\n"
        f"📐 <b>Pic Size:</b> {pic.get('width', 'N/A')}x{pic.get('height', 'N/A')} px\n\n"
        f"<b>📍 LOCATION</b>\n"
        f"🌍 <b>Country:</b> {location.get('country', 'N/A')}\n"
        f"🏙️ <b>City:</b> {location.get('city', 'N/A')}\n"
        f"🌐 <b>Latitude:</b> {location.get('latitude', 'N/A')}\n"
        f"🌐 <b>Longitude:</b> {location.get('longitude', 'N/A')}\n\n"
        f"<b>⚙️ FEATURES</b>\n"
        f"💬 <b>Can DM:</b> {'✅ Yes' if features.get('can_dm') else '❌ No'}\n"
        f"📢 <b>Broadcast Creator:</b> {'✅ Yes' if features.get('broadcast_channel_creator') else '❌ No'}\n"
        f"🧵 <b>Has Threads:</b> {'✅ Yes' if features.get('has_threads') else '❌ No'}\n"
        f"⭐ <b>Has Highlights:</b> {'✅ Yes' if features.get('has_highlights') else '❌ No'}\n"
        f"🎬 <b>Has Videos:</b> {'✅ Yes' if features.get('has_videos') else '❌ No'}\n"
        f"👤 <b>Has Avatar:</b> {'✅ Yes' if features.get('has_avatar') else '❌ No'}\n"
        f"📊 <b>Show Post Insights:</b> {'✅ Yes' if features.get('show_post_insights') else '❌ No'}\n\n"
        f"<b>🔒 PRIVACY</b>\n"
        f"🔍 <b>Profile Search Enabled:</b> {'✅ Yes' if privacy.get('profile_search_enabled') else '❌ No'}\n"
        f"💬 <b>WhatsApp Linked:</b> {'✅ Yes' if privacy.get('whatsapp_linked') else '❌ No'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 <b>Open Profile:</b> <a href='https://instagram.com/{acc.get('username', username)}'>@instagram.com</a>"
    )
    return msg

# ======================== Help ==============================
HELP_TEXT = (
    "🗣️ <b>Hey, listen up!</b>\n\n"
    "👉 <b>Owner:</b> @Xenon33cyber\n"
    "📢 <b>Updates Channel:</b> @Xenoncyber33\n"
    "🛠️ <b>Support:</b> @xenondaemon_Team\n\n"
    "📸 <b>Xenonc Instagram Scanner</b>\n"
    "Use: /instagram &lt;username&gt;\n"
    "Example: /instagram skincare3\n\n"
    "🔹 <b>Features:</b>\n"
    "• Full profile details\n"
    "• Followers / Following / Posts\n"
    "• Profile pic (HD) link\n"
    "• Account type & status\n"
    "• Location info\n"
    "• Features & privacy settings\n\n"
    "💀 <b>Owner's oath:</b> Fast, reliable, and full data!"
)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        format_hacker(HELP_TEXT),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(user_id)
    )

# ======================== Start ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    user = get_user(user_id)
    first_name = update.effective_user.first_name or "Bro"
    username = update.effective_user.username
    user_display = f"@{username}" if username else first_name
    admin_tag = "👑 <b>Admin Sahab</b>" if user[1] == 1 else f"<b>{user_display}</b>"
    
    msg = (
        f"📸 <b>Xenonc Instagram Scanner</b>\n\n"
        f"💀 <b>What's up, bro!</b> {admin_tag}\n"
        f"📸 <b>Command:</b> /instagram &lt;username&gt;\n"
        f"🔹 <b>Example:</b> /instagram skincare3\n\n"
        f"🔹 <b>Features:</b>\n"
        "• Full profile details\n"
        "• Followers / Following / Posts\n"
        "• Profile pic (HD)\n"
        "• Account type & status\n"
        "• Location info\n"
        "• Features & privacy settings\n\n"
        f"📢 <b>Updates:</b> @Xenoncyber33 | @xenondaemon_Team"
    )
    formatted_msg = format_hacker(msg)

    await update.message.reply_text(
        formatted_msg,
        parse_mode='HTML',
        reply_markup=get_main_keyboard(user_id)
    )

# ======================== INSTAGRAM LOOKUP ====================
async def instagram_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            format_hacker("❌ <b>Enter Instagram username, bro!</b>\n> Example: /instagram skincare3"),
            parse_mode='HTML'
        )
        return

    username = context.args[0].strip()
    msg = await update.message.reply_text(
        format_hacker("⏳ <b>Fetching Instagram data, bro...</b>"),
        parse_mode='HTML'
    )

    data = await fetch_instagram_data(username)

    if "error" in data:
        await msg.edit_text(
            format_hacker(f"❌ <b>Error:</b> {data['error']}"),
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )
        return

    formatted = format_instagram_data(data, username)
    await msg.edit_text(
        format_hacker(formatted),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(user_id)
    )

async def button_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        format_hacker("📸 <b>Enter Instagram username, bro!</b>\n> Example: skincare3"),
        parse_mode='HTML'
    )
    context.user_data['action'] = 'waiting_instagram'

# ======================== Admin Commands ====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(format_hacker("🚫 <b>You're not admin, bro!</b>"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        return
    keyboard = [
        [InlineKeyboardButton("📊 All Users", callback_data="admin_users")],
        [InlineKeyboardButton("📋 Commands Copy", callback_data="admin_commands")],
    ]
    await update.message.reply_text(format_hacker("👑 <b>Admin Panel – solid control!</b>"), parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.edit_message_text(format_hacker("🚫 <b>You're not admin, bro!</b>"), parse_mode='HTML')
        return
    data = query.data
    if data == "admin_users":
        users = c.execute("SELECT user_id, is_admin FROM users").fetchall()
        msg = "📊 <b>All Users:</b>\n\n"
        for u in users[:50]:
            admin_tag = "👑 Admin" if u[1] == 1 else "👤 User"
            msg += f"<code>{u[0]}</code> → {admin_tag}\n"
        await query.edit_message_text(format_hacker(msg), parse_mode='HTML')
    elif data == "admin_commands":
        await query.edit_message_text(
            format_hacker(
                "📋 <b>Commands Copy:</b>\n\n"
                "/add_admin &lt;id&gt;\n"
                "/broadcast &lt;msg&gt;\n"
                "/instagram &lt;username&gt;"
            ),
            parse_mode='HTML'
        )

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != SUPER_ADMIN_ID:
        await update.message.reply_text(format_hacker("🚫 Super Admin only!"), parse_mode='HTML')
        return
    if not context.args:
        await update.message.reply_text(format_hacker("❌ /add_admin <id>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
    except:
        await update.message.reply_text(format_hacker("❌ Give valid ID, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET is_admin = 1 WHERE user_id=?", (target,))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> is now admin, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML')
        return
    if not context.args:
        await update.message.reply_text(format_hacker("❌ /broadcast <msg>"), parse_mode='HTML')
        return
    msg = ' '.join(context.args)
    users = c.execute("SELECT user_id FROM users").fetchall()
    count = 0
    for u in users:
        try:
            await context.bot.send_message(u[0], format_hacker(f"📢 <b>Broadcast:</b>\n{msg}"), parse_mode='HTML')
            count += 1
        except:
            pass
    await update.message.reply_text(format_hacker(f"✅ Sent to {count} users, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

# ======================== Text Handler ======================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    action = context.user_data.get('action')

    if text.lower() in ["help", "🆘 help"]:
        await help_handler(update, context)
        return

    if action == 'waiting_instagram':
        context.user_data['action'] = None
        # Create fake context with args
        class FakeContext:
            def __init__(self, username):
                self.args = [username]
        fake_ctx = FakeContext(text)
        await instagram_lookup(update, fake_ctx)

    else:
        await update.message.reply_text(format_hacker("❓ Use buttons below, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))

# ======================== Error Handler =====================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# ======================== Main ============================
if __name__ == "__main__":
    # Kill any existing bot processes
    try:
        os.system("pkill -f 'python.*bot.py' 2>/dev/null || true")
        os.system("pkill -f 'python.*@MasterOsint33_bot.py' 2>/dev/null || true")
        os.system("pkill -f 'python.*xenonc.*' 2>/dev/null || true")
    except:
        pass

    print("🔥 Starting Xenonc Instagram Scanner...")
    print("📡 Connecting to Telegram...")

    # Create a custom HTTPX client with longer timeouts and retries
    timeout = httpx.Timeout(
        connect=120.0,
        read=120.0,
        write=120.0,
        pool=120.0
    )
    
    transport = httpx.AsyncHTTPTransport(retries=5)
    client = httpx.AsyncClient(timeout=timeout, transport=transport)
    
    timeout_request = HTTPXRequest(
        connect_timeout=120.0,
        read_timeout=120.0,
        write_timeout=120.0,
        pool_timeout=120.0,
        client=client
    )

    app = Application.builder().token(BOT_TOKEN).request(timeout_request).build()

    app.add_error_handler(error_handler)

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("instagram", instagram_lookup))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("add_admin", add_admin))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Button handlers
    button_handlers = [
        ("📸 Instagram Scan", button_instagram),
        ("🆘 Help", help_handler),
        ("👑 Admin Panel", admin_panel),
        ("➕ Add Admin", add_admin),
        ("📢 Broadcast", broadcast),
    ]
    for text, handler in button_handlers:
        app.add_handler(MessageHandler(filters.Regex(f'^{text}$'), handler))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(admin_callback))

    print("🔥 Xenonc Instagram Scanner – Only Instagram, Maharaj!")
    print("🔄 Retry count: 5 | Timeout: 120 seconds")
    print("📡 Bot is live! Send /start to test.")
    app.run_polling(drop_pending_updates=True)
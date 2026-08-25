# -*- coding: utf-8 -*-
"""
Bot Name: Vish - Hacker Boy (English Only, Auto Delete History, Error Fixed)
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
BOT_TOKEN = "8716988605:AAF5b7qE4Thm-a74jqE9EZJQcEQ7HobYD4k"
SUPER_ADMIN_ID = 6303062255
API_URL = "https://adityaapi.onrender.com/api/v1/info?key=Rahul&query="
# ============================================================

# ======================== Database ===========================
DB_FILE = "vish_bot.db"
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

# ======================== Branding ===========================
def hacker_header():
    return "💀 [OWNER] :: @Xenon33cyber\n" + "═" * 30 + "\n"

def hacker_footer():
    return "\n" + "═" * 30 + "\n💳 Credits? Talk to Owner – solid deal! 😎"

def format_hacker(msg):
    return hacker_header() + msg + hacker_footer()

def info_box(title, content):
    border = "▬" * 40
    return f"📦 <b>{title}</b>\n{border}\n{content}\n{border}"

# ======================== Keyboard (English) ==================
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
                        return {"error": "No info found for this number, bro!"}
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

# ======================== Help (English) ======================
HELP_TEXT = (
    "🗣️ <b>Hey, listen up!</b>\n\n"
    "👉 <b>Owner:</b> @Xenon33cyber\n"
    "📢 <b>Updates Channel:</b> @Xenoncyber33\n"
    "🛠️ <b>Support:</b> @xenondaemon_Team\n\n"
    "Only DM the Owner if money is deducted and credits don't arrive.\n"
    'No "give demo", "free", "try 1 rupee" – don\'t do that. Owner\'s phone gets hot! 😂\n'
    "If the bot is broken, let us know – we'll fix it.\n\n"
    "💰 <b>Plans (cheap, full value)</b>\n\n"
    "🟢 <b>₹49 – Micro (Trial)</b>\n"
    "➜ 90 Credits (9 Searches)\n"
    "➜ ₹5.4 per search\n"
    "➜ Best for new users – test it out\n\n"
    "🟡 <b>₹79 – Starter (Most popular)</b>\n"
    "➜ 160 Credits (16 Searches)\n"
    "➜ ₹4.9 per search (cheap loot)\n"
    "➜ Perfect for 1-2 daily searches\n\n"
    "🔴 <b>₹99 – Best Seller (Heavy user)</b>\n"
    "➜ 210 Credits (21 Searches)\n"
    "➜ ₹4.7 per search! (even below our cost 😅)\n"
    "➜ For those who search 4-5 numbers a day – just take this\n\n"
    "👇 <b>Which one?</b>\n"
    "/pay49\n/pay79\n/pay99\n\n"
    "💀 <b>Owner's oath:</b> Pay and credits will be added instantly. If not, shout at @Xenon33cyber or @xenondaemon_Team!\n"
    "Don't waste time, Owner needs sleep too. 😴🔥"
)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await update.message.reply_photo(
            photo="https://i.postimg.cc/ZYyRDgLs/file-00000000150881faadd26581a4e1144d.png",
            caption=HELP_TEXT,
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )
    except Exception:
        await update.message.reply_text(
            format_hacker(HELP_TEXT),
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )

async def pay_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        format_hacker("💳 <b>DM for payment:</b>\n@Xenon33cyber\n\n⚠️ After transaction, send screenshot and your User ID."),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(update.effective_user.id)
    )

# ======================== Start ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    first_name = update.effective_user.first_name or "Bro"
    username = update.effective_user.username
    user_display = f"@{username}" if username else first_name
    admin_tag = "👑 <b>Admin Sahab</b>" if user[5] == 1 else f"<b>{user_display}</b>"
    
    msg = (
        f"💀 <b>What's up, bro!</b> {admin_tag}\n"
        f"🧑‍💻 <b>I'm Xenon – The Hacker Machine</b>\n"
        f"💻 <b>Credits:</b> {user[1]} (20 demo)\n"
        f"⚡ <b>Command:</b> /search &lt;number&gt; or hit the button.\n"
        f"🔐 <b>Cost:</b> 10 credits per search.\n"
        f"📢 <b>Updates:</b> @Xenoncyber33 | @xenondaemon_Team"
    )
    formatted_msg = format_hacker(msg)

    try:
        await update.message.reply_photo(
            photo="https://i.postimg.cc/ZYyRDgLs/file-00000000150881faadd26581a4e1144d.png",
            caption=formatted_msg,
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )
    except Exception:
        await update.message.reply_text(
            formatted_msg,
            parse_mode='HTML',
            reply_markup=get_main_keyboard(user_id)
        )

# ======================== Button Handlers =====================
async def button_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        format_hacker("🔍 <b>Enter number, bro!</b>\n> Format: 9876543210 (without +91)"),
        parse_mode='HTML'
    )
    context.user_data['action'] = 'waiting_search'

async def button_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    msg = f"💰 <b>Your remaining credits:</b> {user[1]}"
    await update.message.reply_text(
        format_hacker(msg),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(update.effective_user.id)
    )

async def button_request_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        format_hacker("📨 <b>How many credits do you need?</b>\n> Example: 20"),
        parse_mode='HTML'
    )
    context.user_data['action'] = 'waiting_request_credits'

async def button_give_credits_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 <b>That's admin work, bro!</b>"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    msg = (
        "💰 <b>Credits Guide</b>\n\n"
        "Use: /giveall <amount>\n"
        "Or: /addcredits <user_id> <amount>\n\n"
        "Examples:\n"
        "/giveall 5\n"
        "/addcredits 123456789 10"
    )
    await update.message.reply_text(
        format_hacker(msg),
        parse_mode='HTML',
        reply_markup=get_main_keyboard(update.effective_user.id)
    )

# Admin Buttons (all in English)
async def button_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("➕ <b>Give User ID, bro</b>\n> Example: 987654321"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_add_admin'

async def button_switch_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("🔄 <b>Give User ID, bro</b>\n> Example: 987654321"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_switch_user'

async def button_add_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("➕ <b>Give ID and Amount, bro</b>\n> Example: 987654321 50"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_add_credits'

async def button_remove_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("➖ <b>Give ID and Amount, bro</b>\n> Example: 987654321 20"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_remove_credits'

async def button_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("📢 <b>Type your message, bro</b>"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_broadcast'

async def button_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("✅ <b>Give ID and Amount, bro</b>\n> Example: 987654321 20"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_approve'

async def button_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
        return
    await update.message.reply_text(format_hacker("❌ <b>Give ID, bro</b>\n> Example: 987654321"), parse_mode='HTML')
    context.user_data['action'] = 'waiting_reject'

# ======================== Text Handler (Auto Delete History, Error Safe) ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    action = context.user_data.get('action')

    # Fallback for help
    if text.lower() in ["help", "🆘 help"]:
        await help_handler(update, context)
        return

    if action == 'waiting_search':
        number = text.replace(" ", "").strip()
        if not number.isdigit():
            await update.message.reply_text(format_hacker("❌ <b>Digits only, bro!</b> Example: 9876543210"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        context.user_data['action'] = None
        user = get_user(user_id)
        if user[1] < 10:
            await update.message.reply_text(format_hacker("🚫 <b>Credits over, bro!</b> /request_credits 10"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return

        new_bal = user[1] - 10
        c.execute("UPDATE users SET credits = ?, total_searches = total_searches + 1 WHERE user_id=?", (new_bal, user_id))
        conn.commit()

        searching_msg = await update.message.reply_text(
            format_hacker("⏳ <b>One sec, pulling info...</b>"),
            parse_mode='HTML'
        )

        full_response = await fetch_number_info(number)

        if not full_response or "error" in full_response:
            error_msg = full_response.get('error', 'Something went wrong!') if full_response else 'Something went wrong!'
            try:
                await searching_msg.edit_text(
                    format_hacker(f"❌ <b>{error_msg}</b>"),
                    parse_mode='HTML',
                    reply_markup=get_main_keyboard(user_id)
                )
            except Exception:
                # If edit fails, send new message
                await update.message.reply_text(
                    format_hacker(f"❌ <b>{error_msg}</b>"),
                    parse_mode='HTML',
                    reply_markup=get_main_keyboard(user_id)
                )
            return

        results = full_response.get('results', [])
        if not results:
            try:
                await searching_msg.edit_text(
                    format_hacker("❌ <b>No results for this number, bro! 😢</b>"),
                    parse_mode='HTML',
                    reply_markup=get_main_keyboard(user_id)
                )
            except Exception:
                await update.message.reply_text(
                    format_hacker("❌ <b>No results for this number, bro! 😢</b>"),
                    parse_mode='HTML',
                    reply_markup=get_main_keyboard(user_id)
                )
            return

        total_count = full_response.get('count', len(results))
        box_content = f"📞 <b>Number:</b> <code>{number}</code>\n💰 <b>Remaining Credits:</b> {new_bal}\n"
        box_content += f"📊 <b>Total results:</b> {total_count}\n\n"

        for i, res in enumerate(results[:10], 1):
            name = res.get('name', 'N/A')
            fname = res.get('fname', 'N/A')
            mobile = res.get('mobile', 'N/A')
            email = res.get('email', 'N/A')
            address = res.get('address', 'N/A')
            circle = res.get('circle', 'N/A')
            alt = res.get('alt', 'N/A')
            id_field = res.get('id', 'N/A')
            
            box_content += (
                f"╔══════ Result {i} ══╗\n"
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
        
        if len(results) > 10:
            box_content += f"\n⚠️ <b>Showing first 10, search more for the rest.</b>"

        parsed_msg = info_box("FULL INFO", box_content)
        final_text = format_hacker(parsed_msg)

        try:
            await searching_msg.edit_text(
                final_text,
                parse_mode='HTML',
                reply_markup=get_main_keyboard(user_id)
            )
        except Exception:
            # If edit fails, send as new message
            await update.message.reply_text(
                final_text,
                parse_mode='HTML',
                reply_markup=get_main_keyboard(user_id)
            )

    elif action == 'waiting_request_credits':
        try:
            amount = int(text)
        except:
            await update.message.reply_text(format_hacker("❌ <b>Enter a valid number, bro!</b>"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("INSERT INTO credit_requests (user_id, amount) VALUES (?, ?)", (user_id, amount))
        conn.commit()
        
        username = update.effective_user.username or "NoUsername"
        user_link = f"<a href='tg://user?id={user_id}'>@{username}</a>"
        admin_msg = (
            f"📩 <b>Credit Request</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>User:</b> {user_link}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"💰 <b>Requested:</b> {amount} credits\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%I:%M %p')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Use: <code>/addcredits {user_id} {amount}</code>"
        )
        admins = c.execute("SELECT user_id FROM users WHERE is_admin=1").fetchall()
        for admin in admins:
            try:
                await context.bot.send_message(admin[0], format_hacker(admin_msg), parse_mode='HTML')
            except:
                pass
        await update.message.reply_text(format_hacker("✅ <b>Request sent, bro!</b>"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_add_admin':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            await update.message.reply_text(format_hacker("❌ Give a valid ID, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE users SET is_admin = 1 WHERE user_id=?", (target,))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> is now admin, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_switch_user':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            await update.message.reply_text(format_hacker("❌ Give a valid ID, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE users SET credits = 999999 WHERE user_id=?", (target,))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> got unlimited credits – go wild!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_add_credits':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text(format_hacker("❌ Format: ID amount"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> got +{amount} credits, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_remove_credits':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text(format_hacker("❌ Format: ID amount"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE users SET credits = credits - ? WHERE user_id=?", (amount, target))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ Removed {amount} from <code>{target}</code>, solid!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_broadcast':
        if not is_admin(user_id): return
        msg = text
        users = c.execute("SELECT user_id FROM users").fetchall()
        count = 0
        for u in users:
            try:
                await context.bot.send_message(u[0], format_hacker(f"📢 <b>Broadcast:</b>\n{msg}"), parse_mode='HTML')
                count += 1
            except:
                pass
        await update.message.reply_text(format_hacker(f"✅ Sent to {count} users, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        context.user_data['action'] = None

    elif action == 'waiting_approve':
        if not is_admin(user_id): return
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text(format_hacker("❌ Format: ID amount"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        try:
            target = int(parts[0])
            amount = int(parts[1])
        except:
            await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE credit_requests SET status='approved' WHERE user_id=? AND amount=? AND status='pending'", (target, amount))
        if c.rowcount == 0:
            await update.message.reply_text(format_hacker("❌ Request not found, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ Approved {amount} for <code>{target}</code> – awesome!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        try:
            await context.bot.send_message(target, format_hacker(f"✅ +{amount} credits approved, bro!"), parse_mode='HTML')
        except:
            pass
        context.user_data['action'] = None

    elif action == 'waiting_reject':
        if not is_admin(user_id): return
        try:
            target = int(text)
        except:
            await update.message.reply_text(format_hacker("❌ Give valid ID, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
            return
        c.execute("UPDATE credit_requests SET status='rejected' WHERE user_id=? AND status='pending'", (target,))
        conn.commit()
        await update.message.reply_text(format_hacker(f"✅ Rejected <code>{target}</code> – no worries!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        try:
            await context.bot.send_message(target, format_hacker("❌ Request rejected, bro!"), parse_mode='HTML')
        except:
            pass
        context.user_data['action'] = None

    else:
        await update.message.reply_text(format_hacker("❓ Use the buttons below, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))

# ======================== Admin Commands (English) ============
async def giveall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML')
        return
    if not context.args:
        await update.message.reply_text(format_hacker("❌ /giveall <amount>"), parse_mode='HTML')
        return
    try:
        amount = int(context.args[0])
    except:
        await update.message.reply_text(format_hacker("❌ Give a valid amount, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET credits = credits + ?", (amount,))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ Everyone got {amount} credits, bro!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

async def addcredits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(format_hacker("🚫 Denied."), parse_mode='HTML')
        return
    if len(context.args) < 2:
        await update.message.reply_text(format_hacker("❌ /addcredits <id> <amount>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> got +{amount} credits – enjoy!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

async def cmd_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def cmd_switch_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text(format_hacker("❌ /switch_user <id>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
    except:
        await update.message.reply_text(format_hacker("❌ Give valid ID, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET credits = 999999 WHERE user_id=?", (target,))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ <code>{target}</code> unlimited – play on!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

async def cmd_remove_credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        await update.message.reply_text(format_hacker("❌ /remove_credits <id> <amount>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET credits = credits - ? WHERE user_id=?", (amount, target))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ Removed {amount} from <code>{target}</code> – solid!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))

async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
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

async def cmd_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if len(context.args) < 2:
        await update.message.reply_text(format_hacker("❌ /approve <id> <amount>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
        amount = int(context.args[1])
    except:
        await update.message.reply_text(format_hacker("❌ Give numbers, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE credit_requests SET status='approved' WHERE user_id=? AND amount=? AND status='pending'", (target, amount))
    if c.rowcount == 0:
        await update.message.reply_text(format_hacker("❌ Request not found, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id=?", (amount, target))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ Approved {amount} for <code>{target}</code> – awesome!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    try:
        await context.bot.send_message(target, format_hacker(f"✅ +{amount} credits approved, bro!"), parse_mode='HTML')
    except:
        pass

async def cmd_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text(format_hacker("❌ /reject <id>"), parse_mode='HTML')
        return
    try:
        target = int(context.args[0])
    except:
        await update.message.reply_text(format_hacker("❌ Give valid ID, bro!"), parse_mode='HTML')
        return
    c.execute("UPDATE credit_requests SET status='rejected' WHERE user_id=? AND status='pending'", (target,))
    conn.commit()
    await update.message.reply_text(format_hacker(f"✅ Rejected <code>{target}</code> – no worries!"), parse_mode='HTML', reply_markup=get_main_keyboard(update.effective_user.id))
    try:
        await context.bot.send_message(target, format_hacker("❌ Request rejected, bro!"), parse_mode='HTML')
    except:
        pass

# ======================== Admin Panel =========================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(format_hacker("🚫 <b>You're not admin, bro!</b>"), parse_mode='HTML', reply_markup=get_main_keyboard(user_id))
        return
    keyboard = [
        [InlineKeyboardButton("📊 All Users", callback_data="admin_users")],
        [InlineKeyboardButton("💰 Pending Requests", callback_data="admin_requests")],
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
        users = c.execute("SELECT user_id, credits, total_searches FROM users ORDER BY credits DESC").fetchall()
        msg = "📊 <b>All Users (Top 20):</b>\n\n"
        for u in users[:20]:
            msg += f"<code>{u[0]}</code> → {u[1]} credits, {u[2]} searches\n"
        await query.edit_message_text(format_hacker(msg), parse_mode='HTML')
    elif data == "admin_requests":
        reqs = c.execute("SELECT id, user_id, amount FROM credit_requests WHERE status='pending'").fetchall()
        if not reqs:
            await query.edit_message_text(format_hacker("✅ No pending, bro!"), parse_mode='HTML')
            return
        msg = "📋 <b>Pending Requests:</b>\n\n"
        for r in reqs:
            msg += f"ID: {r[0]} | User: <code>{r[1]}</code> | Amount: {r[2]}\n"
        await query.edit_message_text(format_hacker(msg), parse_mode='HTML')
    elif data == "admin_commands":
        await query.edit_message_text(
            format_hacker(
                "📋 <b>Commands Copy:</b>\n\n"
                "/add_admin &lt;id&gt;\n/switch_user &lt;id&gt;\n/addcredits &lt;id&gt; &lt;amt&gt;\n"
                "/remove_credits &lt;id&gt; &lt;amt&gt;\n/giveall &lt;amt&gt;\n/broadcast &lt;msg&gt;\n"
                "/approve &lt;id&gt; &lt;amt&gt;\n/reject &lt;id&gt;"
            ),
            parse_mode='HTML'
        )

# ======================== Error Handler ======================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the developer."""
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

    # Register error handler
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

    # Button handlers – all English labels
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

    print("🔥 Vish – Hacker Boy (English Only, Auto Delete, Error Handler) – Running, Maharaj!")
    app.run_polling(drop_pending_updates=True)
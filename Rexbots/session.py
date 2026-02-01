import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait,
    MessageIdInvalid,
    MessageNotModified
)
from config import API_ID, API_HASH
from database.db import db
from logger import LOGGER
logger = LOGGER(__name__)

LOGIN_STATE = {}
CLEANER_TASK = None
CLEANER_LOCK = asyncio.Lock()
TIMEOUT_SECONDS = 600
ANIMATION_SPEED = 2.0
FLOOD_BUFFER = 2

cancel_keyboard = ReplyKeyboardMarkup([[KeyboardButton("❌ Cancel")]], resize_keyboard=True)
remove_keyboard = ReplyKeyboardRemove()

PROGRESS_STEPS = {
    "WAITING_PHONE": "🟢 Phone Number → 🔵 Code → 🔵 Password",
    "WAITING_CODE": "✅ Phone Number → 🟢 Code → 🔵 Password",
    "WAITING_PASSWORD": "✅ Phone Number → ✅ Code → 🟢 Password",
    "COMPLETE": "✅ Phone Number → ✅ Code → ✅ Password"
}

PROGRESS_BARS = [
    "░░░░░░░░░░ 0%", "█░░░░░░░░░ 10%", "██░░░░░░░░ 20%", "███░░░░░░░ 30%",
    "████░░░░░░ 40%", "█████░░░░░ 50%", "██████░░░░ 60%", "███████░░░ 70%",
    "████████░░ 80%", "█████████░ 90%", "██████████ 100%"
]

LOADING_FRAMES = [
    "🔄 Connecting •••", "🔄 Connecting ••○", "🔄 Connecting •○○",
    "🔄 Connecting ○○○", "🔄 Connecting ○○•", "🔄 Connecting ○••"
]

async def stop_animation(task):
    if task and not task.done():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

async def cleanup_user_state(user_id):
    if user_id in LOGIN_STATE:
        state = LOGIN_STATE[user_id]
        if "data" in state and "client" in state["data"]:
            client = state["data"]["client"]
            if client.is_connected:
                try:
                    await client.disconnect()
                except Exception:
                    pass
        if "anim_task" in state:
            await stop_animation(state["anim_task"])
        del LOGIN_STATE[user_id]

async def state_cleaner_loop():
    while True:
        await asyncio.sleep(60)
        now = time.time()
        expired_users = [uid for uid, state in list(LOGIN_STATE.items()) if now - state.get("timestamp", 0) > TIMEOUT_SECONDS]
        for uid in expired_users:
            await cleanup_user_state(uid)

async def ensure_cleaner_running():
    global CLEANER_TASK
    async with CLEANER_LOCK:
        if CLEANER_TASK is None or CLEANER_TASK.done():
            CLEANER_TASK = asyncio.create_task(state_cleaner_loop())

async def animate_loading(client: Client, user_id: int, chat_id: int):
    frame_index = 0
    while True:
        if user_id not in LOGIN_STATE: break
        current_msg_id = LOGIN_STATE[user_id].get("status_msg_id")
        frame = LOADING_FRAMES[frame_index % len(LOADING_FRAMES)]
        try:
            await client.edit_message_text(chat_id, current_msg_id, f"<b>{frame}</b>", parse_mode=enums.ParseMode.HTML)
            await asyncio.sleep(ANIMATION_SPEED)
        except MessageNotModified:
            await asyncio.sleep(ANIMATION_SPEED)
        except MessageIdInvalid:
            try:
                new_msg = await client.send_message(chat_id, f"<b>{frame}</b>", parse_mode=enums.ParseMode.HTML)
                if user_id in LOGIN_STATE:
                    LOGIN_STATE[user_id]["status_msg_id"] = new_msg.id
            except:
                break
        except FloodWait as fw:
            await asyncio.sleep(fw.value + FLOOD_BUFFER)
        except Exception:
            break
        frame_index += 1

async def update_progress(client: Client, user_id: int, chat_id: int, step: str, additional_text: str = ""):
    progress_text = PROGRESS_STEPS.get(step, PROGRESS_STEPS["WAITING_PHONE"])
    bar_index = 0
    if step == "WAITING_PHONE": bar_index = 3
    elif step == "WAITING_CODE": bar_index = 6
    elif step == "WAITING_PASSWORD": bar_index = 8
    elif step == "COMPLETE": bar_index = 10
    bar = PROGRESS_BARS[bar_index]
    text = f"<b>Progress: [{bar}]</b>\n<i>{progress_text}</i>\n\n{additional_text}"
    if user_id not in LOGIN_STATE: return
    LOGIN_STATE[user_id]["timestamp"] = time.time()
    current_msg_id = LOGIN_STATE[user_id].get("status_msg_id")
    try:
        await client.edit_message_text(chat_id, current_msg_id, text, parse_mode=enums.ParseMode.HTML)
    except MessageNotModified:
        pass
    except (MessageIdInvalid, Exception):
        try:
            new_msg = await client.send_message(chat_id, text, parse_mode=enums.ParseMode.HTML)
            if user_id in LOGIN_STATE:
                LOGIN_STATE[user_id]["status_msg_id"] = new_msg.id
        except:
            pass

@Client.on_message(filters.private & filters.command("login"))
async def login_start(client: Client, message: Message):
    await ensure_cleaner_running()
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_data = await db.get_session(user_id)
    if user_data:
        return await message.reply("<b>✅ You're already logged in! 🎉</b>\n\nTo switch accounts, first use /logout.", parse_mode=enums.ParseMode.HTML)
    await cleanup_user_state(user_id)
    status_msg = await message.reply("<b>👋 Hey! Let's log you in smoothly 🌟</b>", parse_mode=enums.ParseMode.HTML, reply_markup=cancel_keyboard)
    LOGIN_STATE[user_id] = {"step": "WAITING_PHONE", "data": {}, "status_msg_id": status_msg.id, "timestamp": time.time()}
    additional_text = "📞 Please send your <b>Telegram Phone Number</b> with country code.\n\n<blockquote>Example: +919876543210</blockquote>\n\n<i>💡 Your number is used only for verification and is kept secure. 🔒</i>\n\n❌ Tap the <b>Cancel</b> button or send /cancel to stop."
    await update_progress(client, user_id, chat_id, "WAITING_PHONE", additional_text)

@Client.on_message(filters.private & filters.command("logout"))
async def logout(client: Client, message: Message):
    user_id = message.from_user.id
    await cleanup_user_state(user_id)
    await db.set_session(user_id, session=None)
    await message.reply("<b>🚪 Logout Successful! 👋</b>\n\n<i>Your session has been cleared. You can log in again anytime! 🔄</i>", parse_mode=enums.ParseMode.HTML, reply_markup=remove_keyboard)

@Client.on_message(filters.private & filters.command(["cancel", "cancellogin"]))
async def cancel_login(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in LOGIN_STATE:
        await cleanup_user_state(user_id)
    await message.reply("<b>❌ Login process cancelled. 😌</b>", parse_mode=enums.ParseMode.HTML, reply_markup=remove_keyboard)

async def check_login_state(_, __, message):
    return message.from_user.id in LOGIN_STATE

login_state_filter = filters.create(check_login_state)

@Client.on_message(filters.private & filters.text & login_state_filter & ~filters.command(["cancel", "cancellogin"]))
async def login_handler(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text.strip()
    if user_id not in LOGIN_STATE: return
    state = LOGIN_STATE[user_id]
    step = state["step"]
    if "cancel" in text.lower():
        await cleanup_user_state(user_id)
        await message.reply("<b>❌ Login process cancelled. 😌</b>", parse_mode=enums.ParseMode.HTML, reply_markup=remove_keyboard)
        return
    if step == "WAITING_PHONE":
        phone_number = text.replace(" ", "")
        if not phone_number.startswith('+') or not phone_number[1:].isdigit():
            await update_progress(client, user_id, chat_id, step, "<b>❌ Invalid format! Please use + followed by digits (e.g., +919876543210).</b>")
            return
        temp_client = Client(name=f"session_{user_id}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        await update_progress(client, user_id, chat_id, step, "<b>🔄 Connecting to Telegram... 🌐</b>")
        state["anim_task"] = asyncio.create_task(animate_loading(client, user_id, chat_id))
        try:
            await temp_client.connect()
        except FloodWait as fw:
            await asyncio.sleep(fw.value + FLOOD_BUFFER)
            await temp_client.connect()
        except Exception as e:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, f"<b>❌ Connection failed: {str(e)}. Please try again.</b>")
            del LOGIN_STATE[user_id]
            return
        await stop_animation(state["anim_task"])
        try:
            code = await temp_client.send_code(phone_number)
            state["data"]["client"] = temp_client
            state["data"]["phone"] = phone_number
            state["data"]["hash"] = code.phone_code_hash
            state["step"] = "WAITING_CODE"
            additional_text = "<b>📩 OTP Sent to your app! 📲</b>\n\nPlease open your Telegram app and copy the verification code.\n\n<b>Send it like this:</b> <code>12 345</code> or <code>1 2 3 4 5 6</code>\n\n<blockquote>Adding spaces helps prevent Telegram from deleting the message automatically. 💡</blockquote>"
            await update_progress(client, user_id, chat_id, "WAITING_CODE", additional_text)
        except PhoneNumberInvalid:
            await update_progress(client, user_id, chat_id, step, "<b>❌ Oops! Invalid phone number. 😅 Please try again (e.g., +919876543210).</b>")
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
        except FloodWait as fw:
            await asyncio.sleep(fw.value + FLOOD_BUFFER)
            await update_progress(client, user_id, chat_id, step, "<b>⚠️ Rate limit hit. Retrying after delay...</b>")
            try:
                code = await temp_client.send_code(phone_number)
                state["data"]["client"] = temp_client
                state["data"]["phone"] = phone_number
                state["data"]["hash"] = code.phone_code_hash
                state["step"] = "WAITING_CODE"
                additional_text = "<b>📩 OTP Sent to your app! 📲</b>\n\nPlease open your Telegram app and copy the verification code.\n\n<b>Send it like this:</b> <code>12 345</code> or <code>1 2 3 4 5 6</code>\n\n<blockquote>Adding spaces helps prevent Telegram from deleting the message automatically. 💡</blockquote>"
                await update_progress(client, user_id, chat_id, "WAITING_CODE", additional_text)
            except Exception:
                await update_progress(client, user_id, chat_id, step, "<b>❌ Failed after retry. Please try later.</b>")
                await temp_client.disconnect()
                del LOGIN_STATE[user_id]
        except Exception as e:
            await update_progress(client, user_id, chat_id, step, f"<b>❌ Something went wrong: {str(e)} 🤔 Please try /login again.</b>")
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
    elif step == "WAITING_CODE":
        phone_code = text.replace(" ", "")
        if not phone_code.isdigit():
            await update_progress(client, user_id, chat_id, step, "<b>❌ Invalid code! Please send digits only (with spaces if needed).</b>")
            return
        temp_client = state["data"]["client"]
        phone_number = state["data"]["phone"]
        phone_hash = state["data"]["hash"]
        await update_progress(client, user_id, chat_id, step, "<b>🔍 Verifying code... 🔍</b>")
        state["anim_task"] = asyncio.create_task(animate_loading(client, user_id, chat_id))
        try:
            await temp_client.sign_in(phone_number=phone_number, phone_code_hash=phone_hash, phone_code=phone_code)
            await stop_animation(state["anim_task"])
            await finalize_login(client, user_id, chat_id, temp_client)
        except PhoneCodeInvalid:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, "<b>❌ Hmm, that code doesn't look right. 🔍 Please check and try again.</b>")
        except PhoneCodeExpired:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, "<b>⏰ Code has expired. ⏳ Please start over with /login.</b>")
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
        except SessionPasswordNeeded:
            await stop_animation(state["anim_task"])
            state["step"] = "WAITING_PASSWORD"
            additional_text = "<b>🔐 Two-Step Verification Detected 🔒</b>\n\nPlease enter your account <b>password</b>.\n\n<i>Take your time — it's secure! 🛡️</i>"
            await update_progress(client, user_id, chat_id, "WAITING_PASSWORD", additional_text)
        except FloodWait as fw:
            await stop_animation(state["anim_task"])
            await asyncio.sleep(fw.value + FLOOD_BUFFER)
            await update_progress(client, user_id, chat_id, step, "<b>⚠️ Rate limit hit. Retrying...</b>")
            try:
                await temp_client.sign_in(phone_number=phone_number, phone_code_hash=phone_hash, phone_code=phone_code)
                await finalize_login(client, user_id, chat_id, temp_client)
            except:
                await update_progress(client, user_id, chat_id, step, "<b>❌ Verification failed after retry.</b>")
                await temp_client.disconnect()
                del LOGIN_STATE[user_id]
        except Exception as e:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, f"<b>❌ Something went wrong: {str(e)} 🤔</b>")
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]
    elif step == "WAITING_PASSWORD":
        password = text
        temp_client = state["data"]["client"]
        await update_progress(client, user_id, chat_id, step, "<b>🔑 Checking password... 🔑</b>")
        state["anim_task"] = asyncio.create_task(animate_loading(client, user_id, chat_id))
        try:
            await temp_client.check_password(password=password)
            await stop_animation(state["anim_task"])
            await finalize_login(client, user_id, chat_id, temp_client)
        except PasswordHashInvalid:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, "<b>❌ Incorrect password. 🔑 Please try again.</b>")
        except FloodWait as fw:
            await stop_animation(state["anim_task"])
            await asyncio.sleep(fw.value + FLOOD_BUFFER)
            await update_progress(client, user_id, chat_id, step, "<b>⚠️ Rate limit hit. Retrying...</b>")
            try:
                await temp_client.check_password(password=password)
                await finalize_login(client, user_id, chat_id, temp_client)
            except:
                await update_progress(client, user_id, chat_id, step, "<b>❌ Password check failed after retry.</b>")
                await temp_client.disconnect()
                del LOGIN_STATE[user_id]
        except Exception as e:
            await stop_animation(state["anim_task"])
            await update_progress(client, user_id, chat_id, step, f"<b>❌ Something went wrong: {str(e)} 🤔</b>")
            await temp_client.disconnect()
            del LOGIN_STATE[user_id]

async def finalize_login(client: Client, user_id: int, chat_id: int, temp_client):
    try:
        session_string = await temp_client.export_session_string()
        await temp_client.disconnect()
        await db.set_session(user_id, session=session_string)
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]
        await update_progress(client, user_id, chat_id, "COMPLETE", "<b>🎉 Login Successful! 🌟</b>\n\n<i>Your session has been saved securely. 🔒</i>\n\nYou can now use all features! 🚀")
        await client.send_message(chat_id, " ", reply_markup=remove_keyboard)
    except Exception as e:
        await update_progress(client, user_id, chat_id, "WAITING_PASSWORD", f"<b>❌ Failed to save session: {str(e)} 😔</b>\n\nPlease try /login again.")
        if user_id in LOGIN_STATE:
            del LOGIN_STATE[user_id]

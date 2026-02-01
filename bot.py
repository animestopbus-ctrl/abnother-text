import asyncio
import datetime
import sys
import os
from datetime import timezone, timedelta
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import Message, BotCommand
from pyrogram.errors import FloodWait, RPCError
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from database.db import db
from logger import LOGGER

# Keep-alive server (Render / Heroku)
try:
    from keep_alive import keep_alive
except ImportError:
    keep_alive = None

logger = LOGGER(__name__)
IST = timezone(timedelta(hours=5, minutes=30))

# Small cache for your ~200 users to prevent DB lag
USER_CACHE = set()

LOGO = r"""
  ██████╗  ██╗  ██╗  █████╗  ███╗   ██╗ ██████╗   █████╗  ██╗      
  ██╔══██╗ ██║  ██║ ██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗ ██║      
  ██║  ██║ ███████║ ███████║ ██╔██╗ ██║ ██████╔╝ ███████║ ██║      
  ██║  ██║ ██╔══██║ ██╔══██║ ██║╚██╗██║ ██╔═══╝  ██╔══██║ ██║      
  ██████╔╝ ██║  ██║ ██║  ██║ ██║ ╚████║ ██║      ██║  ██║ ███████
    𝙱𝙾𝚃 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝙿𝚁𝙾𝙿𝙴𝚁𝙻𝚈....
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Rexbots_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Rexbots"),
            workers=10, 
            sleep_threshold=15,
            max_concurrent_transmissions=5,
            ipv6=False,
            in_memory=False,
        )
        self._keep_alive_started = False

    async def start(self):
        print(LOGO)

        # 1. Start keep-alive BEFORE attempting Telegram login
        if keep_alive and not self._keep_alive_started:
            try:
                # Handle potential loop passing for different keep_alive implementations
                loop = asyncio.get_running_loop()
                try:
                    keep_alive(loop)
                except TypeError:
                    keep_alive()
                self._keep_alive_started = True
                logger.info("Keep-alive server started.")
            except Exception as e:
                logger.warning(f"Keep-alive failed: {e}")

        # 2. FIX FOR FLOOD WAIT: Resilient Login Loop
        while True:
            try:
                await super().start()
                break # Success!
            except FloodWait as e:
                wait_time = int(e.value) + 10
                logger.warning(f"FLOOD_WAIT detected during login. Sleeping for {wait_time}s before retrying...")
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Critical Startup Error: {e}")
                await asyncio.sleep(15) # Safety wait before retry

        me = await self.get_me()

        # 3. DB and Cache Validation
        try:
            user_count = await db.total_users_count()
            logger.info(f"MongoDB Connected: {user_count} users found.")
        except Exception as e:
            logger.error(f"DB stats failed: {e}")
            user_count = "Unknown"

        # 4. Startup notification
        now = datetime.datetime.now(IST)
        startup_text = (
            f"<b><i>🤖 Bot Successfully Started ♻️</i></b>\n\n"
            f"<b>Bot:</b> @{me.username}\n"
            f"<b>Users:</b> <code>{user_count} / 200</code>\n"
            f"<b>Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>Developed by @RexBots_Official</b>"
        )

        try:
            await self.send_message(LOG_CHANNEL, startup_text)
            logger.info("Startup log sent.")
        except Exception as e:
            logger.error(f"Failed to send startup log: {e}")

        await self.set_bot_commands_list()

    async def stop(self, *args):
        try:
            await self.send_message(LOG_CHANNEL, "<b><i>❌ Bot is going Offline</i></b>")
        except:
            pass
        # asyncio.shield prevents the shutdown from being cancelled mid-way
        await asyncio.shield(super().stop())
        logger.info("Bot stopped cleanly")

    async def set_bot_commands_list(self):
        commands = [
         import asyncio
import datetime
import sys
import os
from datetime import timezone, timedelta
from pyrogram import Client, filters, enums, **version** as pyrogram_version
from pyrogram.types import Message, BotCommand
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from database.db import db
from logger import LOGGER
# Keep-alive server setup for 24/7 hosting (Render / Heroku)
try:
    from keep_alive import keep_alive
except ImportError:
    keep_alive = None
logger = LOGGER(**name**)
IST = timezone(timedelta(hours=5, minutes=30))
# In-memory cache to prevent hitting the Database on every single message
USER_CACHE = set()
LOGO = r"""
  ██████╗ ██╗ ██╗ █████╗ ███╗ ██╗ ██████╗ █████╗ ██╗
  ██╔══██╗ ██║ ██║ ██╔══██╗ ████╗ ██║ ██╔══██╗ ██╔══██╗ ██║
  ██║ ██║ ███████║ ███████║ ██╔██╗ ██║ ██████╔╝ ███████║ ██║
  ██║ ██║ ██╔══██║ ██╔══██║ ██║╚██╗██║ ██╔═══╝ ██╔══██║ ██║
  ██████╔╝ ██║ ██║ ██║ ██║ ██║ ╚████║ ██║ ██║ ██║ ███████
    𝙱𝙾𝚃 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝙿𝚁𝙾𝙿𝙴𝚁𝙻𝚈....
"""
class Bot(Client):
    def **init**(self):
        super().**init**(
            name="Rexbots_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Rexbots"),
            workers=50, # Optimized for high-volume message handling
            sleep_threshold=15,
            max_concurrent_transmissions=10,
            ipv6=False,
            in_memory=False,
        )
        self._keep_alive_started = False
    async def start(self):
        print(LOGO)
        # 1. Start Keep-Alive Server
        if keep_alive and not self._keep_alive_started:
            try:
                loop = asyncio.get_running_loop()
                try:
                    keep_alive(loop)
                except TypeError:
                    keep_alive()
                self._keep_alive_started = True
                logger.info("Keep-alive server started successfully.")
            except Exception as e:
                logger.warning(f"Keep-alive failed to start: {e}", exc_info=True)
        # 2. Resilient Startup with Exponential Backoff & FloodWait Handling
        retry_delay = 10
        while True:
            try:
                await super().start()
                break
            except FloodWait as e:
                wait_time = int(e.value) + 10
                logger.warning(f"Telegram FloodWait hit during startup. Sleeping for {wait_time}s")
                await asyncio.sleep(wait_time)
                retry_delay = 10
            except Exception as e:
                logger.error(f"Startup crash encountered: {e}", exc_info=True)
                logger.info(f"Retrying connection in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay + 10, 60) # Capped at 1 minute
        me = await self.get_me()
        # 3. Database & Stats Logging
        try:
            user_count = await db.total_users_count()
            db_name = getattr(db.db, 'name', 'unknown')
            logger.info(f"Connected to MongoDB: {db_name} | Users: {user_count}")
        except Exception as e:
            logger.error(f"Failed to fetch DB statistics: {e}", exc_info=True)
            user_count = "Error"
        # 4. Cache Log Channel & Validate Permissions
        try:
            await self.get_chat(LOG_CHANNEL)
            logger.info(f"Log Channel Access Verified: {LOG_CHANNEL}")
        except Exception as e:
            logger.warning(f"Could not verify access to LOG_CHANNEL: {e}")
        # 5. Build Comprehensive Startup Notification
        now = datetime.datetime.now(IST)
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        startup_text = (
            f"<b><i>🤖 Bot Successfully Started ♻️</i></b>\n\n"
            f"<b>Bot Name:</b> @{me.username}\n"
            f"<b>Bot ID:</b> <code>{me.id}</code>\n\n"
            f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
            f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>🐍 Python:</b> <code>{py_ver}</code>\n"
            f"<b>🔥 Pyrogram:</b> <code>{pyrogram_version}</code>\n"
            f"<b>🚀 Speed Mode:</b> <code>Enabled (50 Workers)</code>\n\n"
            f"<b>👥 Total Users:</b> <code>{user_count}</code>\n\n"
            f"<b>Developed by @RexBots_Official</b>"
        )
        try:
            await self.send_message(
                LOG_CHANNEL,
                startup_text,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info("Startup log notification sent.")
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
        logger.info(f"Bot session active as @{me.username}")
        await self.set_bot_commands_menu()
    async def stop(self, *args):
        # Notify of shutdown before breaking connection
        try:
            me = await self.get_me()
            now = datetime.datetime.now(IST)
            stop_text = (
                f"<b><i>❌ Bot @{me.username} Stopped</i></b>\n\n"
                f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
                f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
                f"<b>Status:</b> <code>Bot Offline</code>"
            )
            await self.send_message(LOG_CHANNEL, stop_text, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            logger.error(f"Could not send stop log: {e}")
        # CRITICAL: Shield ensures shutdown logic finishes without being cancelled
        try:
            await asyncio.shield(super().stop())
        except Exception as e:
            logger.error(f"Error during core shutdown: {e}")
        logger.info("Bot execution terminated cleanly.")
    async def set_bot_commands_menu(self):
        # Detailed command list for the Telegram Menu
        commands = [
            BotCommand("start", "Initialize the bot"),
            BotCommand("help", "Show help and guidance"),
            BotCommand("settings", "Configure bot preferences"),
            BotCommand("commands", "List all available features"),
            BotCommand("login", "Authorize your account"),
            BotCommand("logout", "Revoke account access"),
            BotCommand("cancel", "Abort current process"),
            BotCommand("myplan", "Check subscription status"),
            BotCommand("premium", "Explore premium tiers"),
            BotCommand("setchat", "Configure dump chat ID"),
            BotCommand("set_thumb", "Upload custom thumbnail"),
            BotCommand("view_thumb", "View current thumbnail"),
            BotCommand("del_thumb", "Delete saved thumbnail"),
            BotCommand("set_caption", "Set custom file caption"),
            BotCommand("see_caption", "Preview active caption"),
            BotCommand("del_caption", "Remove active caption"),
            BotCommand("set_del_word", "Add words to removal list"),
            BotCommand("rem_del_word", "Remove words from removal list"),
            BotCommand("set_repl_word", "Set word replacement rules"),
            BotCommand("rem_repl_word", "Remove replacement rules")
        ]
        # Use Client's native method
        await super().set_bot_commands(commands)
        logger.info("Command menu synchronization complete.")
BotInstance = Bot()
# --- HANDLERS ---
@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def handle_new_users(bot: Client, message: Message):
    """
    Middleware to auto-register users.
    Optimized with USER_CACHE to prevent unnecessary DB hits.
    """
    user = message.from_user
    if not user or user.id in USER_CACHE:
        return
    try:
        # Check database if not in session cache
        if not await db.is_user_exist(user.id):
            await db.add_user(user.id, user.first_name)
           
            # Log the new user to the log channel
            now = datetime.datetime.now(IST)
            username_link = f"@{user.username}" if user.username else "<i>None</i>"
            log_text = (
                f"<b><i>#NewUser 👤 Joined the Bot</i></b>\n\n"
                f"<b>User:</b> {user.mention}\n"
                f"<b>Username:</b> {username_link}\n"
                f"<b>User ID:</b> <code>{user.id}</code>\n\n"
                f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
                f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
                f"<b>Developed by @RexBots_Official</b>"
            )
            try:
                await bot.send_message(LOG_CHANNEL, log_text, parse_mode=enums.ParseMode.HTML)
            except:
                pass
           
            logger.info(f"Registered new user: {user.id}")
       
        # Add to session cache
        USER_CACHE.add(user.id)
       
    except Exception as e:
        logger.error(f"Error in user registration middleware: {e}", exc_info=True)
@BotInstance.on_message(filters.command("cmd") & filters.user(ADMINS))
async def update_commands_handler(bot: Client, message: Message):
    """Admin command to manually refresh the bot menu."""
    try:
        await bot.set_bot_commands_menu()
        await message.reply_text("✅ <b>Bot commands menu updated successfully!</b>", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        logger.error(f"Admin /cmd failed: {e}")
        await message.reply_text(f"❌ <b>Failed to update commands:</b>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)
if **name** == "**main**":
    BotInstance.run() suggestuonsHere are concise, practical suggestions for your bot code (focused on 2025–2026 realities):
Security / Privacy

Remove user.mention from logs → can leak full name + link in public channels
Never log first_name + username together in same message
Consider hashing user IDs before logging if channel is not 100% private

Performance / Reliability

USER_CACHE = set() → will grow forever → use cachetools TTLCache (or dict + periodic cleanup)
50 workers is usually overkill on Render/Heroku free & low tiers → start with 8–16
max_concurrent_transmissions=10 → good, but test real upload/download speed

Code quality / Maintainability

Move set_bot_commands_menu() call to start() (you already do — good)
Replace many try: … except: pass and except Exception → catch specific errors (FloodWait, ChatWriteForbidden, etc.)
Use constants for repeated strings (IST timedelta, date formats, HTML tags)

Modern Pyrogram / Python improvements
Python# Better way (Pyrogram ≥2.0 style)
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

# Cleaner datetime usage
now = datetime.now(IST)
date_str = now.strftime("%d %b %Y")
time_str = now.strftime("%I:%M %p IST")
Small but useful changes

Add filters.command("start", prefixes=["/", "!"]) (support both /start and !start)
Use message.reply("text", quote=True) in most admin/private replies
Consider on_raw_update for very high load instead of on_message everywhere
Add graceful shutdown handler (catch SIGTERM / SIGINT)

Quick refactor example (user registration part)
Python@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def register_middleware(client: Client, msg: Message):
    user = msg.from_user
    if not user or user.id in USER_CACHE:
        return

    if await db.is_user_exist(user.id):
        USER_CACHE.add(user.id)
        return

    await db.add_user(user.id, user.first_name)
    USER_CACHE.add(user.id)

    if not LOG_CHANNEL:
        return

    text = (
        "🆕 <b>New User</b>\n"
        f"• ID: <code>{user.id}</code>\n"
        f"• {datetime.now(IST).strftime('%d %b %Y  %I:%M %p IST')}"
    )
    try:
        await client.send_message(LOG_CHANNEL, text, parse_mode=enums.ParseMode.HTML)
    except:
        pass
Most important 5 things to fix/do next (priority order):

Replace broad except Exception → catch concrete errors
Limit / clean USER_CACHE (add TTL or max size)
Stop logging full names in public/log channels
Reduce workers to 12–16 if hosted on free/low tier
Add proper signal handling for clean shutdown

Which area bothers you most right now (performance, errors, logs, security, something else)?Executed codefix th bus import asyncio
import datetime
import sys
import os
from datetime import timezone, timedelta
from pyrogram import Client, filters, enums, **version** as pyrogram_version
from pyrogram.types import Message, BotCommand
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from database.db import db
from logger import LOGGER
# Keep-alive server setup for 24/7 hosting (Render / Heroku)
try:
    from keep_alive import keep_alive
except ImportError:
    keep_alive = None
logger = LOGGER(**name**)
IST = timezone(timedelta(hours=5, minutes=30))
# In-memory cache to prevent hitting the Database on every single message
USER_CACHE = set()
LOGO = r"""
  ██████╗ ██╗ ██╗ █████╗ ███╗ ██╗ ██████╗ █████╗ ██╗
  ██╔══██╗ ██║ ██║ ██╔══██╗ ████╗ ██║ ██╔══██╗ ██╔══██╗ ██║
  ██║ ██║ ███████║ ███████║ ██╔██╗ ██║ ██████╔╝ ███████║ ██║
  ██║ ██║ ██╔══██║ ██╔══██║ ██║╚██╗██║ ██╔═══╝ ██╔══██║ ██║
  ██████╔╝ ██║ ██║ ██║ ██║ ██║ ╚████║ ██║ ██║ ██║ ███████
    𝙱𝙾𝚃 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 𝙿𝚁𝙾𝙿𝙴𝚁𝙻𝚈....
"""
class Bot(Client):
    def **init**(self):
        super().**init**(
            name="Rexbots_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Rexbots"),
            workers=50, # Optimized for high-volume message handling
            sleep_threshold=15,
            max_concurrent_transmissions=10,
            ipv6=False,
            in_memory=False,
        )
        self._keep_alive_started = False
    async def start(self):
        print(LOGO)
        # 1. Start Keep-Alive Server
        if keep_alive and not self._keep_alive_started:
            try:
                loop = asyncio.get_running_loop()
                try:
                    keep_alive(loop)
                except TypeError:
                    keep_alive()
                self._keep_alive_started = True
                logger.info("Keep-alive server started successfully.")
            except Exception as e:
                logger.warning(f"Keep-alive failed to start: {e}", exc_info=True)
        # 2. Resilient Startup with Exponential Backoff & FloodWait Handling
        retry_delay = 10
        while True:
            try:
                await super().start()
                break
            except FloodWait as e:
                wait_time = int(e.value) + 10
                logger.warning(f"Telegram FloodWait hit during startup. Sleeping for {wait_time}s")
                await asyncio.sleep(wait_time)
                retry_delay = 10
            except Exception as e:
                logger.error(f"Startup crash encountered: {e}", exc_info=True)
                logger.info(f"Retrying connection in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay + 10, 60) # Capped at 1 minute
        me = await self.get_me()
        # 3. Database & Stats Logging
        try:
            user_count = await db.total_users_count()
            db_name = getattr(db.db, 'name', 'unknown')
            logger.info(f"Connected to MongoDB: {db_name} | Users: {user_count}")
        except Exception as e:
            logger.error(f"Failed to fetch DB statistics: {e}", exc_info=True)
            user_count = "Error"
        # 4. Cache Log Channel & Validate Permissions
        try:
            await self.get_chat(LOG_CHANNEL)
            logger.info(f"Log Channel Access Verified: {LOG_CHANNEL}")
        except Exception as e:
            logger.warning(f"Could not verify access to LOG_CHANNEL: {e}")
        # 5. Build Comprehensive Startup Notification
        now = datetime.datetime.now(IST)
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        startup_text = (
            f"<b><i>🤖 Bot Successfully Started ♻️</i></b>\n\n"
            f"<b>Bot Name:</b> @{me.username}\n"
            f"<b>Bot ID:</b> <code>{me.id}</code>\n\n"
            f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
            f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
            f"<b>🐍 Python:</b> <code>{py_ver}</code>\n"
            f"<b>🔥 Pyrogram:</b> <code>{pyrogram_version}</code>\n"
            f"<b>🚀 Speed Mode:</b> <code>Enabled (50 Workers)</code>\n\n"
            f"<b>👥 Total Users:</b> <code>{user_count}</code>\n\n"
            f"<b>Developed by @RexBots_Official</b>"
        )
        try:
            await self.send_message(
                LOG_CHANNEL,
                startup_text,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info("Startup log notification sent.")
        except Exception as e:
            logger.error(f"Failed to send startup message: {e}")
        logger.info(f"Bot session active as @{me.username}")
        await self.set_bot_commands_menu()
    async def stop(self, *args):
        # Notify of shutdown before breaking connection
        try:
            me = await self.get_me()
            now = datetime.datetime.now(IST)
            stop_text = (
                f"<b><i>❌ Bot @{me.username} Stopped</i></b>\n\n"
                f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
                f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
                f"<b>Status:</b> <code>Bot Offline</code>"
            )
            await self.send_message(LOG_CHANNEL, stop_text, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            logger.error(f"Could not send stop log: {e}")
        # CRITICAL: Shield ensures shutdown logic finishes without being cancelled
        try:
            await asyncio.shield(super().stop())
        except Exception as e:
            logger.error(f"Error during core shutdown: {e}")
        logger.info("Bot execution terminated cleanly.")
    async def set_bot_commands_menu(self):
        # Detailed command list for the Telegram Menu
        commands = [
            BotCommand("start", "Initialize the bot"),
            BotCommand("help", "Show help and guidance"),
            BotCommand("settings", "Configure bot preferences"),
            BotCommand("commands", "List all available features"),
            BotCommand("login", "Authorize your account"),
            BotCommand("logout", "Revoke account access"),
            BotCommand("cancel", "Abort current process"),
            BotCommand("myplan", "Check subscription status"),
            BotCommand("premium", "Explore premium tiers"),
            BotCommand("setchat", "Configure dump chat ID"),
            BotCommand("set_thumb", "Upload custom thumbnail"),
            BotCommand("view_thumb", "View current thumbnail"),
            BotCommand("del_thumb", "Delete saved thumbnail"),
            BotCommand("set_caption", "Set custom file caption"),
            BotCommand("see_caption", "Preview active caption"),
            BotCommand("del_caption", "Remove active caption"),
            BotCommand("set_del_word", "Add words to removal list"),
            BotCommand("rem_del_word", "Remove words from removal list"),
            BotCommand("set_repl_word", "Set word replacement rules"),
            BotCommand("rem_repl_word", "Remove replacement rules")
        ]
        # Use Client's native method
        await super().set_bot_commands(commands)
        logger.info("Command menu synchronization complete.")
BotInstance = Bot()
# --- HANDLERS ---
@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def handle_new_users(bot: Client, message: Message):
    """
    Middleware to auto-register users.
    Optimized with USER_CACHE to prevent unnecessary DB hits.
    """
    user = message.from_user
    if not user or user.id in USER_CACHE:
        return
    try:
        # Check database if not in session cache
        if not await db.is_user_exist(user.id):
            await db.add_user(user.id, user.first_name)
           
            # Log the new user to the log channel
            now = datetime.datetime.now(IST)
            username_link = f"@{user.username}" if user.username else "<i>None</i>"
            log_text = (
                f"<b><i>#NewUser 👤 Joined the Bot</i></b>\n\n"
                f"<b>User:</b> {user.mention}\n"
                f"<b>Username:</b> {username_link}\n"
                f"<b>User ID:</b> <code>{user.id}</code>\n\n"
                f"<b>📅 Date:</b> <code>{now.strftime('%d %B %Y')}</code>\n"
                f"<b>🕒 Time:</b> <code>{now.strftime('%I:%M %p')} IST</code>\n\n"
                f"<b>Developed by @RexBots_Official</b>"
            )
            try:
                await bot.send_message(LOG_CHANNEL, log_text, parse_mode=enums.ParseMode.HTML)
            except:
                pass
           
            logger.info(f"Registered new user: {user.id}")
       
        # Add to session cache
        USER_CACHE.add(user.id)
       
    except Exception as e:
        logger.error(f"Error in user registration middleware: {e}", exc_info=True)
@BotInstance.on_message(filters.command("cmd") & filters.user(ADMINS))
async def update_commands_handler(bot: Client, message: Message):
    """Admin command to manually refresh the bot menu."""
    try:
        await bot.set_bot_commands_menu()
        await message.reply_text("✅ <b>Bot commands menu updated successfully!</b>", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        logger.error(f"Admin /cmd failed: {e}")
        await message.reply_text(f"❌ <b>Failed to update commands:</b>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)
if **name** == "**main**":
    BotInstance.run()Here are the fixed and improved parts of your code with the most important corrections and cleanups:
Pythonimport asyncio
import datetime
import sys
import os
from datetime import timezone, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, BotCommand
from pyrogram.errors import FloodWait, ChatWriteForbidden
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
from database.db import db
from logger import LOGGER

# Keep-alive server setup (Render / Heroku)
try:
    from keep_alive import keep_alive
except ImportError:
    keep_alive = None

logger = LOGGER(__name__)

IST = timezone(timedelta(hours=5, minutes=30))

# Better: use a dict or cachetools.TTLCache instead of unlimited set
USER_CACHE: set[int] = set()

# Optional: smaller, cleaner logo
LOGO = """
╔════════════════════════════╗
║     Rexbots Login Bot      ║
║     WORKING PROPERLY       ║
╚════════════════════════════╝
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Rexbots_Login_Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="Rexbots"),
            workers=16,                    # ← reduced (safer for most hosts)
            sleep_threshold=15,
            max_concurrent_transmissions=8,
            ipv6=False,
            in_memory=False,
        )
        self._keep_alive_started = False

    async def start(self):
        print(LOGO)

        # Start keep-alive
        if keep_alive and not self._keep_alive_started:
            try:
                loop = asyncio.get_running_loop()
                try:
                    keep_alive(loop)
                except TypeError:
                    keep_alive()
                self._keep_alive_started = True
                logger.info("Keep-alive server started")
            except Exception as e:
                logger.warning(f"Keep-alive failed: {e}")

        # Resilient startup
        retry_delay = 10
        while True:
            try:
                await super().start()
                break
            except FloodWait as e:
                wait = int(e.value) + 10
                logger.warning(f"FloodWait: sleeping {wait}s")
                await asyncio.sleep(wait)
                retry_delay = 10
            except Exception as e:
                logger.error(f"Startup error: {e}", exc_info=True)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay + 10, 60)

        me = await self.get_me()

        # Database stats
        try:
            user_count = await db.total_users_count()
            logger.info(f"MongoDB connected | Users: {user_count}")
        except Exception as e:
            logger.error(f"DB stats failed: {e}")
            user_count = "Error"

        # Log channel check
        try:
            await self.get_chat(LOG_CHANNEL)
            logger.info(f"Log channel access OK: {LOG_CHANNEL}")
        except Exception as e:
            logger.warning(f"Log channel check failed: {e}")

        # Startup message
        now = datetime.datetime.now(IST)
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        startup_text = (
            f"<b>🤖 Bot Started</b>\n\n"
            f"Name: @{me.username}\n"
            f"ID: <code>{me.id}</code>\n\n"
            f"Date: {now.strftime('%d %b %Y')}\n"
            f"Time: {now.strftime('%I:%M %p')} IST\n\n"
            f"Python: {py_ver}\n"
            f"Pyrogram: {Client.pyrogram_version}\n"  # ← corrected access
            f"Workers: 16\n"
            f"Users: {user_count}\n\n"
            f"Developed by @RexBots_Official"
        )

        try:
            await self.send_message(
                LOG_CHANNEL,
                startup_text,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
        except (ChatWriteForbidden, Exception) as e:
            logger.error(f"Failed to send startup message: {e}")

        logger.info(f"Bot active as @{me.username}")
        await self.set_bot_commands_menu()

    async def stop(self, *args):
        try:
            me = await self.get_me()
            now = datetime.datetime.now(IST)
            stop_text = (
                f"<b>❌ Bot @{me.username} Stopped</b>\n\n"
                f"Date: {now.strftime('%d %b %Y')}\n"
                f"Time: {now.strftime('%I:%M %p')} IST\n"
                f"Status: Offline"
            )
            await self.send_message(LOG_CHANNEL, stop_text, parse_mode=enums.ParseMode.HTML)
        except Exception:
            pass

        try:
            await asyncio.shield(super().stop())
        except Exception as e:
            logger.error(f"Shutdown error: {e}")

        logger.info("Bot stopped cleanly")

    async def set_bot_commands_menu(self):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help"),
            BotCommand("login", "Login"),
            BotCommand("logout", "Logout"),
            BotCommand("cancel", "Cancel current action"),
            BotCommand("myplan", "Check your plan"),
            BotCommand("premium", "Premium info"),
            BotCommand("setchat", "Set target chat"),
            BotCommand("set_thumb", "Set thumbnail"),
            BotCommand("view_thumb", "View thumbnail"),
            BotCommand("del_thumb", "Delete thumbnail"),
            BotCommand("set_caption", "Set caption"),
            BotCommand("see_caption", "View caption"),
            BotCommand("del_caption", "Delete caption"),
            BotCommand("set_del_word", "Add delete word"),
            BotCommand("rem_del_word", "Remove delete word"),
            BotCommand("set_repl_word", "Add replace word"),
            BotCommand("rem_repl_word", "Remove replace word"),
        ]
        await self.set_bot_commands(commands)

BotInstance = Bot()

# ── LOGIC FLOW ──────────────────────────────────────────────────────────────



# ── NEW USER REGISTRATION (OPTIMIZED) ───────────────────────────────────────

@BotInstance.on_message(filters.private & filters.incoming, group=-1)
async def new_user_log(bot: Client, message: Message):
    user = message.from_user
    if not user or user.id in USER_CACHE:
        return

    # Check database only if not in local cache
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        
        now = datetime.datetime.now(IST)
        log_text = (
            f"<b>#NewUser 👤</b>\n"
            f"<b>User:</b> {user.mention}\n"
            f"<b>ID:</b> <code>{user.id}</code>\n"
            f"<b>Time:</b> {now.strftime('%I:%M %p')} IST"
        )
        try:
            await bot.send_message(LOG_CHANNEL, log_text)
        except:
            pass
    
    # Cache the ID to prevent future DB hits during this session
    USER_CACHE.add(user.id)

@BotInstance.on_message(filters.command("cmd") & filters.user(ADMINS))
async def update_commands(bot: Client, message: Message):
    try:
        await bot.set_bot_commands_list()
        await message.reply_text("✅ Commands menu updated!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    BotInstance.run()

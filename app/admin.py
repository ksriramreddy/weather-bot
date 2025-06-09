from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv
import os
from app import database
load_dotenv()

async def block(update : Update, context : ContextTypes.DEFAULT_TYPE):
    if update.effective_user != os.getenv("ADMIN_ID"):
        await update.message.reply_text(
            f"Your not allowd to use this command"
        )
        return
    if not context.args:
        await update.message.reply_text(
            f"Use /block <telegram_id> properly"
        )
        return
    database.block_user(int(context.args[0]))
    await update.message.reply_text(
        f"User blocked Successfully"
    )


async def unblock(update : Update, context : ContextTypes.DEFAULT_TYPE):
    if update.effective_user != os.getenv("ADMIN_ID"):
        await update.message.reply_text(
            f"Your not allowd to use this command"
        )
        return
    if not context.args:
        await update.message.reply_text(
            f"Use /block <telegram_id> properly"
        )
        return
    database.block_user(int(context.args[0]))
    await update.message.reply_text(
        f"User Unblocked Successfully"
    )
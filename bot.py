from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = "7961954465:AAGiBRXZp4OZDGf3uSD5RCfeJD0Al3ljpjQ"
ADMIN_ID = 6126776672
CHANNEL_USERNAME = "@pwdiscounthelper"

users = set()
coupon_code = "ATULPW10"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if member.status not in ["member", "administrator", "creator"]:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ I Joined", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️ Please join our channel first to get coupon.",
            reply_markup=reply_markup
        )
        return

    await send_main_menu(update, context)

async def send_main_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("🎟 Get Coupon", callback_data="coupon")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 Welcome to PW Discount Helper Bot!\nChoose option:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    await query.answer()

    if query.data == "check_join":
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text("✅ Verified Successfully!")
            await send_main_menu(update, context)
        else:
            await query.answer("❌ You still haven't joined!", show_alert=True)

    if query.data == "coupon":
        await query.edit_message_text(
            f"🎉 Use Code: {coupon_code}\nApply on PW website and enjoy discount!"
        )

async def setcoupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global coupon_code
    if update.effective_user.id == ADMIN_ID:
        if context.args:
            coupon_code = context.args[0]
            await update.message.reply_text("✅ Coupon Updated!")
        else:
            await update.message.reply_text("Usage: /setcoupon NEWCODE")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        message = " ".join(context.args)
        for user_id in users:
            try:
                await context.bot.send_message(user_id, message)
            except:
                pass
        await update.message.reply_text("✅ Broadcast Sent!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setcoupon", setcoupon))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()

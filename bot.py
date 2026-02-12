from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# ===== SETTINGS =====
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")


# Default Coupons
coupons = {
    "neet": "ATUPAN0001",
    "jee": "ATUPAN0001",
    "foundation": "ATUPAN0001",
    "gate": "ATUPAN0001"
}

users = set()

# ===== MAIN MENU =====
async def main_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("🎓 Get Course Coupon", callback_data="select_course")],
        [InlineKeyboardButton("ℹ️ About Us", callback_data="about")],
        [InlineKeyboardButton("❌ Exit", callback_data="exit")]
    ]

    if update.effective_user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("⚙ Admin Panel", callback_data="admin")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🔥 *PW Discount Helper*\n"
        "_India’s Smartest Savings Bot_\n\n"
        "🎯 Get Course-Wise Verified Coupons\n"
        "💰 Maximize Your Savings Today!"
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if member.status not in ["member", "administrator", "creator"]:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ I Joined", callback_data="check_join")]
        ]
        await update.message.reply_text(
            "⚠️ Please join our channel to access coupons.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await main_menu(update, context)

# ===== BUTTON HANDLER =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "check_join":
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
        if member.status in ["member", "administrator", "creator"]:
            await main_menu(update, context)
        else:
            await query.answer("❌ Join channel first!", show_alert=True)

    elif query.data == "select_course":
        keyboard = [
            [InlineKeyboardButton("🩺 NEET", callback_data="neet")],
            [InlineKeyboardButton("🧮 JEE", callback_data="jee")],
            [InlineKeyboardButton("📘 Foundation", callback_data="foundation")],
            [InlineKeyboardButton("🎓 GATE", callback_data="gate")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await query.edit_message_text(
            "🎓 Select Your Course:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data in coupons:
        course = query.data
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="select_course")]]

        await query.edit_message_text(
            f"🎉 *Your Coupon Code*\n\n"
            f"📚 Course: {course.upper()}\n"
            f"🎟 Code: `{coupons[course]}`\n\n"
            f"💰 Apply during checkout & save big!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "about":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
        await query.edit_message_text(
            "🔥 PW Discount Helper\n\n"
            "🎯 Course-wise coupons\n"
            "💰 Verified savings\n"
            "🚀 Fast & Reliable",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "admin" and user.id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("👥 User Count", callback_data="user_count")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        await query.edit_message_text(
            "⚙ Admin Panel",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "user_count" and user.id == ADMIN_ID:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin")]]
        await query.edit_message_text(
            f"👥 Total Users: {len(users)}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "back":
        await main_menu(update, context)

    elif query.data == "exit":
        await query.edit_message_text(
            "👋 Session Closed.\nType /start to begin again."
        )

# ===== RUN =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()



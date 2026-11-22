
import os
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")

keyboard = [
    ["🔎 Kino qidirish", "⭐ Mashhur kinolar"],
    ["🎞 Janrlar", "ℹ️ Bot haqida"],
]

menu = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["searching"] = False

    await update.message.reply_text(
        "🎬 CineVerse 2.0 botiga xush kelibsiz!\n\n"
        "🍿 Kerakli bo‘limni tanlang:",
        reply_markup=menu
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔎 Kino qidirish":
        context.user_data["searching"] = True
        await update.message.reply_text(
            "🔎 Kino nomini yozing!"
        )

    elif text == "⭐ Mashhur kinolar":
        await update.message.reply_text(
            "⭐ Mashhur kinolar bo‘limi tez orada!"
        )

    elif text == "🎞 Janrlar":
        await update.message.reply_text(
            "🎞 Janrlar:\n"
            "• Jangari\n"
            "• Komediya\n"
            "• Sarguzasht\n"
            "• Fantastika\n"
            "• Drama"
        )

    elif text == "ℹ️ Bot haqida":
        await update.message.reply_text(
            "🎬 CineVerse 2.0\n"
            "Kino ma’lumotlari va treylerlar boti!"
        )

    elif context.user_data.get("searching"):
        context.user_data["searching"] = False
        await update.message.reply_text(
            f"🔎 Siz qidirgan kino: {text}\n\n"
            "Kino qidirish xizmati tez orada ulanadi."
        )

    else:
        await update.message.reply_text(
            "🍿 Menyudan kerakli bo‘limni tanlang.",
            reply_markup=menu
        )


def main():
    if not TOKEN:
        raise RuntimeError("TOKEN topilmadi! Render Environment ni tekshiring.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, buttons)
    )

    print("🎬 CineVerse 2.0 ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()

import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# TOKEN من Render
TOKEN = os.getenv("BOT_TOKEN")

SUPPORT_NUMBER = "+212614055191"
SUPPORT_LINK = "https://t.me/Texas4WinMoRoCCo"

# أزرار القائمة
keyboard = [
    ["📌 التسجيل", "💳 الإيداع"],
    ["💸 السحب", "📞 الدعم"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# AI Logic بسيط
def ai_response(text: str):
    text = text.lower()

    if "تسجيل" in text or "register" in text:
        return "📌 باش تسجل:\nدخل للموقع واضغط Sign Up وعمر المعلومات ديالك."

    elif "إيداع" in text or "deposit" in text:
        return "💳 طرق الإيداع:\nتحويل بنكي أو محفظة إلكترونية.\nإذا واجهت مشكل تواصل مع الدعم."

    elif "سحب" in text or "withdraw" in text:
        return "💸 السحب كيتم بين 24 و72 ساعة حسب طريقة السحب."

    elif "مشكل" in text or "problem" in text:
        return "⚠️ إلى كان عندك مشكل، تواصل مع الدعم مباشرة."

    elif "دعم" in text or "support" in text:
        return f"📞 رقم الدعم: {SUPPORT_NUMBER}"

    else:
        return "🤖 ما فهمتش السؤال مزيان.\nاستعمل الأزرار أو تواصل مع الدعم."

# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا بك في AI Support Bot\n\n"
        "💡 كتب السؤال ديالك أو استعمل الأزرار:",
        reply_markup=reply_markup
    )

# التعامل مع الرسائل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = ai_response(text)

    await update.message.reply_text(response)

    await send_support(update)

# إرسال أزرار الدعم
async def send_support(update: Update):

    buttons = [
        [InlineKeyboardButton("📞 تواصل عبر تيليجرام", url=SUPPORT_LINK)],
        [InlineKeyboardButton("💬 رقم الهاتف", callback_data="phone")]
    ]

    await update.message.reply_text(
        "👇 إذا بغيتي مساعدة مباشرة:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback للأزرار
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "phone":
        await query.edit_message_text(f"📞 رقم الدعم:\n{SUPPORT_NUMBER}")

# تشغيل البوت
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.add_handler(CallbackQueryHandler(callback))

    print("Bot started...")

    app.run_polling()

if __name__ == "__main__":
    main()

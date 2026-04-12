from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8346804559:AAHnlhrAH6FR2hVY--mrbh3sQ5flPi_Aodw"
SUPPORT_NUMBER = "+212614055191"
SUPPORT_LINK = "https://t.me/Texas4WinMoRoCCo"

keyboard = [
    ["📌 التسجيل", "💳 الإيداع"],
    ["💸 السحب", "📞 الدعم"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🧠 SIMPLE AI LOGIC
def ai_response(text: str):
    text = text.lower()

    # تسجيل
    if "تسجيل" in text or "register" in text:
        return "📌 باش تسجل: دخل للموقع واضغط Sign Up وعمر البيانات ديالك."

    # إيداع
    elif "إيداع" in text or "deposit" in text:
        return "💳 طرق الإيداع: تحويل بنكي أو محفظة إلكترونية. أي مشكل تواصل مع الدعم."

    # سحب
    elif "سحب" in text or "withdraw" in text:
        return "💸 السحب كيتم بين 24 و72 ساعة حسب الطريقة."

    # مشاكل
    elif "مشكل" in text or "problem" in text:
        return "⚠️ رجاءً تواصل مع الدعم مباشرة لحل المشكل ديالك."

    # دعم
    elif "دعم" in text or "support" in text:
        return f"📞 الدعم: {SUPPORT_NUMBER}"

    # default
    else:
        return "🤖 ما فهمتش السؤال مزيان.\nاستعمل الأزرار أو تواصل مع الدعم."

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا بك في *AI Support Bot*\n\n"
        "💡 كتب سؤالك مباشرة أو استعمل الأزرار:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 🧠 MESSAGE HANDLER (AI)
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # إذا ضغط زر
    if text in ["📌 التسجيل", "💳 الإيداع", "💸 السحب", "📞 الدعم"]:
        response = ai_response(text)
    else:
        response = ai_response(text)

    await update.message.reply_text(response)

    # زر الدعم دائماً
    await send_support(update)

# 🔘 SUPPORT BUTTONS
async def send_support(update: Update):
    buttons = [
        [InlineKeyboardButton("📞 اتصال مباشر", url=SUPPORT_LINK)],
        [InlineKeyboardButton("💬 رقم الهاتف", callback_data="phone")]
    ]

    await update.message.reply_text(
        "👇 إذا بغيتي مساعدة مباشرة:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 📲 CALLBACK
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "phone":
        await query.edit_message_text(f"📞 رقم الدعم: {SUPPORT_NUMBER}")

# 🚀 APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(CallbackQueryHandler(callback))

app.run_polling()

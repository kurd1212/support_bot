from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import datetime

TOKEN = "7585234219:AAG6iXxT8oL4ADLHKoxDUdOYWeVsBMGF5ME"  # استبدلها بتوكن البوت الخاص بك
SUPPORT_GROUP_ID = -1002258741658  # معرف مجموعة الدعم
IMAGE_URL = "https://imagizer.imageshack.com/img923/7157/wFqjdU.jpg"  # رابط صورة صالح 

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username or update.message.from_user.first_name
    welcome_text = (f"Hello Dear ~ @{username}!\n\n"
                    "Choose EGOS, and you will have a smart and trustworthy investment partner.\n"
                    "Start your intelligent financial journey today and create a brilliant future of wealth growth!")

    keyboard = [[InlineKeyboardButton("العربية", callback_data='lang_ar')],
                [InlineKeyboardButton("English", callback_data='lang_en')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.message.chat_id, 
        photo=IMAGE_URL, 
        caption=welcome_text
    )
    await context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="Please select your language:", 
        reply_markup=reply_markup
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


    user_id = query.from_user.id
    lang = "ar" if query.data == "lang_ar" else "en"
    user_states[user_id] = {"lang": lang, "state": "waiting"}

    buttons = [
        [("(قريبا) فتح التطبيق", "قريبا"), ("قناة تيليجرام", "https://t.me/EGOS_A")],
        [("فيسبوك", "https://www.facebook.com/share/1BkxU8zfxj/?mibextid=qi2Omg"), ("إنستغرام", "https://www.instagram.com/egosgrowth?igsh=NTF5ZTA0MmI1bXRt")],
        [("تيك توك", "https://www.tiktok.com/@egosgrowth?_t=ZS-8ubPLXoFvip&_r=1"), ("X", "https://x.com/EgosGrowth?t=B43oMvzvu0JHD4E4RQusGg&s=09")],
        [("📞 تواصل مع الدعم", "contact_support")]
    ] if lang == "ar" else [
        [("Open App (Soon)", "Soon"), ("Telegram Channel", "https://t.me/EGOS_A")],
        [("Facebook", "https://www.facebook.com/share/1BkxU8zfxj/?mibextid=qi2Omg"), ("Instagram", "https://www.instagram.com/egosgrowth?igsh=NTF5ZTA0MmI1bXRt")],
        [("Tiktok", "https://www.tiktok.com/@egosgrowth?_t=ZS-8ubPLXoFvip&_r=1"), ("X", "https://x.com/EgosGrowth?t=B43oMvzvu0JHD4E4RQusGg&s=09")],
        [("📞 Contact Support", "contact_support")]
    ]

    keyboard = [[InlineKeyboardButton(text, url=data) if "http" in data else InlineKeyboardButton(text, callback_data=data) for text, data in row] for row in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = "اختر خيارًا من القائمة أدناه:" if lang == "ar" else "Choose an option from the menu below:"
    await query.edit_message_text(text=message, reply_markup=reply_markup)

async def contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = user_states.get(user_id, {}).get("lang", "en")
    
    user_states[user_id]["state"] = "waiting_for_issue"
    message = "✍️ نشكرك على التواصل معنا، يرجى وصف مشكلتك بالتفصيل حتى نتمكن من مساعدتك بشكل أفضل..." if lang == "ar" else "✍️ Thank you for reaching out, Please describe your issue in detail so we can assist you better..."
    await context.bot.send_message(chat_id=user_id, text=message)

async def receive_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_states.get(user_id, {}).get("state") == "waiting_for_issue":
        user_states[user_id]["state"] = "waiting"
        issue_text = update.message.text
        lang = user_states[user_id]["lang"]

        message = (f"📢 **بلاغ جديد** 📢\n\n"
                   f"👤 **المستخدم:** @{update.message.from_user.username or update.message.from_user.first_name}\n"
                   f"🆔 **ايدي اليوزر:** {user_id}\n"
                   f"❌ **المشكلة:** {issue_text}\n\n"
                   f"🚀 الرجاء متابعة الحالة!")

        sent_message = await context.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=message, parse_mode="Markdown")
        user_states[user_id]["support_message_id"] = sent_message.message_id

        confirmation_text = "✅ تم إرسال مشكلتك إلى فريق الدعم سيتم الرد عليك في أقرب وقت " if lang == "ar" else "✅ Your issue has been sent to the support team and they will respond to you soon."
        await update.message.reply_text(confirmation_text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_issue))
    app.add_handler(CallbackQueryHandler(set_language, pattern=r"^lang_(ar|en)$"))
    app.add_handler(CallbackQueryHandler(contact_support, pattern=r"^contact_support$"))
    
    print("✅ Bot Is Working...")
    app.run_polling()

if __name__ == "__main__":
    main()

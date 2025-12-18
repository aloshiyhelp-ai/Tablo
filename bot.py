import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("=" * 50)
print("🤖 BALL BOT v2.0 ISHGA TUSHMOQDA...")
print("=" * 50)

# TOKEN - O'Z TOKENINGIZNI QO'YING!
TOKEN = "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Saqlash uchun oddiy dictionary
points_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komandasi"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Salom {user.first_name}!\n"
        f"🎯 *Ball Bot ishga tushdi!*\n\n"
        f"✅ *Ball berish:*\n"
        "Kimdir javob bersa, uning xabariga reply qilib '+5' yozing\n\n"
        f"📊 *Buyruqlar:*\n"
        "/ball - Reyting\n"
        "/myball - Mening ballarim",
        parse_mode='Markdown'
    )
    print(f"✅ Start command from: {user.first_name}")

async def give_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply orqali ball berish"""
    if update.message.reply_to_message:
        chat_id = str(update.message.chat.id)
        user = update.message.reply_to_message.from_user
        user_id = str(user.id)
        
        # Saqlash tizimi
        if chat_id not in points_db:
            points_db[chat_id] = {}
        
        if user_id not in points_db[chat_id]:
            points_db[chat_id][user_id] = {
                'name': user.full_name,
                'points': 0
            }
        
        # 5 ball qo'shish
        points_db[chat_id][user_id]['points'] += 5
        
        await update.message.reply_text(
            f"✅ *{user.full_name}* ga +5 ball!\n"
            f"📊 Jami: {points_db[chat_id][user_id]['points']} ball",
            parse_mode='Markdown'
        )
        print(f"✅ 5 ball added to {user.full_name}")

async def show_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reytingni ko'rsatish"""
    chat_id = str(update.message.chat.id)
    
    if chat_id in points_db and points_db[chat_id]:
        users = points_db[chat_id]
        # Ballar bo'yicha tartiblash
        sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
        
        text = "🏆 *GURUH REYTINGI* 🏆\n\n"
        for i, (uid, data) in enumerate(sorted_users[:10], 1):
            if i == 1:
                medal = "🥇 "
            elif i == 2:
                medal = "🥈 "
            elif i == 3:
                medal = "🥉 "
            else:
                medal = f"{i}. "
            
            text += f"{medal}*{data['name']}* - {data['points']} ball\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        await update.message.reply_text("Hali hech kim ball to'plamagan!")

async def my_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shaxsiy ballarni ko'rsatish"""
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    
    if chat_id in points_db and user_id in points_db[chat_id]:
        user_points = points_db[chat_id][user_id]['points']
        await update.message.reply_text(f"📊 Sizda *{user_points} ball* bor!", parse_mode='Markdown')
    else:
        await update.message.reply_text("Sizda hali ball yo'q!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatolarni qayta ishlash"""
    logger.error(f"Xato {context.error} chiqdi")

def main():
    """Asosiy funksiya"""
    print(f"🔑 Token uzunligi: {len(TOKEN)}")
    print(f"🔑 Token boshi: {TOKEN[:20]}...")
    
    if not TOKEN or TOKEN == "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg":
        print("❌ Iltimos, TOKEN ni o'zgartiring! Bot Father bergan tokeningizni qo'ying.")
        return
    
    try:
        # Bot yaratish (YANGI VERSIYA)
        application = Application.builder().token(TOKEN).build()
        
        # Handlerlar qo'shish
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ball", show_ball))
        application.add_handler(CommandHandler("myball", my_ball))
        application.add_handler(MessageHandler(filters.REPLY & filters.TEXT, give_points))
        
        # Xato handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot yaratildi!")
        print("🔄 Polling boshlanmoqda...")
        
        # Botni ishga tushirish
        application.run_polling()
        
    except Exception as e:
        print(f"❌ XATO: {type(e).__name__}")
        print(f"❌ Xato tafsiloti: {str(e)[:100]}...")
        
        if "invalid" in str(e).lower() or "unauthorized" in str(e):
            print("❗ TOKEN NOTO'G'RI! @BotFather dan yangi bot yarating.")
        else:
            print("❗ Boshqa xato.")

if __name__ == '__main__':
    main()

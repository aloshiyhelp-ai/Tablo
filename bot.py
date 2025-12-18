import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

print("=" * 50)
print("🤖 BALL BOT v2.0 ISHGA TUSHMOQDA...")
print("=" * 50)

# Token - BU YERGA O'Z TOKENINGIZNI YOZING
TOKEN = "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Saqlash
points_db = {}

async def start(update: Update, context: CallbackContext):
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
    logger.info(f"Start command from {user.first_name}")

async def give_points(update: Update, context: CallbackContext):
    try:
        if update.message.reply_to_message:
            chat_id = str(update.message.chat.id)
            user = update.message.reply_to_message.from_user
            user_id = str(user.id)
            
            # 5 ball berish
            if chat_id not in points_db:
                points_db[chat_id] = {}
            
            if user_id not in points_db[chat_id]:
                points_db[chat_id][user_id] = {
                    'name': user.full_name,
                    'points': 0
                }
            
            points_db[chat_id][user_id]['points'] += 5
            
            await update.message.reply_text(
                f"✅ *{user.full_name}* ga +5 ball!\n"
                f"📊 Jami: {points_db[chat_id][user_id]['points']} ball",
                parse_mode='Markdown'
            )
            logger.info(f"Added 5 points to {user.full_name}")
    except Exception as e:
        logger.error(f"Error in give_points: {e}")

async def show_ball(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat.id)
    
    if chat_id in points_db and points_db[chat_id]:
        users = points_db[chat_id]
        sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
        
        text = "🏆 *GURUH REYTINGI* 🏆\n\n"
        for i, (uid, data) in enumerate(sorted_users[:10], 1):
            if i == 1: medal = "🥇 "
            elif i == 2: medal = "🥈 "
            elif i == 3: medal = "🥉 "
            else: medal = f"{i}. "
            
            text += f"{medal}*{data['name']}* - {data['points']} ball\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        await update.message.reply_text("Hali hech kim ball to'plamagan!")

async def my_ball(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    
    if chat_id in points_db and user_id in points_db[chat_id]:
        points = points_db[chat_id][user_id]['points']
        await update.message.reply_text(f"📊 Sizda *{points} ball* bor!", parse_mode='Markdown')
    else:
        await update.message.reply_text("Sizda hali ball yo'q!")

async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    # Token tekshirish
    if not TOKEN:
        logger.error("❌ Token kiritilmagan!")
        print("❌ ERROR: Token kiritilmagan!")
        return
    
    print(f"🔑 Token uzunligi: {len(TOKEN)}")
    print(f"🔑 Token: {TOKEN[:15]}...")
    
    try:
        # Bot yaratish (YANGI VERSIYA)
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlar
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ball", show_ball))
        app.add_handler(CommandHandler("myball", my_ball))
        app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, give_points))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        print("✅ Bot yaratildi!")
        print("🔄 Polling boshlanmoqda...")
        
        # Ishga tushirish
        app.run_polling()
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {type(e).__name__}")
        print(f"❌ Xato: {str(e)[:200]}")
        
        if "invalid" in str(e).lower() or "unauthorized" in str(e):
            print("❗ TOKEN NOTO'G'RI! @BotFather dan yangi token oling")
        elif "timed out" in str(e).lower():
            print("❗ INTERNET MUAMMOSI")
        else:
            print("❗ Boshqa xato")

if __name__ == '__main__':
    main()

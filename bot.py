import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Token environment'dan olish
TOKEN = "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg"
# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Saqlash uchun
points_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 *Ball Bot ishga tushdi!*\n\n"
        "✅ *Ball berish:*\n"
        "Kimdir javob bersa, uning xabariga reply qilib '+5' yozing\n\n"
        "📊 *Buyruqlar:*\n"
        "/ball - Reyting\n"
        "/myball - Mening ballarim",
        parse_mode='Markdown'
    )

async def give_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def show_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    
    if chat_id in points_db and points_db[chat_id]:
        users = points_db[chat_id]
        sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
        
        text = "🏆 *GURUH REYTINGI* 🏆\n\n"
        for i, (uid, data) in enumerate(sorted_users[:10], 1):
            medal = "🥇 " if i == 1 else f"{i}. "
            text += f"{medal}*{data['name']}* - {data['points']} ball\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        await update.message.reply_text("Hali hech kim ball to'plamagan!")

async def my_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    
    if chat_id in points_db and user_id in points_db[chat_id]:
        points = points_db[chat_id][user_id]['points']
        await update.message.reply_text(f"📊 Sizda *{points} ball* bor!", parse_mode='Markdown')
    else:
        await update.message.reply_text("Sizda hali ball yo'q!")

def main():
    if not TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi! Environment variable qo'ying.")
        return
    
    # Bot yaratish
    app = Application.builder().token(TOKEN).build()
    
    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ball", show_ball))
    app.add_handler(CommandHandler("myball", my_ball))
    
    # Reply handler
    app.add_handler(MessageHandler(
        filters.REPLY & filters.TEXT & filters.ChatType.GROUPS,
        give_points
    ))
    
    # Ishga tushirish
    logger.info("🤖 Bot ishga tushmoqda...")
    app.run_polling()

if __name__ == '__main__':
    main()

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

print("=" * 50)
print("🤖 BALL BOT ISHGA TUSHMOQDA...")
print("=" * 50)

# TOKEN - O'Z TOKENINGIZNI QO'YING
TOKEN = "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Saqlash uchun oddiy dictionary
points = {}

# Start komandasi
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
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

# Ball berish
def give_points(update, context):
    if update.message.reply_to_message:
        chat_id = str(update.message.chat.id)
        user = update.message.reply_to_message.from_user
        user_id = str(user.id)
        
        # Saqlash tizimi
        if chat_id not in points:
            points[chat_id] = {}
        
        if user_id not in points[chat_id]:
            points[chat_id][user_id] = {
                'name': user.full_name,
                'points': 0
            }
        
        # 5 ball qo'shish
        points[chat_id][user_id]['points'] += 5
        
        update.message.reply_text(
            f"✅ *{user.full_name}* ga +5 ball!\n"
            f"📊 Jami: {points[chat_id][user_id]['points']} ball",
            parse_mode='Markdown'
        )
        print(f"✅ 5 ball added to {user.full_name}")

# Reyting
def show_ball(update, context):
    chat_id = str(update.message.chat.id)
    
    if chat_id in points and points[chat_id]:
        users = points[chat_id]
        # Ballar bo'yicha tartiblash
        sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
        
        text = "🏆 *GURUH REYTINGI* 🏆\n\n"
        for i, (uid, data) in enumerate(sorted_users[:10], 1):
            if i == 1: medal = "🥇 "
            elif i == 2: medal = "🥈 "
            elif i == 3: medal = "🥉 "
            else: medal = f"{i}. "
            
            text += f"{medal}*{data['name']}* - {data['points']} ball\n"
        
        update.message.reply_text(text, parse_mode='Markdown')
    else:
        update.message.reply_text("Hali hech kim ball to'plamagan!")

# Shaxsiy ball
def my_ball(update, context):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    
    if chat_id in points and user_id in points[chat_id]:
        user_points = points[chat_id][user_id]['points']
        update.message.reply_text(f"📊 Sizda *{user_points} ball* bor!", parse_mode='Markdown')
    else:
        update.message.reply_text("Sizda hali ball yo'q!")

# Xato handler
def error(update, context):
    logger.warning(f'Xato: {context.error}')

# Asosiy funksiya
def main():
    print(f"

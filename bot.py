import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("=" * 50)
print("🤖 BALL BOT ISHGA TUSHMOQDA...")
print("=" * 50)

# TOKENNI BU YERGA YANGI TOKEN QO'YING
TOKEN = "8568086831:AAF5idiBW0T0V6EuQXZk_XFMwlO64fpULrg"  # ❗❗ BOT FATHER BERGAN YANGI TOKEN

# Simple storage
points = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"✅ Start from: {user.first_name}")
    await update.message.reply_text(
        f"👋 Salom {user.first_name}!\n"
        f"🎯 Ball Bot faol!\n\n"
        f"✅ Reply bilan +5 ball bering\n"
        f"📊 /ball - Reyting\n"
        f"📈 /myball - Mening ballarim"
    )

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message:
            chat_id = str(update.message.chat.id)
            user = update.message.reply_to_message.from_user
            user_id = str(user.id)
            
            if chat_id not in points:
                points[chat_id] = {}
            if user_id not in points[chat_id]:
                points[chat_id][user_id] = {"name": user.full_name, "points": 0}
            
            points[chat_id][user_id]["points"] += 5
            
            await update.message.reply_text(
                f"✅ {user.full_name} +5 ball!\n"
                f"📊 Jami: {points[chat_id][user_id]['points']} ball"
            )
            print(f"✅ Ball added to {user.full_name}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def show_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    if chat_id in points:
        text = "🏆 REYTING:\n"
        sorted_users = sorted(points[chat_id].items(), key=lambda x: x[1]["points"], reverse=True)
        for i, (uid, data) in enumerate(sorted_users[:10], 1):
            text += f"{i}. {data['name']} - {data['points']} ball\n"
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Hali ballar yo'q!")

async def my_ball(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    user_id = str(update.message.from_user.id)
    if chat_id in points and user_id in points[chat_id]:
        score = points[chat_id][user_id]["points"]
        await update.message.reply_text(f"Sizda {score} ball bor!")
    else:
        await update.message.reply_text("Sizda hali ball yo'q!")

def main():
    # Token tekshirish
    if not TOKEN or TOKEN == "YANGI_TOKEN_QO'YING":
        print("❌ ERROR: Token kiritilmagan!")
        print("❗ Token qo'yish: TOKEN = '1234567890:AAH...'")
        return
    
    print(f"🔑 Token uzunligi: {len(TOKEN)}")
    print(f"🔑 Token boshi: {TOKEN[:20]}...")
    
    try:
        # Bot yaratish
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlar
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ball", show_ball))
        app.add_handler(CommandHandler("myball", my_ball))
        app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_reply))
        
        print("✅ Bot yaratildi!")
        print("🔄 Polling boshlanmoqda...")
        
        # Ishga tushirish
        app.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {type(e).__name__}")
        print(f"❌ Xato: {str(e)[:200]}")
        
        if "Forbidden" in str(e) or "Unauthorized" in str(e):
            print("❗ TOKEN NOTO'G'RI! Yangi bot yarating @BotFather da")
        elif "timed out" in str(e):
            print("❗ INTERNET MUAMMOSI")
        else:
            print("❗ Noma'lum xato")

if __name__ == "__main__":
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

TOKEN = os.getenv("TOKEN") # Lo pondremos en Render
ID_CANAL = -1004459106029

async def start(update, context):
    await update.message.reply_text("Bienvenida a Verified Models 🩷 Abre la Mini App 👑")

async def recibir_miniapp(update, context):
    datos = json.loads(update.effective_message.web_app_data.data)
    user = update.effective_user
    fotos = await context.bot.get_user_profile_photos(user.id, limit=1)

    texto = f"💎 NUEVA - {user.first_name} (@{user.username or 'sin username'}) 🆔{user.id}\n✅ {', '.join(datos)}"
    url = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"
    botones = InlineKeyboardMarkup([[InlineKeyboardButton(f"💬 Contactar a {user.first_name}", url=url)]])

    await update.message.reply_text(f"Gracias {user.first_name}! Recibimos: {', '.join(datos)} 🩷")

    if fotos.total_count > 0:
        await context.bot.send_photo(ID_CANAL, fotos.photos[0][-1].file_id, caption=texto, reply_markup=botones)
    else:
        await context.bot.send_message(ID_CANAL, texto, reply_markup=botones)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, recibir_miniapp))
app.run_polling()

import os
import threading
from flask import Flask
from google import genai
import telebot

# Flask server
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ANONX AI bot ishlayapti!", 200

# AI va Bot sozlamalari
AI_API_KEY = os.environ.get("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")
BOT_TOKEN = os.environ.get("7645388286:AAEywTFrFIAAcfqU4mjp4Vxg9Qs8KVOwcM8")

client = genai.Client(api_key=AI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# START komandasi
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "ANONX AI botiga hush kelibsiz!")

# Har qanday xabar
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message.text
        )
        text = response.text.strip() if response.text else "Javob topilmadi."
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"xatolik yuz berdi: {e}")

# Botni alohida oqimda ishga tushirish
def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000, debug=True)

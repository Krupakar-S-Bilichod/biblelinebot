import telebot
import json

# Load Bible verses from a local JSON file
with open("bible_verses.json", "r", encoding="utf-8") as file:
    BIBLE = json.load(file)

# Your Telegram bot token
TOKEN = 7905078187:AAGd9gstRGKYfxZp22z24AUC7wCfAD_8nUg
bot = telebot.TeleBot(TOKEN)

# Step 1: Show book selection
@bot.message_handler(commands=['start'])
def send_books(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for book in BIBLE.keys():
        keyboard.add(telebot.types.KeyboardButton(book))
    bot.send_message(message.chat.id, "Select a book:", reply_markup=keyboard)

# Step 2: Show chapters after book selection
@bot.message_handler(func=lambda message: message.text in BIBLE.keys())
def send_chapters(message):
    book = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for chapter in BIBLE[book].keys():
        keyboard.add(telebot.types.KeyboardButton(chapter))
    bot.send_message(message.chat.id, f"Select a chapter from {book}:", reply_markup=keyboard)

# Step 3: Show verses after chapter selection
@bot.message_handler(func=lambda message: any(message.text in BIBLE[book] for book in BIBLE))
def send_verses(message):
    for book in BIBLE:
        if message.text in BIBLE[book]:
            chapter = message.text
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for verse in BIBLE[book][chapter]:
                keyboard.add(telebot.types.KeyboardButton(verse))
            bot.send_message(message.chat.id, f"Select a verse from Chapter {chapter}:", reply_markup=keyboard)
            return

# Step 4: Show selected verse
@bot.message_handler(func=lambda message: any(message.text in BIBLE[book][chapter] for book in BIBLE for chapter in BIBLE[book]))
def send_verse_text(message):
    for book in BIBLE:
        for chapter in BIBLE[book]:
            if message.text in BIBLE[book][chapter]:
                verse_number = message.text
                verse_text = BIBLE[book][chapter][verse_number]
                bot.send_message(message.chat.id, f"{book} {chapter}:{verse_number} - {verse_text}")
                return

# Run the bot
bot.polling()

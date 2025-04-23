import telebot
from telebot import types
import os

# Bot tokeni
TOKEN = "7589006501:AAFagHRJOiviG0W-ztpZmwzB2r1DHAYR-uM"
bot = telebot.TeleBot(TOKEN)

# PDF fayllar saqlanadigan papka
PDF_FOLDER = "pdfs/"

# Kitoblar ro'yxati (har bir kategoriyada 10 ta kitob, PDF fayl yo'llari bilan)
books = {
    "Badiiy": [
        {"name": "Alkimyogar - Paulo Koelyo", "pdf": os.path.join(PDF_FOLDER, "alkimyogar.pdf")},
        {"name": "Shaytanat - To‘xtasin Jalilov", "pdf": os.path.join(PDF_FOLDER, "shaytanat.pdf")},
        {"name": "O‘tgan kunlar - Abdulla Qodiriy", "pdf": os.path.join(PDF_FOLDER, "utgan_kunlar_ziyouz_com.pdf")},
        {"name": "Yulduzli tunlar - Pirimqul Qodirov", "pdf": os.path.join(PDF_FOLDER, "yulduzli_tunlar.pdf")},
        {"name": "Jimjitlik - Said Ahmad ", "pdf": os.path.join(PDF_FOLDER, "Jimjitlik.pdf")},
        {"name": "Ikki eshik orasi - Otkir_Hoshimov", "pdf": os.path.join(PDF_FOLDER, "Ikki_eshik_orasi.pdf")},
        {"name": "Martin Iden - Jek London", "pdf": os.path.join(PDF_FOLDER, "martin_iden.pdf")},
        {"name": "Don Kixot - Migel de Servantes", "pdf": os.path.join(PDF_FOLDER, "don_kixot.pdf")},

    ],
    "She’riy": [
        {"name": "Xamsa - Alisher Navoiy", "pdf": os.path.join(PDF_FOLDER, "xamsa.pdf")},
        {"name": "Lison ut-Tayr - Alisher Navoiy", "pdf": os.path.join(PDF_FOLDER, "lison_ut_tayr.pdf")},
        {"name": "Tuyg‘ular - Zulfiya", "pdf": os.path.join(PDF_FOLDER, "tuygular.pdf")},
        {"name": "Ruboiylar - Umar Xayyom", "pdf": os.path.join(PDF_FOLDER, "ruboiylar.pdf")},

    ],
    "Darsliklar": [
        {"name": "Axborot xavfsizligi asoslari kitob", "pdf": os.path.join(PDF_FOLDER, "Axborot xavfsizligi asoslari kitob.pdf")},
        {"name": "Kompyuter-tarmoqlari", "pdf": os.path.join(PDF_FOLDER, "Kompyuter-tarmoqlari.Z.Z.MiryusupovJ.X.Djumanov..pdf")},
        {"name": "Dasturlash-texnologiya", "pdf": os.path.join(PDF_FOLDER, "Dasturlash-texnologiya.Назиров-Ш.pdf")},

    ]
}


# Asosiy menyuni yaratish
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Badiiy kitoblar")
    btn2 = types.KeyboardButton("✍️ She’riy kitoblar")
    btn3 = types.KeyboardButton("📖 Darsliklar")
    btn4 = types.KeyboardButton("🔍 Kitob qidirish")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


# Kitoblar ro'yxatini inline klaviatura bilan yuborish
def send_book_list(chat_id, category):
    message = f"{category} ro‘yxati:\n"
    markup = types.InlineKeyboardMarkup()
    for book in books[category]:
        message += f"- {book['name']}\n"
        markup.add(types.InlineKeyboardButton(
            text=f"📄 {book['name']} PDF",
            callback_data=f"pdf_{category}_{book['name']}"
        ))
    bot.send_message(chat_id, message, reply_markup=markup)


# Start buyrug'i
@bot.message_handler(commands=["start"])
def start(message):
    welcome_text = (
        "Assalomu aleykum! 📖\n"
        "Ushbu bot sizga badiiy, she’riy va darslik kitoblarni taqdim etadi.\n"
        "Quyidagi bo‘limlardan birini tanlang:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_menu())


# Foydalanuvchi xabarlariga javob berish
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "📚 Badiiy kitoblar":
        send_book_list(message.chat.id, "Badiiy")
    elif message.text == "✍️ She’riy kitoblar":
        send_book_list(message.chat.id, "She’riy")
    elif message.text == "📖 Darsliklar":
        send_book_list(message.chat.id, "Darsliklar")
    elif message.text == "🔍 Kitob qidirish":
        bot.send_message(message.chat.id, "Qidirilayotgan kitob nomini kiriting:")
        bot.register_next_step_handler(message, search_book)
    else:
        bot.send_message(message.chat.id, "Iltimos, menyudan biror bo‘limni tanlang.", reply_markup=create_main_menu())


# Kitob qidirish funksiyasi
def search_book(message):
    query = message.text.lower()
    results = []
    markup = types.InlineKeyboardMarkup()
    for category, book_list in books.items():
        for book in book_list:
            if query in book['name'].lower():
                results.append(book['name'])
                markup.add(types.InlineKeyboardButton(
                    text=f"📄 {book['name']} PDF",
                    callback_data=f"pdf_{category}_{book['name']}"
                ))
    if results:
        bot.send_message(message.chat.id, "Topilgan kitoblar:\n" + "\n".join(results), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hech qanday kitob topilmadi.")
    bot.send_message(message.chat.id, "Yana biror nima qilamiz?", reply_markup=create_main_menu())


# Inline tugmalar uchun ishlov berish
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("pdf_"):
        try:
            _, category, book_name = call.data.split("_", 2)
            for book in books[category]:
                if book['name'] == book_name:
                    pdf_path = book['pdf']
                    if os.path.exists(pdf_path):
                        with open(pdf_path, 'rb') as pdf_file:
                            bot.send_document(call.message.chat.id, pdf_file, caption=f"📄 {book_name}")
                    else:
                        bot.send_message(call.message.chat.id, f"PDF fayl topilmadi: {book_name}")
                    break
            bot.answer_callback_query(call.id)
        except Exception as e:
            bot.send_message(call.message.chat.id,
                             f"Xato yuz berdi: PDF faylni yuborib bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
            bot.answer_callback_query(call.id)
            print(f"Xato: {e}")


# Botni ishga tushirish
if __name__ == "__main__":
    # PDF papkasini yaratish
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
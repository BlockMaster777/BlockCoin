# coding=utf-8
import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TG_BOT_TOKEN"))


def gen_ru_translation_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("RU 🇷🇺", callback_data="rus_menu"))
    return markup


@bot.message_handler(commands=['start', "help"])
def start_message(message):
    bot.reply_to(message,
                 "*MENU*\n"
                 "/verify <token or tokens, split with spaces>\n"
                 "/save <token or tokens, split with spaces> - save tokens to the bot\n"
                 "/mytokens - see your tokens\n"
                 "/top - top 20 richest\n"
                 "/usertokens <username> - see users tokens\n\n"
                 "To mine tokens for yourself or someone, you need to download an open source desktop app\n"
                 "https://github.com/BlockMaster777/BlockCoin", reply_markup=gen_ru_translation_markup(),
                 parse_mode="Markdown", disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == "rus_menu")
def rus_menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*МЕНЮ*\n"
                 "/verify <токен(-ы), разделять пробелами>\n"
                 "/save <токен(-ы), разделять пробелами> - сохранить токены в боте\n"
                 "/mytokens - посмотреть ваши токены\n"
                 "/top - топ 20 самых богатых\n"
                 "/usertokens <имя пользователя> - посмотреть токены пользователя\n\n"
                 "Чтобы майнить токены себе или кому-то другому, вы должны установить приложение для ПК с открытым "
                 "исходным кодом\n"
                 "https://github.com/BlockMaster777/BlockCoin", parse_mode="Markdown", disable_web_page_preview=True)
    

bot.infinity_polling(timeout=60)

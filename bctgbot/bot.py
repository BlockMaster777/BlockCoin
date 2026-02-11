# coding=utf-8
import telebot
from telebot import types
import os
import bctgbot.api as api
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TG_BOT_TOKEN"))

def get_args(text) -> list[str]:
    els = text.split(" ")[1:]
    elsf = []
    for el in els:
        if el == "":
            continue
        else:
            elsf.append(el)
    return elsf

def gen_ru_translation_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("RU 🇷🇺", callback_data="rus_menu"))
    return markup


@bot.message_handler(commands=['start', "help"])
def start_message(message):
    bot.reply_to(message,
                 "*MENU*\n"
                 "/start or /help \\- show this message\n"
                 "/verify \\<token or tokens, split with spaces\\> \\- verify tokens\n"
                 "~/save \\<token or tokens, split with spaces\\> \\- save tokens to the bot~\n"
                 "~/mytokens \\- see your tokens~\n"
                 "~/top \\- top 20 richest~\n"
                 "~/usertokens \\<username\\> \\- see users tokens~\n\n"
                 "Send file tokens\\.txt which was exported from the app, to verify tokens in it\n"
                 "To mine tokens for yourself or someone, you need to download an open source desktop app\n"
                 "https://github\\.com/BlockMaster777/BlockCoin", reply_markup=gen_ru_translation_markup(),
                 parse_mode="MarkdownV2", disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == "rus_menu")
def rus_menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*МЕНЮ*\n"
                 "/start или /help \\- показать это сообщение\n"
                 "/verify \\<токен\\(\\-ы\\), разделять пробелами\\> \\- проверить токены\n"
                 "~/save \\<токен\\(\\-ы\\), разделять пробелами\\> \\- сохранить токены в боте~\n"
                 "~/mytokens \\- посмотреть ваши токены~\n"
                 "~/top \\- топ 20 самых богатых~\n"
                 "~/usertokens \\<имя пользователя\\> \\- посмотреть токены пользователя~\n\n"
                 "Отправьте файл tokens\\.txt, который был экспортирован из приложения, для проверки токенов внутри\n"
                 "Чтобы майнить токены себе или кому\\-то другому, вы должны установить приложение для ПК с открытым "
                 "исходным кодом\n"
                 "https://github\\.com/BlockMaster777/BlockCoin", parse_mode="MarkdownV2",
                          disable_web_page_preview=True)


def do_verifying(message, args):
    if len(args) < 1:
        bot.reply_to(message, "Send at least 1 token / Отправьте как минимум один токен")
        return
    wrong = []
    right_count = 0
    for res in api.verify_tokens(args):
        if res["result"]:
            right_count += 1
        else:
            wrong.append(res)
    wrong_msg_part = ""
    for res in wrong:
        wrong_msg_part += f"⛔ {res["token"]} - {res["err"]}\n"
    bot.reply_to(message, f"VERIFYING RESULTS\n✅ {right_count}, ⛔ {len(wrong)}\n\n" + (wrong_msg_part if
                                len(wrong_msg_part) <  4000 else "Too many wrong "
                                "tokens to display / Слишком много неправильных токенов для отображения"))


@bot.message_handler(commands=['verify'])
def verify(message):
    args = get_args(message.text)
    do_verifying(message, args)


@bot.message_handler(content_types=['document'], func=lambda message: message.document.file_name == "tokens.txt")
def handle_tokens_file(message):
    if message.document.mime_type != "text/plain":
        bot.reply_to(message, "Only text files are supported / Поддерживаются только текстовые файлы")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    content = downloaded_file.decode()
    args = content.split(" ")
    do_verifying(message, args)
    

bot.infinity_polling(timeout=60)

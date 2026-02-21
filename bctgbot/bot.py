# coding=utf-8
import telebot
from telebot import types
import os
import bctgbot.api as api
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TG_BOT_TOKEN"))


def get_args(text) -> list[str]:
    elements = text.split(" ")[1:]
    result = []
    for el in elements:
        if el == "":
            continue
        else:
            result.append(el)
    return result


def gen_ru_translation_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("RU 🇷🇺", callback_data="rus_menu"))
    return markup


def gen_ru_info_translation_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("RU 🇷🇺", callback_data="rus_info"))
    return markup


@bot.message_handler(commands=['start', "help"])
def start_message(message):
    bot.reply_to(message,
    "**MENU**\n"
    "/start or /help \\- show this message\n"
    "/info \\- information about this bot\n"
    "/verify \\<token or tokens, split with spaces\\> \\- verify tokens\n"
    "/save \\<token or tokens, split with spaces\\> \\- save tokens to the bot\n"
    "/mytokens \\- see your tokens\n"
    "~/top \\- top 20 richest~\n"
    "~/usertokens \\<username\\> \\- see users tokens~\n\n"
    "Send file v\\_tokens\\.txt which was exported from the app, to verify tokens in it\n"
    "Send file s\\_tokens\\.txt which was exported from the app, to save tokens in it\n\n"
    "To mine tokens for yourself or someone, you need to download an open source desktop app\n"
    "https://github\\.com/BlockMaster777/BlockCoin", reply_markup=gen_ru_translation_markup(),
                 parse_mode="MarkdownV2", disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data == "rus_menu")
def rus_menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=
    "**МЕНЮ**\n"
    "/start или /help \\- показать это сообщение\n"
    "/info \\- информация о проекте\n"
    "/verify \\<токен\\(\\-ы\\), разделять пробелами\\> \\- проверить токены\n"
    "/save \\<токен\\(\\-ы\\), разделять пробелами\\> \\- сохранить токены в боте\n"
    "/mytokens \\- посмотреть ваши токены\n"
    "~/top \\- топ 20 самых богатых~\n"
    "~/usertokens \\<имя пользователя\\> \\- посмотреть токены пользователя~\n\n"
    "Чтобы майнить токены себе или кому\\-то другому, "
    "вы должны установить приложение для ПК с открытым "
    "исходным кодом\n"
    "https://github\\.com/BlockMaster777/BlockCoin", parse_mode="MarkdownV2",
                          disable_web_page_preview=True)


@bot.message_handler(commands=["info"])
def info_menu(message):
    bot.reply_to(message,
    "**Info about BlockCoin**\n"
    "> BlockCoin is a non\\-spendable, yet mineable, currency developed by @BlockMaster777\\. "
    "It's based on the concept of a token\\-currency, where you can mine tokens for yourself or "
    "for someone else\\. You can't spend this type of currency because you can't completely remove a "
    "piece of information \\(the token\\) from existence and prove it to everyone\\. You also can't "
    "transfer "
    "your tokens to someone else because you can't change the owner of a token without changing its "
    "hash\\. "
    "The token looks like this: protocol\\_version$$$owner\\_of\\_the\\_token$$$random\\_characters$$$hash"
    "\\. "
    "The hash is a 'fingerprint' of all the other information in the token\\. It's impossible to recover "
    "information from the 'fingerprint'\\. A token's hash must start with '0000' to be valid\\. "
    "Mining a single token means finding random data that, when combined with the owner and protocol "
    "version, will result in a hash starting with '0000'\\. Due to the irreversibility of the hashing "
    "algorithm, the best way to do this is to randomize the data and hope it works "
    "\\(verifying random data one by one also works\\)\\. Mining a single token takes about 1 second on a "
    "moderately powerful computer\\.\n\n"
    "> Original creator of token\\-currency concept \\- @aryluneix0\n\n",
                 parse_mode="MarkdownV2", reply_markup=gen_ru_info_translation_markup())


@bot.callback_query_handler(func=lambda call: call.data == "rus_info")
def rus_info(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
    "**Информация о BlockCoin**\n"
    "> BlockCoin — это нерасходуемая, но майнинговая валюта, разработанная @BlockMaster777\\. "
    "Она основана на концепции токен\\-валюты, где вы можете майнить токены для себя или для "
    "кого\\-то другого\\. Вы не можете потратить этот тип валюты, потому что вы не можете "
    "полностью "
    "удалить часть информации \\(токен\\) из существования и доказать это всем\\. Также вы не "
    "можете "
    "передать свои токены кому\\-либо другому, потому что вы не можете изменить владельца "
    "токена, "
    "не изменив при этом его хеш\\. "
    "Токен выглядит так: версия\\_протокола$$$владелец$$$случайные\\_символы$$$хэш\\. "
    "Хэш — это «отпечаток пальца» всей остальной информации токена\\. Восстановить "
    "информацию "
    "из "
    "«отпечатка пальца» невозможно\\. Хэш токена должен начинаться с «0000», чтобы быть "
    "действительным\\. Майнинг одного токена означает поиск случайных данных, которые в "
    "сочетании "
    "с владельцем и версией протокола приведут к тому, что хеш будет начинаться с «0000»\\. "
    "А из\\-за необратимости алгоритма хеширования лучший способ сделать это — рандомизировать "
    "данные и надеяться, что это сработает \\(проверка случайных данных по одному тоже "
    "сработает\\)\\. "
    "Майнинг одного токена занимает около 1 секунды на компьютере средней мощности\\.\n\n"
    "> Изначальный создатель концепции токен\\-валюты \\- @aryluneix0\n\n",
                          parse_mode="MarkdownV2")


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
    len(wrong_msg_part) < 4000 else "Too many wrong tokens to display / Слишком много неправильных токенов для отображения"))


def do_saving(message, args):
    if len(args) < 1:
        bot.reply_to(message, "Send at least 1 token / Отправьте как минимум один токен")
        return
    do_verifying(message, args)
    bot.reply_to(message, "Only tokens, that successfully completed verification, and not already in database, "
                          "will be saved / Только токены, которые успешно прошли верификацию, и не находятся в базе "
                          "данных, будут сохранены")
    wrong_count = api.save_tokens(args)
    if wrong_count:
        bot.reply_to(message, f"{len(args) - wrong_count} tokens were successfully saved, {wrong_count} "
                              f"tokens were skipped, because off not completing verification or being already in "
                              f"database / {len(args) - wrong_count} токенов было успешно сохранено, {wrong_count} "
                              f"токенов было пропущено, из-за неправильности или наличии таких-же токенов в базе "
                              f"данных.")
    else:
        bot.reply_to(message, f"All tokens were successfully saved! / Все токены были сохранены!\n"
                              f"/mytokens - see all your tokens / посмотреть ваши токены")


@bot.message_handler(commands=['verify'])
def verify(message):
    args = get_args(message.text)
    do_verifying(message, args)


@bot.message_handler(content_types=['document'], func=lambda message: message.document.file_name == "v_tokens.txt")
def handle_v_tokens_file(message):
    if message.document.mime_type != "text/plain":
        bot.reply_to(message, "Only text files are supported / Поддерживаются только текстовые файлы")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    content = downloaded_file.decode()
    args = content.split(" ")
    do_verifying(message, args)


@bot.message_handler(commands=['save'])
def save_tokens(message):
    args = get_args(message.text)
    do_saving(message, args)


@bot.message_handler(content_types=['document'], func=lambda message: message.document.file_name == "s_tokens.txt")
def handle_s_tokens_file(message):
    if message.document.mime_type != "text/plain":
        bot.reply_to(message, "Only text files are supported / Поддерживаются только текстовые файлы")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    content = downloaded_file.decode()
    args = content.split(" ")
    do_saving(message, args)


@bot.message_handler(commands=['mytokens'])
def my_tokens(message):
    tokens = api.get_users_tokens(message.from_user.username)
    data_str = " ".join(tokens)
    file_with_results = bytes(data_str, "utf-8")
    bot.send_document(message.chat.id, file_with_results,
                      caption=f"{len(tokens)} tokens of "
                              f"{message.from_user.username} / "
                              f"{len(tokens)} токенов {message.from_user.username}",
                      visible_file_name="your_tokens.txt")


if __name__ == '__main__':
    bot.infinity_polling(timeout=60)

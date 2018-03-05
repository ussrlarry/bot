from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import time
import logging


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log'
                    )

def main():
    f = open("token.file","r")
    token = f.readline().rstrip()
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("wordcount", word_counter))
    dp.add_handler(CommandHandler("dict_calc", dict_calculator))
    dp.add_handler(CommandHandler("simple_calc", simple_calculator))

    updater.start_polling()
    updater.idle()

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def planet_constellation(bot, update):
    user_text_get = update.message.text
    cutted_user_input = user_text_get[8:]
    try:
        planet = getattr(ephem, cutted_user_input)
        ephem_planet = planet(time.strftime("%x"))
        update.message.reply_text('Планета %s сейчас находится в созвездии %s' % (cutted_user_input, ephem.constellation(ephem_planet)[1]))
    except AttributeError:
        update.message.reply_text('Сорян, такой планеты пока не открыли')

def word_counter(bot, update):
    user_text_get = update.message.text
    cutted_user_input = user_text_get[11:]

    if cutted_user_input[0] != "\"" or cutted_user_input[-1] != "\"":
        update.message.reply_text('Сорян, нужно брать в кавычки стрингу. Попробуйте еще раз')
    else:
        user_string_no_quotas = cutted_user_input[1:-2]
        user_string_list = user_string_no_quotas.split()

        if not user_string_list:
            update.message.reply_text("Стринга пустая")
        else:
            update.message.reply_text("Ваша стринга состоит из %d слов." % len(user_string_list))

def simple_calculator(bot, update):
    user_input = update.message.text
    cutted_user_input = user_input[13:]
    user_string_list = []

    if cutted_user_input[0] != "\"" or cutted_user_input[-1] != "\"":
        update.message.reply_text('Сорян, нужно брать в кавычки стрингу. Попробуйте еще раз')
    elif cutted_user_input[-2] != "=" or len(cutted_user_input) <= 3:
        update.message.reply_text('Арфиметическое выражение должно заканчиваться на "=" и не должно быть пустым')
    else:
        user_string_no_quotas = cutted_user_input[1:-2]
        user_string_cutted = str(user_string_no_quotas)

        for i in user_string_cutted:
            user_string_list.append(i)

        if len(user_string_list) < 3:
            update.message.reply_text("Нужно ввести 2 числа для выполнения операции")
        else:
            try:
                final = eval(''.join(user_string_list))
                update.message.reply_text(final)
            except NameError:
                update.message.reply_text('Было бы неплохо использовать числа для арифметических операций')

def dict_calculator(bot, update):
    all_numbers = {
            "ноль": '0',
            "один": '1',
            "два": '2',
            "три": '3',
            "четыре": '4',
            "пять": '5',
            "шесть": '6',
            "семь": '7',
            "восемь": '8',
            "девять": '9',
            "десять": '10',
            "плюс": '+',
            "минус": '-',
            "равно": '=',
            "умножить": '*',
            "делить": '/',
            "возвести": '**',
            "и": '.'
        }

    result_list = []
    input_list = []

    user_input = update.message.text
    cutted_user_input = user_input[11:]
    user_input_noquotas = cutted_user_input[1:-1]
    input_list = user_input_noquotas.split()
    
    for i in input_list:
        if i in all_numbers.keys():
            result_list.append(all_numbers.get(i))
    try:
        final = eval(''.join(result_list))
        update.message.reply_text(round(final, 2))
    except ZeroDivisionError:
        update.message.reply_text('На нолик мы не делим!')

if __name__ == '__main__':
    main()

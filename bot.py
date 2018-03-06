from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import time
import logging
from telepot.namedtuple import ReplyKeyboardMarkup

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename='bot.log'
                    )

def main():
    f = open("token.file","r")
    token = f.readline().rstrip()
    updater = Updater(token)


    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_constellation))
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

    if cutted_user_input[0] != "\"" or cutted_user_input[-1] != "\"":
        update.message.reply_text('Сорян, нужно брать в кавычки стрингу. Попробуйте еще раз')
    elif cutted_user_input[-2] != "=" or len(cutted_user_input) <= 3:
        update.message.reply_text('Арфиметическое выражение должно заканчиваться на "=" и не должно быть пустым')
    else:
        user_string_no_quotas = cutted_user_input[1:-2]

    def calculator(string):
        no_spaces_string = string.lower().replace(" ", "")
        parts = no_spaces_string.split("+")

        try:
            for i in range(len(parts)):
                if "-" in parts[i]:
                    parts[i] = parts[i].split("-")

            for i in range(len(parts)):
                parts[i] = precalculator(parts[i])

            result = sum(parts)
        except ValueError:
            result = ("Не надо использовать неправильный тип данных")
        except ZeroDivisionError:
            result = ("На нолик мы не делим")

        return result

    def precalculator(part):
        if type(part) is str:
            if "*" in part:
                result = 1
                for subpart in part.split("*"):
                    result *= precalculator(subpart)
                return result
            elif "/" in part:
                parts = list(map(precalculator, part.split("/")))
                result = parts[0]
                for subpart in parts[1:]:
                    result /= subpart
                return result
            else:
                return float(part)
        elif type(part) is list:
            for i in range(len(part)):
                part[i] = precalculator(part[i])
            return part[0] - sum(part[1:])

    update.message.reply_text(calculator(user_string_no_quotas))

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

    user_input = update.message.text
    cutted_string = user_input[11:]
    delete_quotas = cutted_string[1:-1]
    input_list = delete_quotas.split()

    for i in input_list:
        if i in all_numbers.keys():
            result_list.append(all_numbers.get(i))

    string_to_calc = ''.join(result_list)

    def calculator(string):
        no_spaces_string = string.lower().replace(" ", "")
        parts = no_spaces_string.split("+")

        try:
            for i in range(len(parts)):
                if "-" in parts[i]:
                    parts[i] = parts[i].split("-")

            for i in range(len(parts)):
                parts[i] = precalculator(parts[i])

            result = sum(parts)
        except ValueError:
            result = ("Не надо использовать неправильный тип данных")
        except ZeroDivisionError:
            result = ("На нолик мы не делим")

        return result

    def precalculator(part):
        if type(part) is str:
            if "*" in part:
                result = 1
                for subpart in part.split("*"):
                    result *= precalculator(subpart)
                return result
            elif "/" in part:
                parts = list(map(precalculator, part.split("/")))
                result = parts[0]
                for subpart in parts[1:]:
                    result /= subpart
                return result
            else:
                return float(part)
        elif type(part) is list:
            for i in range(len(part)):
                part[i] = precalculator(part[i])
            return part[0] - sum(part[1:])

    update.message.reply_text(calculator(string_to_calc))


if __name__ == '__main__':
    main()

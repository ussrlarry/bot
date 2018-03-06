from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import time
import logging
from datetime import datetime
import random

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
    dp.add_handler(CommandHandler("ask_moon", next_fullmoon))
    dp.add_handler(CommandHandler("wordcount", word_counter))
    dp.add_handler(CommandHandler("dict_calc", dict_calculator))
    dp.add_handler(CommandHandler("simple_calc", simple_calculator))
    dp.add_handler(CommandHandler("goroda", goroda))

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

def next_fullmoon(bot, update):
    user_text_get = update.message.text
    cutted_user_input = user_text_get[10:]
    remove_quotas = cutted_user_input[1:-1]
    string_to_list = remove_quotas.split()
    get_date = (string_to_list[-1])[0:-1]
    user_date = datetime.strptime(get_date, '%Y-%m-%d')
    final_date = str(datetime.strftime(user_date, '%Y/%m/%d'))
    result = str(ephem.next_full_moon(final_date))
    update.message.reply_text(result)

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

def goroda(bot, update):
    cities = ['абакан', 'азов', 'александров', 'алексин', 'альметьевск', 'анапа', 'ангарск', 'анжеро-судженск', 'апатиты', 'арзамас', 'армавир', 'арсеньев', 'артем', 'архангельск', 'асбест', 'астрахань', 'ачинск', 'балаково', 'балахна',
    'балашиха', 'балашов', 'барнаул', 'батайск', 'белгород', 'белебей', 'белово', 'белогорск', 'белорецк', 'белореченск', 'бердск', 'березники', 'березовский', 'бийск', 'биробиджан', 'благовещенск', 'бор', 'борисоглебск', 'боровичи', 'братск', 'брянск', 'бугульма', 'буденновск', 'бузулук',
    'буйнакск', 'великие', 'великий', 'верхняя', 'видное', 'владивосток', 'владикавказ', 'владимир', 'волгоград', 'волгодонск', 'волжск', 'волжский', 'вологда', 'вольск', 'воркута', 'воронеж', 'воскресенск', 'воткинск', 'всеволожск', 'выборг', 'выкса', 'вязьма', 'гатчина', 'геленджик', 'георгиевск',
    'глазов', 'горно-алтайск', 'грозный', 'губкин', 'гудермес', 'гуково', 'гусь-хрустальный', 'дербент', 'дзержинск', 'димитровград', 'дмитров', 'долгопрудный', 'домодедово', 'донской', 'дубна', 'евпатория', 'егорьевск', 'ейск', 'екатеринбург', 'елабуга', 'елец', 'ессентуки', 'железногорск', 'железногорск', 'жигулевск',
    'жуковский', 'заречный', 'зеленогорск', 'зеленодольск', 'златоуст', 'иваново', 'ивантеевка', 'ижевск', 'избербаш', 'иркутск', 'искитим', 'ишим', 'ишимбай', 'йошкар-ола', 'казань', 'калининград', 'калуга', 'каменск-уральский', 'каменск-шахтинский', 'камышин', 'канск', 'каспийск', 'кемерово', 'керчь', 'кинешма',
    'кириши', 'киров', 'кирово-чепецк', 'киселевск', 'кисловодск', 'клин', 'клинцы', 'ковров', 'когалым', 'коломна', 'комсомольск-на-амуре', 'копейск', 'королев', 'кострома', 'котлас', 'красногорск', 'краснодар', 'краснокаменск', 'краснокамск', 'краснотурьинск', 'красноярск', 'кропоткин', 'крымск', 'кстово', 'кузнецк',
    'кумертау', 'кунгур', 'курган', 'курск', 'кызыл', 'лабинск', 'лениногорск', 'ленинск-кузнецкий', 'лесосибирск', 'липецк', 'лиски', 'лобня', 'лысьва', 'лыткарино', 'люберцы', 'магадан', 'магнитогорск', 'майкоп', 'махачкала', 'междуреченск', 'мелеуз', 'миасс', 'минеральные', 'минусинск', 'михайловка',
    'михайловск', 'мичуринск', 'москва', 'мурманск', 'муром', 'мытищи', 'набережные', 'назарово', 'назрань', 'нальчик', 'наро-фоминск', 'находка', 'невинномысск', 'нерюнгри', 'нефтекамск', 'нефтеюганск', 'нижневартовск', 'нижнекамск', 'нижний', 'нижний', 'новоалтайск', 'новокузнецк', 'новокуйбышевск', 'новомосковск', 'новороссийск',
    'новосибирск', 'новотроицк', 'новоуральск', 'новочебоксарск', 'новочеркасск', 'новошахтинск', 'новый', 'ногинск', 'норильск', 'ноябрьск', 'нягань', 'обнинск', 'одинцово', 'озерск', 'октябрьский', 'омск', 'орел', 'оренбург', 'орехово-зуево', 'орск', 'павлово', 'павловский', 'пенза', 'первоуральск', 'пермь',
    'петрозаводск', 'петропавловск-камчатский', 'подольск', 'полевской', 'прокопьевск', 'прохладный', 'псков', 'пушкино', 'пятигорск', 'раменское', 'ревда', 'реутов', 'ржев', 'рославль', 'россошь', 'ростов-на-дону', 'рубцовск', 'рыбинск', 'рязань', 'салават', 'сальск', 'самара', 'санкт-петербург', 'саранск', 'сарапул',
    'саратов', 'саров', 'свободный', 'севастополь', 'северодвинск', 'северск', 'сергиев', 'серов', 'серпухов', 'сертолово', 'сибай', 'симферополь', 'славянск-на-кубани', 'смоленск', 'соликамск', 'солнечногорск', 'сосновый', 'сочи', 'ставрополь', 'старый', 'стерлитамак', 'ступино', 'сургут', 'сызрань', 'сыктывкар',
    'таганрог', 'тамбов', 'тверь', 'тимашевск', 'тихвин', 'тихорецк', 'тобольск', 'тольятти', 'томск', 'троицк', 'туапсе', 'туймазы', 'тула', 'тюмень', 'узловая', 'улан-удэ', 'ульяновск', 'урус-мартан', 'усолье-сибирское', 'уссурийск', 'усть-илимск', 'уфа', 'ухта', 'феодосия', 'фрязино',
    'хабаровск', 'ханты-мансийск', 'хасавюрт', 'химки', 'чайковский', 'чапаевск', 'чебоксары', 'челябинск', 'черемхово', 'череповец', 'черкесск', 'черногорск', 'чехов', 'чистополь', 'чита', 'шадринск', 'шали', 'шахты', 'шуя', 'щекино', 'щелково', 'электросталь', 'элиста', 'энгельс', 'южно-сахалинск',
    'юрга', 'якутск', 'ялта', 'ярославль']

    user_city = update.message.text[8:].lower()
    cities_diff = []
    cities_final = list(set(cities + cities_diff))

    def city_answers(ask_bot):

        answers = []
        cities_diff.append(user_city)

        for i in cities_final:
            if i.startswith(user_city[-1]):
                answers.append(i)

        answer_to_user = random.choice(answers)
        cities_diff.append(answer_to_user)
        return answer_to_user
    print (len(cities_final))

    update.message.reply_text(city_answers(user_city))



if __name__ == '__main__':
    main()

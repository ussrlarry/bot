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

if __name__ == '__main__':
    main()

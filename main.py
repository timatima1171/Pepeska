from telebot import types
import telebot
import datetime
import sqlite3
import random
import datetime

# from flask import Flask, request

token = '5159768808:AAFhfoTW7lL-YGD5jkKyTdGp1L5Rl3vlb_I'
# app = Flask(__name__)

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def inf(message):
    conn = sqlite3.connect('pepeska.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO users VALUES (?,?,?,?) ON CONFLICT (userid) DO NOTHING;''',
                (message.from_user.id, f"{message.from_user.first_name}", 0, datetime.datetime.now()))

    conn.commit()
    cur.close()

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Начать мерить', callback_data='begin')
    button2 = types.InlineKeyboardButton('Топ', callback_data='top')

    markup.row(button1, button2)

    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'begin')
    def callback_inline_first(call):
        pass

    @bot.callback_query_handler(func=lambda call: call.data == 'top')
    def callback_inline_first(call):
        conn = sqlite3.connect('pepeska.db')
        cur = conn.cursor()
        pisyun = random.randint(-3, 10)
        cur.execute('''SELECT * FROM users order by size''')
        top=cur.fetchall()
        print()
        bot.send_message(call.message.chat.id, f' {top[-1][1]} его размер:{top[-1][2]} \n {top[-2][1]} его размер:{top[-2][2]} \n {top[-3][1]} его размер:{top[-3][2]} \n {top[-4][1]} его размер:{top[-4][2]} \n ')
        conn.commit()
        cur.close()


@bot.message_handler(content_types=['text'])
def number(message):
    try:
        if message.text == '1':
            conn = sqlite3.connect('pepeska.db')
            cur = conn.cursor()

            cur.execute('''SELECT * FROM users WHERE userid=?''', (message.from_user.id,))
            total = cur.fetchall()
            cur.execute('''SELECT users.time from users where userid=?''', (message.from_user.id,))
            extime = cur.fetchone()
            now = datetime.datetime.now()
            extime = datetime.datetime.fromisoformat(extime[0])
            timer = now - extime
            xd = datetime.timedelta(minutes=30)
            if not (len(str(total[0][0]))) == 0 and timer > xd:
                ran = random.randint(-5, 5)
                cur.execute('''UPDATE users set time=?''', (datetime.datetime.now(),))
                conn.commit()
                if ran > 0:
                    bot.send_message(message.chat.id, f'Твой писюн увеличился на {ran}')
                elif ran == 0:
                    bot.send_message(message.chat.id, f'Стручек не на что не увеличился')
                else:
                    bot.send_message(message.chat.id, f'Твой писюн уменьшился на {ran}')
                a = total[0][2] + ran

                cur.execute('''UPDATE users SET size=?''', (a,))
                conn.commit()
                cur.close()
                bot.send_message(message.chat.id, f'Теперь твой песюн: {a}')
            else:
                bot.send_message(message.chat.id, f"Возвращайся через: {xd - timer}")
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, "Для начала нажмите на /start")


bot.remove_webhook()
# bot.set_webhook('https://test.com/' + token)
# app.run()
bot.polling(interval=0, none_stop=True)

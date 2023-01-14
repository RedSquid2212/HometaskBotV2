import telebot
import sqlite3
from telebot import types


TOKEN = '5393072938:AAFcdGoWWpJjhubq5dT1ThOo9ITHT0d_HZQ'
bot = telebot.TeleBot(TOKEN)
connection = sqlite3.connect(r'C:\Users\79126\Documents\database.db', check_same_thread=False)
cursor = connection.cursor()
new_message = ''
subjects = ['Дискретка', 'Сети', 'Матан', 'Тервер', 'ООП', 'Python']
current_subject = ''
subject_for_extracting = ''
task = ''
deadline = ''
annotation = ''''''


def db_set_table_value(task: str, deadline: str, subject: str):
    cursor.execute(f'INSERT INTO {subject} (Задание, Дедлайн) VALUES (?, ?)', (task, deadline))
    connection.commit()


def db_get_table_value(subject: str):
    cursor.execute(f'SELECT Задание, Дедлайн FROM {subject};')
    results = cursor.fetchall()
    print(results)
    return results


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать предмет")
    btn2 = types.KeyboardButton("Все задания")
    btn3 = types.KeyboardButton("Добавить задание")
    btn4 = types.KeyboardButton("Создать напоминалку")
    btn5 = types.KeyboardButton("Настройки")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, text='Тут будет список всех доступных команд', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def ask_subject(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Дискретка")
    btn2 = types.KeyboardButton("Сети")
    btn3 = types.KeyboardButton("Матан")
    btn4 = types.KeyboardButton("Тервер")
    btn5 = types.KeyboardButton("ООП")
    btn6 = types.KeyboardButton("Python")
    back = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)

    if message.text == 'Добавить задание':
        bot.send_message(message.chat.id, text='Выбери предмет', reply_markup=markup)
        bot.register_next_step_handler(message, ask_task)
    elif message.text == 'Выбрать предмет':
        bot.send_message(message.chat.id, text='Выбери предмет, и я скажу тебе задания', reply_markup=markup)
        bot.register_next_step_handler(message, ask_current_subject)
    elif message.text == 'Все задания':
        bot.register_next_step_handler(message, get_all_tasks)
    elif message.text == 'Вернуться в главное меню':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn7 = types.KeyboardButton("Выбрать предмет")
        btn8 = types.KeyboardButton("Все задания")
        btn9 = types.KeyboardButton("Добавить задание")
        btn10 = types.KeyboardButton("Создать напоминалку")
        btn11 = types.KeyboardButton("Настройки")
        markup2.add(btn7, btn8, btn9, btn10, btn11)
        bot.send_message(message.chat.id, text='Окей! Сейчас ты в главном меню', reply_markup=markup2)


def get_all_tasks(message):
    result = ''
    for s in subjects:
        result += s + ':' + '\n'
        result += '\n'
        res = ''
        res1 = db_get_table_value(s)

        for t in res1:
            result_string = '- ' + t[0] + f' ({t[1]})'
            res += result_string + '\n'

        result += res

    bot.send_message(message.chat.id, text=result)


def ask_current_subject(message):
    global subject_for_extracting
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отметить задание выполненным')
    btn2 = types.KeyboardButton('Вернуться в главное меню')
    markup.add(btn1, btn2)

    if message.text in subjects:
        subject_for_extracting = message.text
        result = db_get_table_value(subject_for_extracting)
        res = ''

        for t in result:
            result_string = '- ' + t[0] + f' ({t[1]})'
            res += result_string + '\n'

        bot.send_message(message.chat.id, text=res, reply_markup=markup)
        bot.register_next_step_handler(message, ask_subject)


def ask_task(message):
    global current_subject
    if message.text in subjects:
        current_subject = message.text
        bot.send_message(message.chat.id, text='Введи задание')
        bot.register_next_step_handler(message, set_task_for_subject)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выбрать предмет")
        btn2 = types.KeyboardButton("Все задания")
        btn3 = types.KeyboardButton("Добавить задание")
        btn4 = types.KeyboardButton("Создать напоминалку")
        btn5 = types.KeyboardButton("Настройки")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text='Окей! Сейчас ты в главном меню', reply_markup=markup)


def set_task_for_subject(message):
    global task
    task = message.text
    bot.send_message(message.chat.id, text='Введи дату, к которой нужно выполнить задание (в формате ДД.ММ.ГГ)')
    bot.register_next_step_handler(message, set_deadline_for_subject)


def set_deadline_for_subject(message):
    global task
    global deadline
    global current_subject
    deadline = message.text
    db_set_table_value(task, deadline, current_subject)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать предмет")
    btn2 = types.KeyboardButton("Все задания")
    btn3 = types.KeyboardButton("Добавить задание")
    btn4 = types.KeyboardButton("Создать напоминалку")
    btn5 = types.KeyboardButton("Настройки")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id,
                     text='Задание принято! Теперь ты сможешь без проблем найти его', reply_markup=markup)


bot.polling(none_stop=True, interval=0)

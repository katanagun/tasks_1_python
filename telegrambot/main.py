from db_connection import create_connection, close_connection
import bot_func
import telebot
from telebot import types

# Константы для состояния пользователя
STATE_NAME = 0
STATE_DATE = 1
STATE_START_TIME = 2
STATE_END_TIME = 3
STATE_EVENT_NAME = 4
STATE_MEMBERS = 5

# Функции для обработки сообщений
def start(message):
    bot.send_message(message.chat.id, 'Введите имя и фамилию через пробел')
    user_state[message.chat.id] = STATE_NAME

def get_name(message):
    user_input = message.text.split()
    if len(user_input) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, введите имя и фамилию через пробел.')
        return

    id_tg = message.from_user.id
    user_data[message.chat.id] = {'user_id': id_tg, 'first_name': user_input[0], 'last_name': user_input[1]}

    if not bot_func.check_user(user_data[message.chat.id]['user_id']):
        bot_func.create_user(user_data[message.chat.id]['last_name'], user_data[message.chat.id]['first_name'], user_data[message.chat.id]['user_id'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Создать событие'))
    bot.send_message(message.chat.id, 'Нажмите "Создать событие" для начала', reply_markup=markup)
    user_state[message.chat.id] = None

def create_event(message):
    id_tg = message.from_user.id
    user_data.setdefault(message.chat.id, {'user_id': id_tg})
    bot.send_message(message.chat.id, 'Введите дату события (например, 2024-12-30)')
    user_state[message.chat.id] = STATE_DATE

def get_date(message):
    user_data[message.chat.id]['date'] = message.text
    bot.send_message(message.chat.id, 'Введите время начала события (например, 14:00)')
    user_state[message.chat.id] = STATE_START_TIME

def get_start_time(message):
    user_data[message.chat.id]['start_time'] = message.text
    bot.send_message(message.chat.id, 'Введите время окончания события (например, 16:00)')
    user_state[message.chat.id] = STATE_END_TIME

def get_end_time(message):
    user_data[message.chat.id]['end_time'] = message.text
    bot.send_message(message.chat.id, 'Введите название события')
    user_state[message.chat.id] = STATE_EVENT_NAME

def get_event_name(message):
    user_data[message.chat.id]['event_name'] = message.text
    bot.send_message(message.chat.id, 'Введите имя и фамилию пользователей через запятую')
    user_state[message.chat.id] = STATE_MEMBERS

def get_members(message):
    members = [name.strip() for name in message.text.split(',')]
    id_tg = message.from_user.id
    user_send_message = bot_func.get_users_id(members)
    user_ids = user_send_message.copy()
    user_ids.append(id_tg)
    users = bot_func.get_user_name(user_send_message)
    users_string = ", ".join([f"{user[0]} {user[1]}" for user in users])
    event = bot_func.create_event(user_data[message.chat.id]['date'], user_data[message.chat.id]['start_time'], user_data[message.chat.id]['end_time'], user_data[message.chat.id]['event_name'], user_ids)
    if event:
        bot.send_message(message.chat.id, f"Событие создано:\n{user_data[message.chat.id]['event_name']}\nДата: {user_data[message.chat.id]['date']}\nВремя начала: {user_data[message.chat.id]['start_time']}\nВремя окончания: {user_data[message.chat.id]['end_time']}\nУчастники: {users_string}")

        for user_id in user_send_message:
            bot.send_message(user_id, f"Вам назначено новое событие:\n{user_data[message.chat.id]['event_name']}\nДата: {user_data[message.chat.id]['date']}\nВремя начала: {user_data[message.chat.id]['start_time']}\nВремя окончания: {user_data[message.chat.id]['end_time']}\nУчастники: {users_string}")

        user_state[message.chat.id] = None

if __name__ == '__main__':
    db_config = {
        "db_name": "postgres",
        "db_user": "postgres",
        "db_password": "password",
        "db_host": "localhost",
        "db_port": "5432"
    }

    conn = None
    try:
        conn = create_connection(**db_config)
        bot_func = bot_func.Bot_func(conn)
        bot = telebot.TeleBot("7648621881:AAF-7OGKQlkzSF6ngKYvw6uLLfvg8LxQ7wY")
        user_data = {}
        user_state = {}

        bot.message_handler(commands=['start'])(start)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_NAME)(get_name)
        bot.message_handler(func=lambda message: message.text == 'Создать событие')(create_event)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_DATE)(get_date)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_START_TIME)(get_start_time)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_END_TIME)(get_end_time)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_EVENT_NAME)(get_event_name)
        bot.message_handler(func=lambda message: user_state.get(message.chat.id) == STATE_MEMBERS)(get_members)

        bot.infinity_polling()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if conn:
            close_connection(conn)

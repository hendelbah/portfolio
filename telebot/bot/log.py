from bot import Config
import datetime


def log(log_data):
    with open(Config.LOG_PATH, 'a') as file:
        entry = ('{time}\nChat id: {chat_id}, Chat title: {chat_title}\n'
                 'User id: {user_id}, Username: @{username}\n{content}\n\n').format(**log_data)
        file.write(entry)


def log_message(message):
    log_data = {
        'time': datetime.datetime.fromtimestamp(message.date),
        'chat_id': message.chat.id,
        'chat_title': message.chat.title,
        'user_id': message.from_user.id,
        'username': message.from_user.username
    }
    if message.content_type == 'text':
        log_data['content'] = message.text
    elif message.content_type == 'sticker':
        log_data['content'] = 'Sticker: ' + message.sticker.file_id
    elif message.content_type == 'photo':
        log_data['content'] = f'''Photo: {message.photo[-1].file_id}\nCaption: {message.caption}'''
    else:
        log_data['content'] = '-'
    log(log_data)


def log_call(call):
    log_data = {
        'time': datetime.datetime.now(),
        'chat_id': call.message.chat.id,
        'chat_title': call.message.chat.title,
        'user_id': call.from_user.id,
        'username': call.from_user.username,
        'content': f'Callback: "{call.data}"'
    }
    log(log_data)


def log_error(exception, user_id=None, username=None, chat_id=None, chat_title=None, e_type='TeleBot'):
    log_data = {
        'time': datetime.datetime.now(),
        'chat_id': chat_id,
        'chat_title': chat_title,
        'user_id': user_id,
        'username': username,
        'content': f'{e_type} error occurred: "{exception.__class__.__name__}: {exception.args[0]}"'
    }
    log(log_data)
    if Config.DEBUG >= 6:
        raise exception
    elif Config.DEBUG >= 1:
        print(log_data['content'])

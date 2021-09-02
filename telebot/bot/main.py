from telebot import apihelper
from bot import Config, log
from bot.sql import SQL
from bot.my_telebot import TeleBot, Keyboard

apihelper.ENABLE_MIDDLEWARE = True

bot = TeleBot(Config.TOKEN)


@bot.middleware_handler(update_types=['message'])
def modify_message(self, message):
    if message.chat.type == 'private':
        db = SQL()
        log.log_message(message)
        if message.chat.type == 'private' and message.from_user.id in self.forward:
            self.forward_message(self.forward_to, message.chat.id, message.id)
        if message.content_type == 'text':
            message.text_low = message.text.lower()
            message.text = message.text[0:800]
        message.user_data = db.handle_user(message.from_user)
        message.user_queries = db.get_user_active_queries(message.from_user.id)
        if Config.DEBUG >= 4:
            print(message)
        elif Config.DEBUG >= 2:
            print(message.text)


# noinspection PyUnusedLocal
@bot.middleware_handler(update_types=['callback_query'])
def modify_callback_query(self, call):
    db = SQL()
    log.log_call(call)
    call.user_data = db.handle_user(call.from_user)
    call.user_queries = db.get_user_active_queries(call.from_user.id)
    call.command = call.data.split('_')
    if Config.DEBUG >= 4:
        print(call)
    elif Config.DEBUG >= 2:
        print(call.data)


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'audio', 'document', 'animation', 'video', 'voice'],
                     func=lambda message: message.chat.type == 'private')
def get_private_messages(message):
    db = SQL()
    message.db = db
    if message.content_type == 'text' and message.text[0] == '/' and bot.command_handle(message):
        return
    user = message.from_user.id
    sp_messages = message.user_data[2]
    sp_string = message.user_data[3]

    curent_stage = TeleBot.get_reagent_current_stage(sp_string)
    delete = True
    if curent_stage:
        if curent_stage == 'photo':
            if message.content_type == 'photo':
                delete = False
                sp_string += f'•p{message.photo[-1].file_id}'
                bot.delete_special_message(user, sp_messages)
                text = ('Отправь пожалуйста необходимый вес в грамах '
                        '(числом без лишних символов, десятичные дроби разрешены)')
                markup = Keyboard.special_reagent_find(skip=False)
                sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
            else:
                bot.send_message(user, 'Неверный формат, нужно обычное сжатое фото')
        else:
            if message.content_type == 'text':
                message.text = message.text.replace('•', '*')
                if any([word in message.text_low for word in Config.SWEAR_LIST]):
                    bot.send_message(user, 'Пиво может быть и не фильтрованым, но базар обязан быть таковым.')
                if curent_stage == 'name':
                    delete = False
                    sp_string += f'•n{message.text}'
                    bot.delete_special_message(user, sp_messages)
                    text = 'Отправь пожалуйста фото со структурой (не как файл)'
                    markup = Keyboard.special_reagent_find()
                    sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
                elif curent_stage == 'amount':
                    text = message.text.replace(',', '.')
                    try:
                        amount = round(float(text) * 1000)
                    except ValueError:
                        bot.send_message(user, 'Значение не подходит')
                    else:
                        delete = False
                        sp_string += f'•a{amount}'
                        bot.delete_special_message(user, sp_messages)
                        text = 'Отпавь дополнительную информацию: какой корпус, с возвратом или нет... '
                        markup = Keyboard.special_reagent_find()
                        sp_messages = [bot.send_message(user, text, parse_mode='HTML', reply_markup=markup).id]
                elif curent_stage == 'info':
                    delete = False
                    sp_string += f'•i{message.text}'
                    sp_messages = bot.reagent_send_finish(sp_string, user, sp_messages)
            else:
                bot.send_message(user, 'Неверный формат, подходит только текст')
    else:
        if message.content_type == 'sticker':
            delete = not bot.sticker_handle(message)
    if delete:
        bot.delete_message(user, message.id)
    else:
        db.update_specials(user, sp_messages, sp_string)


@bot.message_handler(content_types=['text', 'sticker'],
                     func=lambda message: message.chat.type == 'group' and not message.from_user.is_bot)
def get_group_messages(message):
    db = SQL()
    message.db = db
    parsed = False
    delete = True
    if message.content_type == 'text':
        text_low = message.text.lower()
        if text_low[0] == '/' and message.from_user.id in bot.main_chat_admin_ids:
            if text_low.startswith('/show'):
                queries = db.get_reagents_active_queries()
                if queries:
                    for query in queries:
                        bot.reagent_send_query(
                            message.chat.id, query, mode='group')
                else:
                    bot.send_message(message.chat.id, 'Пока запросов нет')
                parsed = True
            if text_low.startswith('/updatechat'):
                bot.update_main_chat_data()
                parsed = True
        pass
    if message.content_type == 'sticker':
        message.user_data = db.handle_user(message.from_user)
        message.user_queries = db.get_user_active_queries(message.from_user.id)
        parsed = bot.sticker_handle(message)
        delete = message.user_data[0]
    if parsed:
        if delete:
            bot.delete_message(message.chat.id, message.id)
        log.log_message(message)
        if Config.DEBUG >= 4:
            print(message)
        elif Config.DEBUG >= 2:
            print(message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    db = SQL()
    call.db = db
    user = call.from_user.id
    if call.command[0] == 'd':
        sp_string, sp_messages = default_query_handler(call)
    elif call.command[0] == 's':
        sp_string, sp_messages = special_query_handler(call)
    else:
        sp_messages = call.user_data[2]
        sp_string = call.user_data[3]
    if Config.DEBUG >= 3:
        print(sp_string)
    if Config.DEBUG >= 1:
        print()
    db.update_specials(user, sp_messages, sp_string)


def default_query_handler(call):
    user = call.from_user.id
    if call.message.id != call.user_data[1]:
        bot.delete_message(user, call.message.id)
    bot.delete_special_message(user, call.user_data[2])
    sp_string = ''
    sp_messages = []
    if call.command[1] == 'meal':
        if call.command[2] == 'get' and not call.user_queries[0]:
            sp_string = 'meal_get'
            text = 'Какой обед хочешь?'
            markup = Keyboard.special_meal()
            sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
        elif call.command[2] == 'give' and not call.user_queries[0]:
            sp_string = 'meal_give'
            text = 'А какой обед у тебя есть?'
            markup = Keyboard.special_meal(False)
            sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
        elif call.command[2] == 'cancel' and call.user_queries[0]:
            sp_string = 'meal_cancel'
            text = 'Уверен?'
            markup = Keyboard.special_finish()
            sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
    elif call.command[1] == 'reagent':
        if call.command[2] == 'find':
            sp_string = 'reagent_find'
            text = 'Отправь пожалуйста название/формулу нужного соединения'
            markup = Keyboard.special_reagent_find()
            sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
        elif call.command[2] == 'check':
            sp_string = ''
            queries = call.db.get_reagents_active_queries()
            if queries:
                sp_messages = []
                for query in queries:
                    sp_message = bot.reagent_send_query(user, query)
                    if sp_message:
                        sp_messages.append(sp_message)
            else:
                sp_messages = []
                bot.send_message(user, 'Пока запросов нет')
        elif call.command[2] == 'cancel':
            sp_string = 'reagent_cancel'
            text = 'Уверен?'
            markup = Keyboard.special_finish()
            sp_messages = [bot.send_message(user, text, reply_markup=markup).id]
    return sp_string, sp_messages


def special_query_handler(call):
    user = call.from_user.id
    sp_messages = call.user_data[2]
    sp_string = call.user_data[3]
    if call.message.chat.type == 'private' and call.message.id not in sp_messages:
        bot.delete_message(user, call.message.id)
    if call.command[1] == 'meal':
        if call.command[2] == 'any' and sp_string == 'meal_get':
            text = 'Встать в очередь за обедами (любой)'
            markup = Keyboard.special_finish()
            bot.edit_special_message(text, user, sp_messages, markup)
            sp_string += '•any'
        elif call.command[2] == 'full':
            text = 'Обшибка'
            if sp_string == 'meal_get':
                text = 'Встать в очередь за обедами (обязательно с первым)'
            if sp_string == 'meal_give':
                text = 'Отдаешь полный обед'
            markup = Keyboard.special_finish()
            bot.edit_special_message(text, user, sp_messages, markup)
            sp_string += '•full'
        elif call.command[2] == 'nosoup':
            text = 'Обшибка'
            if sp_string == 'meal_get':
                text = 'Встать в очередь за обедами (обязательно без первого)'
            if sp_string == 'meal_give':
                text = 'Отдаешь обед без первого'
            markup = Keyboard.special_finish()
            bot.edit_special_message(text, user, sp_messages, markup)
            sp_string += '•nosoup'
    elif call.command[1] == 'reagent':
        if call.command[2] == 'skip':
            curent_stage = TeleBot.get_reagent_current_stage(sp_string)
            if curent_stage == 'name':
                sp_string += '•n_'
                text = 'Тогда отправь хотя бы фото со структурой (не как файл)'
                markup = Keyboard.special_reagent_find(skip=False)
                bot.edit_special_message(text, user, sp_messages, markup)
            elif curent_stage == 'photo':
                if sp_string.split('•')[1][1:] == '_':
                    bot.send_message(
                        user, 'Фотография обязательна при отсутствии названия')
                else:
                    sp_string += '•p_'
                    text = ('Отправь пожалуйста необходимый вес в грамах '
                            '(числом без лишних символов, десятичные дроби разрешены)')
                    markup = Keyboard.special_reagent_find(skip=False)
                    bot.edit_special_message(
                        text, user, sp_messages, markup)
            elif curent_stage == 'info':
                sp_string += '•i_'
                sp_messages = bot.reagent_send_finish(
                    sp_string, user, sp_messages)
            else:
                bot.send_message(user, 'Невозможно пропустить')
        elif call.command[2] == 'pick':
            query_id = int(call.command[3])
            query = call.db.get_reagents_query(query_id)
            if query[1] != user and query[3]:
                sp_string = f'reagent_pick•{query_id}'
                bot.delete_special_message(user, sp_messages)
                sp_messages = [
                    bot.reagent_send_query(user, query, prefix='Подтверди, что готов поделиться:', mode='finish')]
            else:
                if not query[3]:
                    bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(user, 'Действие невозможно')
    elif call.command[1] == 'end':
        if call.command[2] == 'confirm':  # parsing final query
            confirm_query_handler(call, sp_string)
        elif call.command[2] == 'cancel':
            if len(sp_string.split('•')) > 2:
                bot.send_default_message(call)
        bot.delete_special_message(user, call.user_data[2])
        sp_messages = []
    return sp_string, sp_messages


def confirm_query_handler(call, sp_string):
    user = call.from_user.id
    parsed = False
    sp_list = sp_string.split('•') if sp_string else []
    if len(sp_list) == 1:
        if sp_list[0] == 'meal_cancel':
            for query_id in call.user_queries[0]:
                call.db.update_query(query_id, 'meals')
            call.user_queries = ([], call.user_queries[1])
            parsed = True
        elif sp_list[0] == 'reagent_cancel':
            for query_id in call.user_queries[1]:
                call.db.update_query(query_id, 'reagents')
            call.user_queries = (call.user_queries[0], [])
            parsed = True
    elif len(sp_list) == 2:
        if sp_list[0] == 'meal_get' and sp_list[1] in ['any', 'full', 'nosoup']:
            if not call.user_queries[0]:
                call.db.add_meals(user, sp_list[1])
            else:
                bot.send_message(user, 'Ты уже в очереди')
            parsed = True
        elif sp_list[0] == 'meal_give' and sp_list[1] in ['full', 'nosoup']:
            queue = call.db.get_meals_queue()
            target = ()
            for meal_query in queue:
                if meal_query[4] == 'all' or meal_query[4] == sp_list[1]:
                    target = meal_query
                    break
            if target:
                if target[1] != user:
                    meal_user = call.db.get_user_names(target[1])
                    m = f'Твой обед заберет <a href="tg://user?id={meal_user[0]}">@{meal_user[1]}</a>'
                    bot.send_message(user, m)
                    m = f'Можешь забрать обед у <a href="tg://user?id={user}">@{call.from_user.username}</a>'
                    bot.send_message(meal_user[0], m)
                else:
                    bot.send_message(user, 'Ну вот сам свой обед и ешь.')
                call.db.update_query(target[0], 'meals', user)
            else:
                bot.send_message(user, 'Не нашлось никого кто хотел бы твой обед(')
            parsed = True
        elif sp_list[0] == 'reagent_pick':
            try:
                reagents_id = int(sp_list[1])
            except ValueError as exc:
                log.log_error(exc, user_id=call.from_user.id, username=call.from_user.username,
                              chat_id=call.message.chat.id, e_type='parser')
            else:
                reagents_user = call.db.get_reagents_user(reagents_id)
                if reagents_user:
                    if reagents_user[0] != user:
                        bot.send_message(user, f'<a href="tg://user?id={reagents_user[0]}">'
                                               f'Напиши @{reagents_user[1]}</a>')
                        bot.send_message(reagents_user[0], f'<a href="tg://user?id={user}">'
                                                           f'Речовинка нашлась у: @{call.from_user.username}</a>')
                        call.db.update_query(reagents_id, 'reagents', user)
                    else:
                        bot.send_message(user, 'Нельзя самому себе это делать')
                    parsed = True
    elif len(sp_list) == 5 and sp_list[0] == 'reagent_find' and all(
            len(item) > 1 and item[0] == char for item, char in zip(sp_list[1:], ['n', 'p', 'a', 'i'])):
        if sp_list[1] == 'n_' and sp_list[2] == 'p_':
            bot.send_message(user, 'Ни названия ни фото')
        else:
            try:
                amount = int(sp_list[3][1:])
            except Exception as exc:
                log.log_error(exc, user_id=call.from_user.id, username=call.from_user.username,
                              chat_id=call.message.chat.id, e_type='parser')
                amount = 0
            name = None if sp_list[1] == 'n_' else sp_list[1][1:]
            photo = None if sp_list[2] == 'p_' else sp_list[2][1:]
            info = None if sp_list[4] == 'i_' else sp_list[4][1:]
            call.db.add_reagents(user, name, photo, amount, info)
            parsed = True
    if parsed:
        bot.send_default_message(call, mode='e')
    else:
        bot.send_message(user, 'Произошла ошибка')


try:
    bot.polling(none_stop=True)
except BaseException as e:
    bot.send_message(353360159, f'{type(e).__name__}: {e}')
    raise e

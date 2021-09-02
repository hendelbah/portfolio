import telebot
from telebot import types
from bot import Config, log
from bot.sql import SQL


class Keyboard(types.InlineKeyboardMarkup):
    # keys for default message
    # meal section
    key_meal_give = types.InlineKeyboardButton(
        text='Отдам обед...', callback_data='d_meal_give')
    key_meal_get = types.InlineKeyboardButton(
        text='Ищу обед...', callback_data='d_meal_get')
    key_meal_cancel = types.InlineKeyboardButton(
        text='Обед больше ненужен', callback_data='d_meal_cancel')
    # reagent section
    key_reagent_find = types.InlineKeyboardButton(
        text='Ищу реактив...', callback_data='d_reagent_find')
    key_reagent_check = types.InlineKeyboardButton(
        text='Посмотреть что ищут', callback_data='d_reagent_check')
    key_reagent_cancel = types.InlineKeyboardButton(
        text='Отменить поиск речовынки', callback_data='d_reagent_cancel')
    # keys for special message
    # setting meal type
    key_meal_any = types.InlineKeyboardButton(
        text='Любой сойдет', callback_data='s_meal_any')
    key_meal_full = types.InlineKeyboardButton(
        text='Только полный', callback_data='s_meal_full')
    key_meal_nosoup = types.InlineKeyboardButton(
        text='Только без первого', callback_data='s_meal_nosoup')
    # skip options for reagent query
    key_reagent_skip = types.InlineKeyboardButton(
        text='Пропустить', callback_data='s_reagent_skip')
    # end query
    key_end_confirm = types.InlineKeyboardButton(
        text='Да, подтверждаю', callback_data='s_end_confirm')
    key_end_cancel = types.InlineKeyboardButton(
        text='Отмена', callback_data='s_end_cancel')

    @classmethod
    def default(cls, params=None):
        if params is None:
            params = [0, 0]
        meal_keyboard = [cls.key_meal_cancel] if params[0] else [
            cls.key_meal_give, cls.key_meal_get]
        reagent_keyboard = [cls.key_reagent_cancel if params[1] else cls.key_reagent_find, cls.key_reagent_check]
        return cls(keyboard=[meal_keyboard, reagent_keyboard], row_width=2)

    @classmethod
    def special_finish(cls):
        return cls(keyboard=[[cls.key_end_confirm, cls.key_end_cancel]], row_width=2)

    @classmethod
    def special_meal(cls, get=True):
        keyboard = [[cls.key_meal_full, cls.key_meal_nosoup],
                    [cls.key_end_cancel]]
        if get:
            return cls(keyboard=[[cls.key_meal_any]] + keyboard, row_width=2)
        else:
            return cls(keyboard=keyboard, row_width=2)

    @classmethod
    def special_reagent_check(cls, query_id, cancel=True):
        key = types.InlineKeyboardButton(
            text='Могу поделиться', callback_data=f's_reagent_pick_{query_id}')
        if cancel:
            return cls(keyboard=[[key, cls.key_end_cancel]])
        else:
            return cls(keyboard=[[key]])

    @classmethod
    def special_reagent_find(cls, skip=True):
        if skip:
            return cls(keyboard=[[cls.key_reagent_skip], [
                cls.key_end_cancel]], row_width=1)
        else:
            return cls(keyboard=[[cls.key_end_cancel]], row_width=1)


class Message(types.Message):
    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None, [], None)


# noinspection SpellCheckingInspection
my_stickers = {
    'pig': 'CAACAgIAAxkBAAO5X_WkIXVBpdRTWBOjhE6oE2pdrx0AAgMAAx_ZDxWRh_LydQABcv4eBA',
    'wednesday': 'CAACAgIAAxkBAAPeX_WqPvRy-DREOpeZfiH_8LeEEq0AAkcBAAK0gEoktibMiBVu2TEeBA',
    'meal': {
        'give': 'CAACAgIAAxkBAAIGB2AG4W0Gz7IiNUYxvRrH508k9KzMAAIMAAMf2Q8VQrXgq3trfzIeBA',
        'cancel': 'CAACAgIAAxkBAAIGDGAG4uP87oUTxNKaHArWK7JgLjSmAAIPAAMf2Q8VqqRBXnfVP5geBA',
        1: 'CAACAgIAAxkBAAIGCGAG4fwXrRlsSXHA7CcQtdz4O53tAAILAAMf2Q8VE12EAoM2c2weBA',
        2: 'CAACAgIAAxkBAAIGCWAG4jJfN8Ll8EgLeeslQPZaKGv9AAINAAMf2Q8VfVWtSVKfqpIeBA',
        3: 'CAACAgIAAxkBAAIGCmAG4kICAgRNigAB7XbQhD47dEKQKgACDgADH9kPFXBp8ynXwPINHgQ',
        4: 'CAACAgIAAxkBAAIGC2AG4nxUG-ChTb1ugxyHCmSnNK5qAAIQAAMf2Q8Vpg0VPvPXN8weBA'
    },
    'meal_unique': {
        'give': 'AgADDAADH9kPFQ',
        'cancel': 'AgADDwADH9kPFQ',
        1: 'AgADCwADH9kPFQ',
        2: 'AgADDQADH9kPFQ',
        3: 'AgADDgADH9kPFQ',
        4: 'AgADEAADH9kPFQ'
    }
}


class TeleBot(telebot.TeleBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db = SQL()
        self.forward = db.get_forwarding()
        self.forward_to = db.get_id(Config.ADMINS[0])
        self.m_to = 0
        self.me = self.get_me()
        self.main_chat = db.chat()
        self.main_chat_admins = []
        self.main_chat_admin_ids = []
        self.update_main_chat_data()
        if Config.DEBUG >= 2:
            db.print_table('users')

    def send_message(self, chat_id, text, *args, **kwargs):
        try:
            message = super().send_message(chat_id, text, *args, **kwargs)
        except Exception as e:
            log.log_error(e, chat_id=chat_id)
            return Message.empty()
        log.log_message(message)
        return message

    def send_sticker(self, chat_id, data, *args, **kwargs):
        try:
            message = super().send_sticker(chat_id, data, *args, **kwargs)
        except Exception as e:
            log.log_error(e, chat_id=chat_id)
            return Message.empty()
        log.log_message(message)
        return message

    def send_photo(self, chat_id, photo, *args, **kwargs):
        try:
            message = super().send_photo(chat_id, photo, *args, **kwargs)
        except Exception as exc:
            log.log_error(exc, chat_id=chat_id)
            return Message.empty()
        log.log_message(message)
        return message

    def delete_message(self, chat_id, message_id, timeout=None):
        try:
            result = super().delete_message(chat_id, message_id, timeout)
        except Exception as exc:
            log.log_error(exc, chat_id=chat_id)
            return None
        return result

    def edit_message_text(self, text, chat_id=None, *args, **kwargs):
        try:
            result = super().edit_message_text(text, chat_id, *args, **kwargs)
        except Exception as e:
            log.log_error(e, chat_id=chat_id)
            return None
        return result

    def edit_message_reply_markup(self, chat_id=None, *args, **kwargs):
        try:
            result = super().edit_message_reply_markup(chat_id, *args, **kwargs)
        except Exception as e:
            log.log_error(e, chat_id=chat_id)
            return None
        else:
            return result

    def update_main_chat_data(self):
        if self.main_chat:
            self.main_chat_admins = self.get_chat_administrators(self.main_chat)
            self.main_chat_admin_ids = [member.user.id for member in self.main_chat_admins]

    def command_handle(self, message):
        text = message.text
        user = message.from_user.id
        if message.from_user.username in Config.ADMINS:
            words = text.split(maxsplit=2)
            if words[0] in ['/m', '/forward', '/setchat']:
                if len(words) < 2:
                    self.send_message(user, 'Not enough parameters')
                    return True
                user_id = self.check_username(words[1], message)
                if words[0] == '/m':
                    if user_id not in [-1, -2]:
                        if len(words) < 3:
                            self.send_message(user, 'Not enough parameters')
                        else:
                            self.m_to = user_id
                            self.send_message(self.m_to, words[2])
                    if user_id == -2:
                        if self.m_to:
                            self.send_message(
                                self.m_to, text.split(maxsplit=1)[1])
                        else:
                            self.send_message(user, 'No user given')
                    return True
                if words[0] == '/forward':
                    if words[1] == '/':
                        self.forward = message.db.clear_forwarding()
                        self.send_message(user, 'Forwarding stopped')
                    else:
                        if user_id not in [-1, -2]:
                            if user_id in self.forward:
                                self.send_message(
                                    user, 'User is allready added')
                                return True
                            self.forward = message.db.add_to_forwarding(user_id)
                            self.send_message(
                                user, f'User {words[1]} added to forwarding list')
                        if user_id == -2:
                            self.send_message(user, 'Invalid username')
                    return True
                if words[0] == '/setchat':
                    try:
                        chat_id = int(words[1])
                    except ValueError:
                        self.send_message(user, 'Invalid chat id')
                    else:
                        self.main_chat = message.db.chat('u', chat_id)
                        self.update_main_chat_data()
                        return True
        if text == "/start":
            self.send_default_message(message, 's')
            self.delete_special_message(user, message.user_data[2])
            message.db.update_specials(user, [])
            return True
        if text == "/help":
            self.send_default_message(message)
            return True
        if text == "/on_inchat":
            self.send_message(user, 'Теперь бот обрабатывает твои сообщения в групповом чате')
            message.db.update_bot_enabled(message.from_user.id, 1)
            return True
        if text == "/off_inchat":
            self.send_message(user, 'В групповом чате бот больше не обращает внимания на тебя')
            message.db.update_bot_enabled(message.from_user.id, 0)
            return True
        return False

    def sticker_handle(self, message):
        result = False
        user = message.from_user.id
        if message.sticker.file_unique_id in my_stickers['meal_unique'].values():
            self.delete_special_message(user, message.user_data[2])
            if message.sticker.file_unique_id == my_stickers['meal_unique']['cancel']:
                if message.user_queries[0]:
                    sp_string = 'meal_cancel'
                    text = 'Чужой обед больше не нужен?'
                    markup = Keyboard.special_finish()
                    sp_messages = [self.send_message(user, text, reply_markup=markup).id]
                    result = True
            elif message.sticker.file_unique_id == my_stickers['meal_unique']['give']:
                if not message.user_queries[0]:
                    sp_string = 'meal_give'
                    text = 'А какой обед у тебя есть?'
                    markup = Keyboard.special_meal(False)
                    sp_messages = [self.send_message(user, text, reply_markup=markup).id]
                    result = True
            else:
                if not message.user_queries[0]:
                    sp_string = 'meal_get'
                    text = 'Хочешь занять место в очереди за обедами? А какой обед интересует?'
                    markup = Keyboard.special_meal()
                    sp_messages = [self.send_message(user, text, reply_markup=markup).id]
                    result = True
            if result:

                # noinspection PyUnboundLocalVariable
                message.db.update_specials(user, sp_messages, sp_string)
            else:
                message.db.update_specials(user, [])
        return result

    def send_default_message(self, message, mode='h'):
        user = message.from_user.id
        if mode != 'e' and message.user_data[1]:
            self.delete_message(user, message.user_data[1])
        prefix = f'Привет, э{Config.HELP_MESSAGE[1:]}' if mode == 's' else f'{Config.HELP_MESSAGE}'
        text = prefix + f'\n<i>Ты уже в очереди за обедами:</i> '
        if message.user_queries[0]:
            position = message.db.get_queue_position(user)
            text += f'<b>Да</b> (№{position})\nЗаявок на поиск реактивов: '
        else:
            text += f'<b>Нет</b>\n<i>Заявок на поиск реактивов:</i> '
        reagents_count = len(message.user_queries[1])
        text += f'<b>{reagents_count}</b>\nПожалуйста, выбери опцию ниже:'
        k = Keyboard().default(message.user_queries)
        if mode == 'e':
            self.edit_message_text(text, user, message.user_data[1], reply_markup=k, parse_mode='HTML')
        else:
            m = self.send_message(user, text, reply_markup=k, parse_mode='HTML')
            message.db.update_default_message_id(user, m.id)

    def delete_special_message(self, chat, sp_messages):
        if sp_messages:
            for message_id in sp_messages:
                try:
                    self.delete_message(chat, int(message_id))
                except Exception as exc:
                    log.log_error(exc, chat_id=chat)

    def edit_special_message(self, text, chat, sp_messages, reply_markup, parse_mode='HTML'):
        for message_id in sp_messages:
            self.edit_message_text(text, chat, int(message_id), reply_markup=reply_markup, parse_mode=parse_mode)

    def check_username(self, username, message):
        if username[0] == '@':
            username = username[1:]
            user_id = message.db.get_id(username)
            if user_id:
                return user_id[0]
            self.send_message(message.from_user.id, 'Unknown username')
            return -1
        return -2

    def reagent_send_query(self, chat, query, prefix='', mode='private'):
        name = query[4] if query[4] else ' -'
        amount = query[6] / 1000
        aditional = query[7] if query[7] else '-'
        if prefix:
            prefix = f'<i>{prefix}</i>\n'
        text = f'{prefix}<b>Речовинка:</b> {name}\n<b>Необходимо:</b> {amount}г\n<b>Дополнительно:</b> {aditional}'
        if mode == 'finish':
            markup = Keyboard.special_finish()
        elif mode == 'private':
            markup = Keyboard.special_reagent_check(query[0], True)
        elif mode == 'group':
            text = f'@{self.me.username}\n{text}'
            markup = Keyboard.special_reagent_check(query[0], False)
        else:
            markup = []
        if query[5]:
            sp_message = self.send_photo(chat, query[5], text, reply_markup=markup, parse_mode='HTML').id
        else:
            sp_message = self.send_message(chat, text, reply_markup=markup, parse_mode='HTML').id
        return sp_message

    def reagent_send_finish(self, sp_string, user, sp_messages):
        sp_list = sp_string.split('•')
        name = ' -' if sp_list[1][1:] == '_' else sp_list[1][1:]
        photo = '' if sp_list[2][1:] == '_' else sp_list[2][1:]
        try:
            amount = int(sp_list[3][1:]) / 1000
        except ValueError:
            amount = 0
        additional = ' -' if sp_list[4][1:] == '_' else sp_list[4][1:]
        text = (f'<i>Все правильно?</i>\n<b>Речовинка:</b> {name}\n'
                f'<b>Необходимо:</b> {amount}г\n<b>Дополнительно:</b> {additional}')
        markup = Keyboard.special_finish()
        if len(sp_list) > 4 and sp_list[4][1:] == '_' and not photo:
            self.edit_special_message(text, user, sp_messages, markup)
        else:
            self.delete_special_message(user, sp_messages)
            if photo:
                sp_messages = [
                    self.send_photo(user, photo, text, reply_markup=markup, parse_mode='HTML').id]
            else:
                sp_messages = [self.send_message(user, text, reply_markup=markup, parse_mode='HTML').id]
        return sp_messages

    @staticmethod
    def get_reagent_current_stage(sp_string):
        if sp_string:
            sp_list = sp_string.split('•')
            if sp_list[0] == 'reagent_find':
                last = sp_list[-1][0]
                if last == 'r':
                    return 'name'
                if last == 'n':
                    return 'photo'
                if last == 'p':
                    return 'amount'
                if last == 'a':
                    return 'info'
        return None

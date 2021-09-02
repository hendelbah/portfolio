from bot import Config, log
import sqlite3
import datetime


def adapt_list(list_instance):
    string = ' '
    for item in list_instance:
        if item:
            string += f'{item} '
    return string


def convert_int_list(string):
    int_list = []
    error = False
    for item in string.split():
        try:
            int_list.append(int(item))
        except ValueError:
            error = True
    if error:
        print('Lossy conversion str to int_list')
    return int_list


sqlite3.register_adapter(list, adapt_list)
sqlite3.register_converter('int_list', convert_int_list)


class SQL:
    def __init__(self):
        self.connection = None
        self.create_connection(Config.DATA_BASE_PATH)

    def __del__(self):
        self.connection.close()

    def create_connection(self, path):
        try:
            self.connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
            self.create_tables()
            if Config.DEBUG >= 5:
                print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            log.log_error(e, e_type='sqlite')

    def create_tables(self):
        create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY,
              username TEXT,
              first_name TEXT,
              language_code TEXT,
              edit_chat INTEGER,
              default_message_id INTEGER,
              special_messages_id int_list NOT NULL,
              special_string TEXT
            );
            """
        create_meals_table = """
            CREATE TABLE IF NOT EXISTS meals (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              date REAL NOT NULL,
              active INTEGER NOT NULL,
              type TEXT,
              helper_id INTEGER,
              FOREIGN KEY (user_id) REFERENCES users (id),
              FOREIGN KEY (helper_id) REFERENCES users (id)
            );
            """
        create_reagents_table = """
            CREATE TABLE IF NOT EXISTS reagents (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              date REAL NOT NULL,
              active INTEGER NOT NULL,
              name TEXT,
              photo TEXT,
              amount INTEGER,
              info TEXT,
              helper_id INTEGER,
              FOREIGN KEY (user_id) REFERENCES users (id),
              FOREIGN KEY (helper_id) REFERENCES users (id)
            );
            """
        create_forwarding_table = """
            CREATE TABLE IF NOT EXISTS forwarding (
              user_id INTEGER PRIMARY KEY,
              FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        create_chats_table = """
            CREATE TABLE IF NOT EXISTS chats (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              chat_id INTEGER
            );
            """
        self.execute_query(create_users_table)
        self.execute_query(create_meals_table)
        self.execute_query(create_reagents_table)
        self.execute_query(create_forwarding_table)
        self.execute_query(create_chats_table)

    def execute_query(self, *args, **kwargs):
        cursor = self.connection.cursor()
        try:
            cursor.execute(*args, **kwargs)
            self.connection.commit()
            if Config.DEBUG >= 5:
                print("Query executed successfully")
        except sqlite3.Error as e:
            log.log_error(e, e_type='sqlite')

    def executemany_query(self, *args, **kwargs):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(*args, **kwargs)
            self.connection.commit()
            if Config.DEBUG >= 5:
                print("Query executed successfully")
        except sqlite3.Error as e:
            log.log_error(e, e_type='sqlite')

    def execute_read_query(self, *args, **kwargs):
        cursor = self.connection.cursor()
        try:
            cursor.execute(*args, **kwargs)
            result = cursor.fetchall()
            if Config.DEBUG >= 5:
                print("Read query executed successfully")
        except sqlite3.Error as e:
            log.log_error(e, e_type='sqlite')
            raise e
        return result

    def chat(self, mode='g', chat_id=0):
        get_query = """
            SELECT chat_id
            FROM chats
            WHERE id = 1
            """
        update_query = """
            UPDATE chats
            SET chat_id = ?
            WHERE id = 1
            """
        if mode == 'g':
            content = self.execute_read_query(get_query)
            if content:
                return content[0][0]
            else:
                return 0
        if mode == 'u':
            self.execute_query(update_query, (chat_id,))
            return chat_id

    def get_id(self, username):
        query = """
            SELECT id
            FROM users
            WHERE username = ?;
            """
        content = self.execute_read_query(query, (username,))
        if content:
            return list(content[0])
        return content

    def get_user_data(self, user_id):
        query = """
            SELECT *
            FROM users
            WHERE id = ?;
            """
        content = self.execute_read_query(query, (user_id,))
        if content:
            return list(content[0])
        return content

    def get_user_names(self, user_id):
        query = """
            SELECT id, username, first_name
            FROM users
            WHERE id = ?
            """
        user = self.execute_read_query(query, (user_id,))
        return user[0] if user else ()

    def get_user_active_queries(self, user_id):
        meals_query = """
            SELECT id
            FROM meals
            WHERE user_id = ?
              AND active = 1
            """
        reagents_query = """
            SELECT id
            FROM reagents
            WHERE user_id = ?
              AND active = 1
            """
        meals = self.execute_read_query(meals_query, (user_id,))
        reagents = self.execute_read_query(reagents_query, (user_id,))
        meals = [meal_id[0] for meal_id in meals]
        reagents = [reagent_id[0] for reagent_id in reagents]
        return meals, reagents

    def get_reagents_active_queries(self):
        query = """
            SELECT *
            FROM reagents
            WHERE active = 1
            ORDER BY date ASC
        """
        return self.execute_read_query(query)

    def get_meals_queue(self):
        query = """
            SELECT *
            FROM meals
            WHERE active = 1
            ORDER BY date ASC
        """
        return self.execute_read_query(query)

    def get_reagents_query(self, query_id):
        query = """
            SELECT *
            FROM reagents
            WHERE id = ?
        """
        return self.execute_read_query(query, (query_id,))[0]

    def get_queue_position(self, user_id):
        queue = self.get_meals_queue()
        for index in range(len(queue)):
            if queue[index][1] == user_id:
                return index + 1
        return 0

    def get_reagents_user(self, query_id):
        query = """
            SELECT users.id, users.username, users.first_name
            FROM reagents
              INNER JOIN users ON users.id =reagents.user_id
            WHERE reagents.id = ?
              AND reagents.active = 1
            """
        user = self.execute_read_query(query, (query_id,))
        return user[0] if user else ()

    def update_query(self, query_id, table, helper_id=None, active=0):
        query = f"""
            UPDATE {table}
            SET
              active = ?,
              helper_id = ?
            WHERE id = ?
            """
        self.execute_query(query, (active, helper_id, query_id))

    def update_user_data(self, data):
        query = """
            UPDATE users
            SET
              username = ?,
              first_name = ?,
              language_code = ?
            WHERE id = ?;
            """
        self.execute_query(query, tuple(data[1:4] + [data[0]]))

    def update_bot_enabled(self, user_id, value):
        query = """
            UPDATE users
            SET
              bot_enabled = ?
            WHERE id = ?;
            """
        self.execute_query(query, (value, user_id))

    def update_default_message_id(self, user_id, message_id):
        query = """
            UPDATE users
            SET
              default_message_id = ?
            WHERE id = ?;
            """
        self.execute_query(query, (message_id, user_id))

    def update_specials(self, user_id, messages, string=''):
        query = """
            UPDATE users
            SET
              special_messages_id = ?,
              special_string = ?
            WHERE id = ?;
            """
        if not messages:
            string = ''
        self.execute_query(query, (messages, string, user_id))

    def add_user(self, data):
        query = """
            INSERT INTO users
            VALUES (?,?,?,?,?,?,?,?);
            """
        data1 = (1, None, '', '')
        self.execute_query(query, tuple(data) + data1)
        return data1

    def add_meals(self, user_id, meal_type):
        query = """
            INSERT INTO meals (user_id, date, active, type)
            VALUES (?,?,1,?);
            """
        date = datetime.datetime.now().timestamp()
        self.execute_query(query, (user_id, date, meal_type))

    def add_reagents(
            self,
            user_id,
            name=None,
            photo=None,
            amount=0,
            info=None):
        query = """
            INSERT INTO reagents (user_id, date, active, name, photo, amount, info)
            VALUES (?,?,1,?,?,?,?);
            """
        date = datetime.datetime.now().timestamp()
        self.execute_query(query, (user_id, date, name, photo, amount, info))

    def print_table(self, table):
        if table == 'users':
            query = 'SELECT * FROM users'
        elif table == 'meals':
            query = 'SELECT * FROM meals'
        elif table == 'reagents':
            query = 'SELECT * FROM reagents'
        elif table == 'forwarding':
            query = 'SELECT * FROM forwarding'
        else:
            print('There is no such table')
            return
        for row in self.execute_read_query(query):
            print(row)

    def handle_user(self, user):
        data = self.get_user_data(user.id)
        if Config.DEBUG >= 3:
            print(data)
        new_data = [user.id, user.username,
                    user.first_name, user.language_code]
        if data:
            if data[:4] != new_data:
                self.update_user_data(new_data)
            return tuple(data[4:])
        else:
            self.add_user(new_data)
            return 1, None, [], ''

    def get_forwarding(self):
        return (item[0] for item in self.execute_read_query(
            'SELECT user_id FROM forwarding'))

    def add_to_forwarding(self, user_id):
        self.execute_query('INSERT INTO forwarding VALUES (?)', (user_id,))
        return self.get_forwarding()

    def clear_forwarding(self):
        self.execute_query('DELETE FROM forwarding')
        return ()

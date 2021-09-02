token_file = 'files/token.txt'


class Config:
    HELP_MESSAGE = 'Этот бот поможет тебе с обменом обедов и поиском реактивов на Enamine ltd.'
    SWEAR_LIST = ['гей', 'педик', 'лох', 'хуй', 'хуя', 'хуе',
                  'хує', 'пидор', 'підор', 'говн', 'гавн', 'гівн',
                  'залуп', 'гамн' 'гомн', 'гімн', 'жопа', 'дерьм',
                  'шлюх', 'сука', 'уебок', 'ебат', 'ебаны', 'бляд',
                  'ебал', 'їбав', 'їбан', 'їбал', 'пизд', 'пізд']

    ADMINS = ['hendelbah']
    DEBUG = 6
    from pathlib import Path
    ROOT_PATH = Path(__file__).parent
    DATA_BASE_PATH = ROOT_PATH / 'files/data.db'
    LOG_PATH = ROOT_PATH / 'files/history.log'
    TOKEN = (ROOT_PATH / token_file).read_text('UTF-8')

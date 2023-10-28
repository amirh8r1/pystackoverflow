import emoji
from loguru import logger

from src.bot import bot
from src.constants import keyboards, keys, states
from src.db import db
from src.filters import IsAdmin


class Bot:
    """
    Telegram bot to randomly connect two strangers to talk!
    """
    def __init__(self, telebot, mongodb):
        self.bot = telebot
        self.db = mongodb

        # add custom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            /start command handler.
            """
            self.bot.send_message(
                message.chat.id,
                f"Hey <strong>{message.chat.first_name}</strong>",
                reply_markup=keyboards.main
            )

            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, '<strong> You are admin of this\
                              group! </strong>')

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            self.send_message(
                message.chat.id, message.text,
                reply_markup=keyboards.main
            )

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        Send message to telegram bot.
        """
        if emojize:
            text = emoji.emojize(text, use_aliases=True)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {'chat.id': chat_id},
            {'$set': {'state': state}}
        )


if __name__ == '__main__':
    logger.info('Bot Started')
    nashenas_bot = Bot(telebot=bot, mongodb=db)
    nashenas_bot.run()

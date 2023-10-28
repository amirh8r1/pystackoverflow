import emoji
from loguru import logger

from src.bot import bot
from src.constants import keyboards
from src.filters import IsAdmin


class Bot:
    """
    Telegram bot to randomly connect two strangers to talk!
    """
    def __init__(self, telebot):
        self.bot = telebot

        # add mustom filters
        self.bot.add_custom_filter(IsAdmin())

        # register handlers
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, '<strong> You are admin of this group! </strong>')

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


if __name__ == '__main__':
    logger.info('Bot Started')
    nashenas_bot = Bot(telebot=bot)
    nashenas_bot.run()

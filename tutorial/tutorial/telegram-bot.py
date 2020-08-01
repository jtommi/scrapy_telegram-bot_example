from scrapy import signals
from telegram.ext import Updater, CommandHandler

import telegram_credentials


class TelegramBot(object):
    telegram_token = telegram_credentials.token

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler

        cs = crawler.signals
        cs.connect(self._spider_closed, signal=signals.spider_closed)

        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.updater = Updater(self.telegram_token, use_context=True)

        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("stats", self.stats))

        # Start the Bot
        self.updater.start_polling()

    def _spider_closed(self, spider, reason):
        # Stop the Bot
        self.updater.stop()

    def stats(self, update, context):
        # Send a message with the stats
        msg = (
            "Spider "
            + self.crawler.spider.name
            + " stats: "
            + str(self.crawler.stats.get_stats())
        )

        update.message.reply_text(msg)

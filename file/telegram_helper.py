# pip install python-telegram-bot
import telegram

class TelegramHelper():
    def __init__(self, bot_profile):
        self.bot_profile = TelegramBotProfile(bot_profile)
        if self.bot_profile.is_valid:
            self.bot = telegram.Bot(token = self.bot_profile.bot_token)

    def status_check(self):
        pass

    async def send_message(self, target_id = None, message = "HELLO WORLD", message_thread_id=None):
        if target_id is None:
            target_id = self.bot_profile.chat_id
        try:
            result = await self.bot.send_message(target_id, message,
                parse_mode=telegram.constants.ParseMode.HTML, disable_web_page_preview=True, message_thread_id=message_thread_id)
            return result
        except:
            return None

    async def send_file(self, target_id = None, file = None, message_thread_id=None):
        if target_id is None:
            target_id = self.bot_profile.chat_id
        if file is None:
            return
        try:
            result = await self.bot.send_document(target_id, file, message_thread_id=message_thread_id, write_timeout=60)
            return result
        except:
            return None

class TelegramBotProfile():
    TG_BOT_UPDATE_URL = "https://api.telegram.org/bot{}/getUpdates"
    TG_BOT_PROFILE_EXAMPLE = {
        "bot_token": "PLACE_YOUR_TOKEN_HERE",
        "chat_id": "SOME_NUMBER",
        "healthcheck_thread_id": "SOME_NUMBER",
        "alert_thread_id": "SOME_NUMBER",
        "daily_report_id": "SOME_NUMBER",
        "daily_screener_id": "SOME_NUMBER",
        "hk_daily_id": "SOME_NUMBER",
        "us_daily_id": "SOME_NUMBER",
    }

    def __init__(self, bot_profile):
        self.is_valid = False
        try:
            self.bot_token = bot_profile["bot_token"]
            self.chat_id = bot_profile["chat_id"]
            self.healthcheck_thread_id = bot_profile["healthcheck_thread_id"]
            self.alert_thread_id = bot_profile["alert_thread_id"]
            self.daily_report_id = bot_profile["daily_report_id"]
            self.daily_screener_id = bot_profile["daily_screener_id"]
            self.hk_daily_id = bot_profile["hk_daily_id"]
            self.us_daily_id = bot_profile["us_daily_id"]
            self.is_valud = True
        except:
            print("Error reading profile.")
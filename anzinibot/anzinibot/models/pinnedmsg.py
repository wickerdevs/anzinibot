from anzinibot import applogger
from telegram.parsemode import ParseMode
from anzinibot.modules import config
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from anzinibot.models.mq_bot import MQBot
    from telegram.message import Message
from anzinibot.models.callbacks import Callbacks
from anzinibot.models.markup import CreateMarkup


class PinnedMessage():
    def __init__(self, bot:'MQBot', thread_name:str, user_id:int, account:str, message_id:int, text:str) -> None:
        self.bot = bot
        self.message_id = message_id
        self.user_id = user_id
        self.account = account
        self.text = text
        self.thread_name = thread_name

    
    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            if key == 'bot':
                continue

            value = self.__dict__[key]
            data[key] = value
        return data


    @classmethod
    def de_dict(cls, bot:'MQBot', data:dict) -> Optional['PinnedMessage']:
        return cls(bot=bot, **data)


    @staticmethod
    def send(text, *args, **kwargs) -> Optional['PinnedMessage']:
        pinned = PinnedMessage(text=text, *args, **kwargs)
        pinned.update(text)
        return pinned


    def update(self, text:str):
        text = f'<b>PINNED MESSAGE</b>\n<b>Account:</b> {self.account}\n<b>Task:</b> {self.thread_name}\n' + text
        try:
            message = self.bot.edit_message_text(text=text, chat_id=self.user_id, message_id=self.message_id, parse_mode=ParseMode.HTML)
        except:
            message = self.bot.send_message(chat_id=self.user_id, text=text, parse_mode=ParseMode.HTML)
        self.message_id = message.message_id
        self.save()
        return message

    
    def final_update(self, text:str):
        message = self.update(text)
        markup = CreateMarkup({f'{Callbacks.DELETE_PINNED_MESSAGE}:{self.user_id}:{self.account}:{self.thread_name}': 'Hide'}).create_markup()
        message.edit_reply_markup(reply_markup=markup)
        applogger.debug('Sent final Pinned Message with markup')
        return message


    def delete(self):
        try:
            self.bot.delete_message(chat_id=self.user_id, message_id=self.message_id)
        except:
            pass

        data = config.get('PINNED')
        if not data:
            return True

        if f'{self.user_id}:{self.account}:{self.thread_name}' in data.keys():
            del data[f'{self.user_id}:{self.account}:{self.thread_name}']
            config.set('PINNED', data)
        return True


    def save(self):
        pinned = config.get('PINNED')
        if not pinned:
            pinned = dict()
        
        pinned[f'{self.user_id}:{self.account}:{self.thread_name}'] = self.to_dict()
        config.set('PINNED', pinned)


    @classmethod
    def deserialize(cls, bot:'MQBot', user_id:int, account:str, thread_name:str):
        data = config.get('PINNED')
        if not data:
            return None

        selected = data.get(f'{user_id}:{account}:{thread_name}')
        if not selected:
            applogger.debug(f'No pinned found with {user_id} and {thread_name}')
            return None

        return cls.de_dict(bot, selected)
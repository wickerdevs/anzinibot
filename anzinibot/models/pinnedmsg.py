import threading
from cryptography.hazmat.primitives.asymmetric import ec

from telegram.error import BadRequest
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
    def __init__(self, bot:'MQBot', process:str, user_id:int, account:str, message_id:int, text:str, message:Optional['Message']=None) -> None:
        self.bot = bot
        self.message_id = message_id
        self.user_id = user_id
        self.account = account
        self.text = text
        self.process = process
        self.message = message

    
    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            if key in ('bot', 'message'):
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
        try:
            thread = threading.current_thread().getName().split(':')[2]
        except:
            thread = self.account

        text = f'<b>PINNED MESSAGE</b>\n<b>Task:</b> {self.process}\n<b>Thread:</b> {thread}\n' + text
        if self.text == text:
            return self
        try:
            message = self.bot.edit_message_text(text=text, chat_id=self.user_id, message_id=self.message_id, parse_mode=ParseMode.HTML)
        except Exception as error:
            applogger.warning(f'Error editing pinned message: ', exc_info=error)
            message = self.bot.send_message(chat_id=self.user_id, text=text, parse_mode=ParseMode.HTML)
        
        self.message = message
        self.message_id = message.message_id
        self.text = text
        self.save()
        return self

    
    def final_update(self, text:str):
        pinned = self.update(text)
        markup = CreateMarkup({f'{Callbacks.DELETE_PINNED_MESSAGE}:{self.user_id}:{self.account}:{self.process}': 'Hide'}).create_markup()
        pinned.message.edit_reply_markup(reply_markup=markup)
        applogger.debug('Sent final Pinned Message with markup')
        return pinned


    def delete(self):
        try:
            self.bot.delete_message(chat_id=self.user_id, message_id=self.message_id)
        except:
            pass

        data = config.get('PINNED')
        if not data:
            return True

        if f'{self.user_id}:{self.account}:{self.process}' in data.keys():
            del data[f'{self.user_id}:{self.account}:{self.process}']
            config.set('PINNED', data)
        return True


    def save(self):
        pinned = config.get('PINNED')
        if not pinned:
            pinned = dict()
        
        pinned[f'{self.user_id}:{self.account}:{self.process}'] = self.to_dict()
        config.set('PINNED', pinned)


    @classmethod
    def deserialize(cls, bot:'MQBot', user_id:int, account:str, process:str):
        data = config.get('PINNED')
        if not data:
            applogger.debug(f'No pinned found with {user_id} and {process}')
            return None

        selected = data.get(f'{user_id}:{account}:{process}')
        if not selected:
            applogger.debug(f'No pinned found with {user_id} and {process}')
            return None

        return cls.de_dict(bot, selected)
from anzinibot.modules import config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from anzinibot.models.mq_bot import MQBot
from anzinibot.models.callbacks import Callbacks
from anzinibot.models.markup import CreateMarkup


class PinnedMessage():
    def __init__(self, message_id, user_id, text, thread_name) -> None:
        self.message_id = message_id
        self.user_id = user_id
        self.text = text
        self.thread_name = thread_name

    
    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            value = self.__dict__[key]
            data[key] = value
        return data


    @classmethod
    def de_dict(cls, data:dict):
        return cls(**data)


    def final_update(self, bot:'MQBot', text:str):
        message = self.update(bot, text)
        markup = CreateMarkup({Callbacks.DELETE_PINNED_MESSAGE: 'Hide'}).create_markup()
        message.edit_reply_markup(chat_id=self.user_id, message_id=self.message_id, reply_markup=markup)


    def update(self, bot:'MQBot', text:str):
        text = '<b>PINNED MESSAGE</b>\n' + text
        try:
            message = bot.edit_message_text()
        except:
            message = bot.send_message()
        self.message_id = message.message_id
        return message


    def delete(self, bot:'MQBot'):
        try:
            bot.delete_message(chat_id=self.user_id, message_id=self.message_id)
        except:
            pass

        data = config.get('PINNED')
        if not data:
            return True

        if f'{self.user_id}:{self.thread_name}' in data.keys():
            del data[f'{self.user_id}:{self.thread_name}']
            config.set('PINNED', data)
        return True


    def save(self):
        pinned = config.get('PINNED')
        if not pinned:
            pinned = dict()
        
        pinned[f'{self.user_id}:{self.thread_name}'] = self.to_dict()
        config.set('PINNED', pinned)


    @classmethod
    def deserialize(cls, user_id:str, thread_name:str):
        data = config.get('PINNED')
        if not data:
            return None

        selected = data.get(f'{user_id}:{thread_name}')
        if not selected:
            return None

        return cls.de_dict(selected)
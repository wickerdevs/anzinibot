import re
import time
from anzinibot.modules import config
from anzinibot.bot import *
from anzinibot.texts import *
from anzinibot.models.callbacks import *
from anzinibot.models.pinnedmsg import PinnedMessage
from anzinibot.models.persistence import Persistence
from anzinibot.models.instasession import InstaSession
from anzinibot.models.interactsession import InteractSession
from anzinibot.models.settings import Settings
from anzinibot.models.setting import Setting
from anzinibot.models.callbacks import *
from anzinibot.models.markup import CreateMarkup, MarkupDivider
from anzinibot.modules import instagram
from telegram import InputMediaPhoto, InputFile, Update
from telegram.ext import CallbackContext

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def send_photo(name, context, update):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('{}.png'.format(name), 'rb'))


def send_message(update:Update, context:CallbackContext, message:str, markup=None):
    if update.callback_query:
        try:
            update.callback_query.answer()
            if markup:
                message = update.callback_query.edit_message_text(text=message, reply_markup=markup)
            else:
                message = update.callback_query.edit_message_text(text=message)
            config.set_message(update.effective_user.id, message.message_id)
            return message
        except:
            pass

    elif config.get_message(update.effective_chat.id):
        message_id = config.get_message(update.effective_chat.id)
        try:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
            telelogger.debug(f'Deleted bot message. id: {message_id}')
        except: pass

    try: 
        message_id = update.message.message_id
        update.message.delete()
        telelogger.debug(f'Deleted user message. id: {message_id}')
    except: pass

    if markup:
        message = context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML, reply_markup=markup)
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

    config.set_message(update.effective_user.id, message.message_id)
    return message


def check_invalid_text(update, context, text):
    occurences = re.findall(r'(//u[0-9A-Fa-f]+)', text)
    if occurences:
        message = context.bot.send_message(chat_id=update.effective_chat.id, text=invalid_text_text, parse_mode=ParseMode.HTML)
        if update.message:
            update.message.delete()
        time.sleep(1.6)
        message.delete()


def check_auth(update, context):
    users_str = config.get('USERS')
    if isinstance(users_str, str):
        users_str = users_str.replace('[', '')
        users_str = users_str.replace(']', '')
        users_str = users_str.replace(' ', '')
        users = users_str.split(',')
        for index, user in enumerate(users):
            users[index] = int(user)
    else:
        users = users_str
    if update.effective_user.id in users:
        telelogger.debug('User is authorized to use the bot')
        return True
    else:
        telelogger.debug('User is NOT authorized to use the bot.')
        try:
            send_message(update, context, not_authorized_text)
            return False
        except Exception as error:
            telelogger.debug('Error in sending message: {}'.format(error))
            return False

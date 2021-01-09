from anzinibot import texts
from anzinibot.bot.commands import *
import time

@send_typing_action
def incorrect_command(update:Update, context):
    tried = update.message.text
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=incorrect_command_text.format(tried), parse_mode=ParseMode.HTML)
    if update.message:
        update.message.delete()
    time.sleep(2)
    message.delete()
    return
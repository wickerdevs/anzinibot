from anzinibot.bot.commands import *


def help_def(update:Update, context):
    if update.callback_query:
        update.effective_message.delete()
    message = send_message(update, context, help_text)
from anzinibot.bot.commands import *


def cancel_def(update, context:CallbackContext):
    if not check_auth(update, context):
        return 
    return ConversationHandler.END

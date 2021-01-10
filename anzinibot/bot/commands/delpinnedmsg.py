from anzinibot.bot.commands import *


def delpinnedmsg_def(update:Update, context:CallbackContext):
    data = update.callback_query.data
    data = data.split(':')
    update.callback_query.answer()
    try:
        pinned:PinnedMessage = PinnedMessage.deserialize(
            bot=context.bot,
            user_id=int(data[1]),
            account=data[2],
            process=data[3]
        )
        pinned.delete()
    except Exception as error:
        telelogger.warning(f'Impossible to delete Pinned Message with data: {data}', exc_info=error)

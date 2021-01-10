from anzinibot.bot.commands import *


def clear_scraped_def(update, context):
    if not check_auth(update, context):
        return

    markup = CreateMarkup({f'{Callbacks.DELETE_SCRAPED_DATA}:{Callbacks.CONFIRM}': 'Yes', 
    f'{Callbacks.DELETE_SCRAPED_DATA}:{Callbacks.CANCEL}': 'No'}, cols=2).create_markup()
    send_message(update, context, confirm_clear_data_text, markup)


def confirm_clear_data(update:Update, context):
    data = update.callback_query.data
    data = data.split(':')

    markup = CreateMarkup({Callbacks.ACCOUNT: 'Account Info'}).create_markup()
    if data[1] == Callbacks.CONFIRM:
        scraped = dict()
        config.set('SCRAPED', scraped)
        send_message(update, context, scraped_data_cleared_text, markup)
    else:
        send_message(update, context, cancelled_clear_data_text, markup)
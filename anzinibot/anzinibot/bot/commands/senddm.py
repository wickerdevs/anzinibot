from anzinibot.models.interaction import Interaction
from anzinibot.bot.commands import *



def senddm_def(update, context):
    if not check_auth(update, context):
        return ConversationHandler.END

    # Check LoginStatus
    session:InteractSession = InteractSession(update.effective_user.id)
    
    if not session.get_creds():
        # Not Logged In
        message = send_message(update, context, not_logged_in_text)
        session.discard()
        return ConversationHandler.END

    # Get scrape selection
    scraped = config.get('SCRAPED')

    # Create markup
    markupk = dict()
    if scraped:
        # No Scraped Selection
        for item in scraped.keys():
            markupk[item] = f'{item}\'s followers ({len(scraped[item])})'

    markupk[InteractStates.SCRAPEACCOUNT] = 'Scrape another user'
    markupk[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markupk).create_markup()

    # Send message and update ConversationHandler
    message = send_message(update, context, select_scrape_text, markup)
    return InteractStates.SCRAPE


def select_scrape(update, context):
    if not check_auth(update, context):
        return

    session = InteractSession(update.effective_user.id)
    data = update.callback_query.data
    update.callback_query.answer()
    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()

    if data == str(InteractStates.SCRAPEACCOUNT):
        send_message(update, context, select_account_text, markup)
        return InteractStates.SCRAPEACCOUNT

    elif data == Callbacks.CANCEL:
        return cancel_send_dm(update, context)

    session.set_target(data)
    session.set_interaction(Interaction(data))
    session.set_scraped(config.get_scraped(data))

    counts = [5, 25, 50, 100, 250, 400, 500]
    markupk = dict()
    for count in counts:
        if len(session.get_scraped()) >= count:
            markupk[count] = str(count)
    markupk[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markupk).create_markup()
    send_message(update, context, select_count_text, markup)
    return InteractStates.COUNT


def select_scrape_account(update, context):
    session = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return

    username = update.message.text
    update.message.delete()

    send_message(update, context, checking_user_vadility_text)
    client = instagram.init_client()
    try:
        result = client.is_valid_user(username)
        client.disconnect()
    except:
        client.disconnect()
        markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'})
        send_message(update, context, incorrect_user_text.format(str(username)))
        return InteractStates.SCRAPEACCOUNT

    session.set_target(username)
    session.set_interaction(Interaction(username))
    markup = CreateMarkup({
        5: '5',
        25: '25',
        50: '50',
        100: '100',
        250: '250',
        400: '400',
        500: '500',
        Callbacks.CANCEL: 'Cancel'
    }).create_markup()
    send_message(update, context, select_count_text, markup)
    return InteractStates.COUNT


def select_count(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return
    

    data = update.callback_query.data
    update.callback_query.answer()
    if data == Callbacks.CANCEL:
        return cancel_send_dm(update, context, session)

    session.set_count(int(data))
    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, input_message_text, markup)
    return InteractStates.MESSAGE


def input_message(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return

    text = update.message.text
    text = text.replace('\\u', '')
    session.set_text(text)
    update.message.delete()

    markup = CreateMarkup({f'{Callbacks.SKIP}:{InteractStates.INPUTPROXIES}': 'Skip', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, input_accounts_text, markup)
    return InteractStates.INPUTACCOUNTS


def skip(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return

    data = update.callback_query.data
    print(f'Skipping: {data}')
    if str(InteractStates.INPUTPROXIES) in data:
        markup = CreateMarkup({Callbacks.SKIP: 'Skip', Callbacks.CANCEL: 'Cancel'}).create_markup()
        send_message(update, context, input_proxies_text, markup)
        return InteractStates.INPUTPROXIES
    else:
        markup = CreateMarkup({Callbacks.CONFIRM: 'Confirm', Callbacks.CANCEL: 'Cancel'}).create_markup()
        send_message(update, context, confirm_dms_text.format(session.count), markup)
        return InteractStates.CONFIRM
    

def input_accounts(update:Update, context:CallbackContext):
    session:InteractSession = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return
    
    # writing to a custom file
    with open("config/accounts.txt", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

    with open('config/accounts.txt', 'r') as file:
        data = file.read().replace('\n', '')
        accounts = dict()
        for cred in data:
            cred = cred.split(':')
            accounts[cred[0]] = cred[1]

        session.set_accounts(accounts)
    
    markup = CreateMarkup({f'{Callbacks.SKIP}:{InteractStates.CONFIRM}': 'Skip', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, input_proxies_text, markup)
    return InteractStates.INPUTPROXIES


def input_proxies(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return
    
    # writing to a custom file
    with open("config/proxies.txt", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

    with open('config/proxies.txt', 'r') as file:
        proxies = file.read().replace('\n', '')
        session.set_accounts(proxies)
    
    markup = CreateMarkup({Callbacks.CONFIRM: 'Confirm', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, confirm_dms_text.format(session.count), markup)
    return InteractStates.CONFIRM


def confirm_dms(update, context):
    session = InteractSession.deserialize(InteractSession.INTERACT, update)
    if not session: 
        return

    data = update.callback_query.data
    update.callback_query.answer()
    if data == Callbacks.CONFIRM:
        instagram.enqueue_dm(session)
        session.discard()
        return ConversationHandler.END
    else:
        return cancel_send_dm(update, context, session)


def cancel_send_dm(update, context, session:InteractSession=None):
    if not session:
        session = InteractSession.deserialize(Persistence.INTERACT, update)
        if not session:
            return

    send_message(update, context, follow_cancelled_text)
    session.discard()
    return ConversationHandler.END
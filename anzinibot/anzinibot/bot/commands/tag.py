from instaclient.errors.common import PrivateAccountError, NotLoggedInError, InvalidUserError
from instaclient.instagram.profile import Profile
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException    
from anzinibot.models.interaction import Interaction
from anzinibot.bot.commands import *



def tag_def(update, context):
    if not check_auth(update, context):
        return ConversationHandler.END

    if instagram.check_tag_queue():
        send_message(update, context, tag_queue_full_text)
        return ConversationHandler.END

    # Check LoginStatus
    session:InteractSession = InteractSession(update.effective_user.id, InteractSession.TAG)
    
    if not session.get_creds():
        # Not Logged In
        message = send_message(update, context, not_logged_in_text)
        session.discard()
        return ConversationHandler.END

    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
    message = send_message(update, context, input_post_url_text, markup)
    session.set_message(message.message_id)
    return TagStates.POST_URL


def input_post_url(update, context):
    print('Input Post')
    session:InteractSession = InteractSession.deserialize(InteractSession.TAG, update)
    if not session:
        return

    # https://www.instagram.com/p/CIqua7YHtha/
    
    url:str = update.message.text
    telelogger.warn(f'Url: {url}')

    send_message(update, context, checking_post_text)
    client = instagram.init_client()
    try:
        shortcode = url.replace('https://www.instagram.com/p/', '')
        telelogger.warn(f'Url: {shortcode}')
        shortcode = shortcode.replace('/', '')
        telelogger.warn(f'Url: {shortcode}')
        post = client.get_post(shortcode, context=False)
        session.set_post(shortcode)
    except Exception as error:
        client.disconnect()
        telelogger.warning(f'The url <{url}> is invalid.', exc_info=error)
        markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
        send_message(update, context, invalid_post_url_text, markup)
        return TagStates.POST_URL

    client.disconnect()

    # Get scrape selection
    scraped = config.get('SCRAPED')

    # Create markup
    markupk = dict()
    if scraped:
        # No Scraped Selection
        for item in scraped.keys():
            markupk[item] = f'{item}\'s followers ({len(scraped[item])})'

    markupk[TagStates.SCRAPEACCOUNT] = 'Scrape another user'
    markupk[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markupk, cols=2).create_markup()

    # Send message and update ConversationHandler
    message = send_message(update, context, select_tag_scrape_text, markup)
    return TagStates.SCRAPE



def select_tag_scrape(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.TAG, update)
    if not session:
        return
        
    data = update.callback_query.data
    update.callback_query.answer()
    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()

    if data == str(TagStates.SCRAPEACCOUNT):
        send_message(update, context, select_account_text, markup)
        return TagStates.SCRAPEACCOUNT

    elif data == Callbacks.CANCEL:
        return cancel_tag(update, context)

    session.set_target(data)
    session.set_interaction(Interaction(data))
    scraped = config.get_scraped(data)
    session.set_scraped(scraped)

    counts = [5, 25, 50, 100, 250, 400, 500, len(scraped)]
    markupk = dict()
    for count in counts:
        if len(scraped) >= count:
            markupk[count] = str(count)
    markupk[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markupk, cols=2).create_markup()
    send_message(update, context, select_count_text, markup)
    return TagStates.COUNT


def select_tag_scrape_account(update, context):
    session = InteractSession.deserialize(InteractSession.TAG, update)
    if not session: 
        return

    username = update.message.text
    update.message.delete()

    send_message(update, context, checking_user_vadility_text)
    client = instagram.init_client()
    profile = None
    count=750
    try:
        send_message(update, context, "Getting profile info...")
        try:
            profile = client.get_profile(username)
        except NotLoggedInError:
            send_message(update, context, logging_in_text)
            client.login(session.username, session.password)
            profile = client.get_profile(username)

        if not profile:
            raise InvalidUserError(username)
        if profile.is_private and not profile.mutual_followed:
            raise PrivateAccountError(profile.username)

        count = profile.follower_count
    except (NotLoggedInError, TimeoutException, NoSuchElementException):
        telelogger.debug("Error checking instagram")
        pass
    except (InvalidUserError, PrivateAccountError):
        client.disconnect()
        markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
        send_message(update, context, incorrect_user_text.format(str(username)))
        return TagStates.SCRAPEACCOUNT
    except:
        telelogger.debug(f"An error as occured. Ignoring. Username: {username}")
        pass
    client.disconnect()
    counts = [5, 25, 50, 100, 250, 400, 500, count]
    markupk = dict()
    for item in counts:
        if count >= item:
            markupk[item] = str(item)
    markupk[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markupk, cols=2).create_markup()
        
    session.set_target(username)
    session.set_interaction(Interaction(username))
    send_message(update, context, select_tag_count_text, markup)
    return TagStates.COUNT


def select_tag_count(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.TAG, update)
    if not session: 
        return
    
    data = update.callback_query.data
    update.callback_query.answer()
    if data == Callbacks.CANCEL:
        return cancel_tag(update, context, session)

    session.set_count(int(data))
    scraped = list()
    for index, user in enumerate(session.get_scraped()):
        if index+1 > session.count:
            break
        scraped.append(user)
    session.set_scraped(scraped)

    markup = CreateMarkup({f'{Callbacks.TAGSKIP}:{InteractStates.CONFIRM}': 'Skip', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, input_accounts_text, markup)
    return TagStates.INPUTACCOUNTS


def tag_skip(update, context):
    session:InteractSession = InteractSession.deserialize(InteractSession.TAG, update)
    if not session: 
        return

    data = update.callback_query.data
    print(f'Skipping: {data}')

    markup = CreateMarkup({Callbacks.CONFIRM: 'Confirm', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, confirm_tags_text.format(session.count), markup)
    return TagStates.CONFIRM
    

def input_tag_accounts(update:Update, context:CallbackContext):
    session:InteractSession = InteractSession.deserialize(InteractSession.TAG, update)
    if not session: 
        return
    
    # writing to a custom file
    with open("config/accounts.txt", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

    with open('config/accounts.txt', 'r') as file:
        data = file.read().splitlines()
        accounts = dict()
        for cred in data:
            cred = cred.split(':')
            accounts[cred[0]] = cred[1]

        session.set_accounts(accounts)
    
    markup = CreateMarkup({Callbacks.CONFIRM: 'Confirm', Callbacks.CANCEL: 'Cancel'}).create_markup()
    send_message(update, context, confirm_tags_text.format(session.count), markup)
    return TagStates.CONFIRM


def confirm_tags(update, context):
    session = InteractSession.deserialize(InteractSession.TAG, update)
    if not session: 
        return

    data = update.callback_query.data
    update.callback_query.answer()
    if data == Callbacks.CONFIRM:
        markup = CreateMarkup({Callbacks.HELP: 'Command List'}).create_markup()
        send_message(update, context, enqueued_tags_text, markup)
        instagram.enqueue_tag_process(session)
        session.discard()
        return ConversationHandler.END
    else:
        return cancel_tag(update, context, session)


def cancel_tag(update, context, session:InteractSession=None):
    if not session:
        session = InteractSession.deserialize(Persistence.TAG, update)
        if not session:
            return

    send_message(update, context, follow_cancelled_text)
    session.discard()
    return ConversationHandler.END

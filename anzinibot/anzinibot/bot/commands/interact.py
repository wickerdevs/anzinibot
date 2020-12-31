from instaclient.client.instaclient import InstaClient
from instaclient.errors.common import InvalidUserError, NotLoggedInError, PrivateAccountError
from anzinibot.bot.commands import *

@send_typing_action
def follow_def(update, context):
    if not check_auth(update, context):
        return ConversationHandler.END

    session:InteractSession = InteractSession(update.effective_user.id)
    
    if session.get_creds():
        markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
        message = send_message(update, context, select_account_text, markup)
        session.set_message(message.message_id)
        return InteractStates.ACCOUNT

    else:
        # Not Logged In
        message = send_message(update, context, not_logged_in_text)
        session.discard()
        return ConversationHandler.END


@send_typing_action
def input_follow_account(update, context):
    if not check_auth(update, context):
        return

    session:InteractSession = InteractSession.deserialize(Persistence.FOLLOW, update)
    session.set_target(update.message.text.replace('@', ''))
    update.message.delete()
    send_message(update, context, checking_user_vadility_text)
    # Check Account
    instaclient = instagram.init_client()
    try:
        instaclient.is_valid_user(session.target)
    except (InvalidUserError, PrivateAccountError):
        markup = CreateMarkup({'Cancel': Callbacks.CANCEL}).create_markup()
        send_message(update, context, error_when_checking_account.format(session.target), markup)
        instaclient.disconnect()
        return InteractStates.ACCOUNT
    except NotLoggedInError:
        pass

    # Select Count
    instaclient.disconnect()
    markup = CreateMarkup({
        Callbacks.TEN: '10',
        Callbacks.TFIVE: '25',
        Callbacks.FIFTY: '50',
        Callbacks.SFIVE: '75',
        Callbacks.CANCEL: 'Cancel'
    }, cols=2).create_markup()
    send_message(update, context, select_count_text, markup)
    return InteractStates.COUNT


@send_typing_action
def input_follow_count(update, context):
    if not check_auth(update, context):
        return

    session:InteractSession = InteractSession.deserialize(Persistence.FOLLOW, update)
    if update.callback_query.data == Callbacks.CANCEL:
        return cancel_follow(update, context, session)

    session.set_count(int(update.callback_query.data))
    
    # Confirm
    markup = CreateMarkup({
        Callbacks.CONFIRM: 'Confirm',
        Callbacks.CANCEL: 'Cancel' 
    }).create_markup()
    send_message(update, context, confirm_follow_text.format(session.count, session.target), markup)
    return InteractStates.CONFIRM


@send_typing_action
def confirm_follow(update, context):
    if not check_auth(update, context):
        return

    session:InteractSession = InteractSession.deserialize(Persistence.FOLLOW, update)
    send_message(update, context, launching_operation_text)
    print(session)
    instagram.interaction_job(session)
    session.discard()
    return ConversationHandler.END
    

@send_typing_action
def cancel_follow(update, context, session:InteractSession=None):
    if not session:
        session = InteractSession.deserialize(Persistence.FOLLOW, update)
        if not session:
            return


    send_message(update, context, follow_cancelled_text)
    session.discard()
    return ConversationHandler.END

                                                                                                                                                                                                                               



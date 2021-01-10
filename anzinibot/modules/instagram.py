from instaclient.client.constants import ClientUrls
from anzinibot.models.worker import TaskQueue
from anzinibot.models.pinnedmsg import PinnedMessage
from functools import wraps
from random import randint, randrange
from telegram.parsemode import ParseMode
from anzinibot.models.interaction import Interaction
from anzinibot.models.settings import Settings
from anzinibot.models.setting import Setting
from anzinibot.models.interactsession import InteractSession
from anzinibot.modules import config
from anzinibot.texts import *
from typing import List, Optional, Tuple
from anzinibot import CHROMEDRIVER_DIR, CONFIG_DIR, CONFIG_FOLDER
from instaclient.client.instaclient import InstaClient
from instaclient.errors.common import FollowRequestSentError, InvaildPasswordError, InvalidUserError, PrivateAccountError, SuspisciousLoginAttemptError, VerificationCodeNecessary
from instaclient.instagram.post import Post
from anzinibot.models.instasession import InstaSession
from anzinibot import applogger, tagqueue, dmqueue, LOCALHEADLESS
import os, multiprocessing, logging, time, threading

instalogger = logging.getLogger('instaclient')
lock = threading.Lock()


def insta_error_callback(driver):
    driver.save_screenshot('error.png')
    from anzinibot import telegram_bot as bot, config # TODO
    users_str = config.get('DEVS')
    if isinstance(users_str, str):
        users_str = users_str.replace('[', '')
        users_str = users_str.replace(']', '')
        users_str = users_str.replace(' ', '')
        users = users_str.split(',')
        for index, user in enumerate(users):
            users[index] = int(user)
    else:
        users = users_str

    for dev in users:
        bot.send_photo(chat_id=dev, photo=open('{}.png'.format('error'), 'rb'), caption='There was an error with the bot. Check logs')

    
def update_message(obj: InteractSession, text:str, final:bool=False):
    """
    process_update_callback sends an update message to the user, to inform of the status of the current process. This method can be used as a callback in another method.

    Args:
        obj (InteractionSession): Object to get the `chat_id` and `message_id` from.
        text (str): The text to send via message
    """
    global lock
    with lock:
        from anzinibot import telegram_bot as bot
        process = threading.current_thread().getName().split(':')[0]
        pinned:PinnedMessage = PinnedMessage.deserialize(bot, obj.user_id, obj.username, process)
        if pinned:
            if not final:
                pinned.update(text)
            else:
                pinned.final_update(text)
            obj.set_message(pinned.message_id)
            return pinned
        else:
            """ message_id = config.get_message(obj.get_user_id())
            try:
                bot.delete_message(chat_id=obj.user_id, message_id=message_id)
            except Exception as error:
                applogger.error(f'Unable to delete message of id {message_id}')
                pass          """

            if not final:
                pinned = PinnedMessage.send(
                    bot=bot,
                    process=process,
                    user_id=obj.user_id,
                    account=obj.username,
                    message_id=obj.message_id,
                    text=text
                )
            else:
                pinned = PinnedMessage(bot, process, obj.user_id, obj.username, obj.message_id, text)
                pinned.final_update(text)
            obj.set_message(pinned.message_id)
            applogger.debug(f'Sent pinned message of id {pinned.message_id}')
        return pinned


def init_client():
    if os.environ.get('PORT') in (None, ""):
        client = InstaClient(driver_path=f'{CHROMEDRIVER_DIR}', debug=True, logger=instalogger, localhost_headless=LOCALHEADLESS)
    else:
        client = InstaClient(host_type=InstaClient.WEB_SERVER, debug=True, logger=instalogger, localhost_headless=LOCALHEADLESS)
    return client


def error_proof(func):
    @wraps(func)
    def wrapper(session:InteractSession):
        result:Tuple[bool, InteractSession] = func(session)
        if result[1]:
            settings:Settings = config.get_settings(session.user_id)
            settings.add_interaction(result[1].interaction)
        return result
    return wrapper


def scrape_callback(scraped:List[str], session:InteractSession):
    session.set_scraped(scraped)
    session.save_scraped()
    update_message(session, scrape_followers_callback_text.format(len(scraped)))


def check_dm_queue():
    result = dmqueue.unfinished_tasks
    if result > 0:
        return True
    return False


def check_tag_queue():
    result = tagqueue.unfinished_tasks
    if result > 0:
        return True
    return False


#################################################
### DM PROCESS ##################################
def enqueue_dm_process(session:InteractSession):
    dmqueue.add_task(enqueue_dms, session)


@error_proof
def enqueue_dms(session:InteractSession):
    account_jobs:List[List[str]] = list()
    session.get_creds()

    # TODO: Scrape Users
    update_message(session, enqueing_dms_text)
    if not session.get_scraped():
        result = scrape_job(session)
        if result[0]:
            followers = result[1].get_scraped()
        else:
            return (False, session)
    else:
        followers = session.get_scraped()

    # Get Available Accounts
    if not session.accounts:
        session.get_creds()
        session.set_accounts({session.username: session.password})
    for account in session.accounts.keys():
        account_jobs.append(list())
    applogger.debug(f'Account Jobs: {account_jobs}')

    # Divide Targets between available accounts
    for index, follower in enumerate(followers):
        index = index % len(account_jobs)
        account_jobs[index].append(follower)
    applogger.debug(f'Account Jobs: {account_jobs}')

    # Turn into Dict:
    tasks_args = dict()
    for index, account in enumerate(list(session.accounts.keys())):
        tasks_args[account] = account_jobs[index]
    applogger.debug(f'Tassk Args: {tasks_args}')

    # Thread names list:
    names = list()
    for account in session.accounts.keys():
        names.append(f'dms:{session.user_id}:{account}')
    applogger.debug(f'Thread names: {names}')

    # Enqueue all tasks in different queues
    subqueue = TaskQueue(num_workers=len(session.accounts.keys()), names=names)
    for index, account in enumerate(session.accounts.keys()):
        creds = {account: session.accounts.get(account)}
        subqueue.add_task(dm_job, session=session, creds=creds, targets=tasks_args.get(account))
    applogger.info(f'Started {len(subqueue.workers)} DM threads')
    
    # Wait for everything to finish
    subqueue.close()
    applogger.info(f'Messaged {len(session.get_messaged())} users out of {len(followers)}')

    update_message(session, follow_successful_text.format(len(session.get_messaged()), session.target), final=True)
    return (True, session)


def dm_job(session:InteractSession, creds:dict, targets:List[str]) -> Tuple[bool, Optional[InteractSession]]:
    applogger.info(f'Starting Dm Job <{session.target}>')
    
    client = init_client()
    update_message(session, logging_in_text)
    try:
        client.login(list(creds.keys())[0], creds.get(list(creds.keys())[0]))
    except (InvalidUserError, InvaildPasswordError):
        client.disconnect()
        return (False, None)
    except VerificationCodeNecessary:
        client.disconnect()
        return (False, None)

    # FOR EACH USER
    for index, follower in enumerate(targets):
        # Send DM to User
        update_message(session, inform_messages_status_text.format(len(session.get_scraped()), len(session.get_messaged())))
        try:
            client.send_dm(follower, session.get_text())
            global lock
            with lock:
                session.add_messaged(follower)
        except Exception as error:
            applogger.error(f'Error in sending message to <{follower}>', exc_info=error)
        finally:
            if len(session.get_scraped()) > 5:
                text = inform_messages_status_text.format(len(session.get_scraped()), len(session.get_messaged())) + f'\nWaiting a bit...'
                update_message(session, text)
                action = randint(1, 3)
                scrolls = randrange(1, 9)
                interval = randrange(1, 4)
                if action is 1:
                    client.driver.get(ClientUrls.HOME_URL)
                    for scroll in range(scrolls):
                        client.scroll(interval=interval)
                else:
                    client.driver.get('https://www.instagram.com/explore/')
                    for scroll in range(scrolls):
                        client.scroll(interval=interval)

                time.sleep(randrange(60, 135))

    client.disconnect()
    return (True, session)


#################################################
### TAG PROCESS ##################################
def enqueue_tag_process(session:InteractSession):
    tagqueue.add_task(enqueue_tags, session)


def enqueue_tags(session:InteractSession):
    account_jobs:List[List[str]] = list()
    session.get_creds()

    # TODO: Scrape Users
    update_message(session, enqueing_tags_text)
    if not session.get_scraped():
        result = scrape_job(session)
        if result[0]:
            followers = result[1].get_scraped()
        else:
            return (False, session)
    else:
        followers = session.get_scraped()

    # Get Available Accounts
    if not session.accounts:
        session.get_creds()
        session.set_accounts({session.username: session.password})
    for account in session.accounts.keys():
        account_jobs.append(list())
    applogger.debug(f'Account Jobs: {account_jobs}')

    # Divide Targets between available accounts
    for index, follower in enumerate(followers):
        index = index % len(account_jobs)
        account_jobs[index].append(follower)
    applogger.debug(f'Account Jobs: {account_jobs}')

    # Turn into Dict:
    tasks_args = dict()
    for index, account in enumerate(list(session.accounts.keys())):
        tasks_args[account] = account_jobs[index]
    applogger.debug(f'Tassk Args: {tasks_args}')

    # Thread names list:
    names = list()
    for account in session.accounts.keys():
        names.append(f'tags:{session.user_id}:{account}')
    applogger.debug(f'Thread names: {names}')

    # Enqueue all tasks in different queues
    subqueue = TaskQueue(num_workers=len(session.accounts.keys()), names=names)
    for index, account in enumerate(session.accounts.keys()):
        creds = {account: session.accounts.get(account)}
        subqueue.add_task(tag_job, session=session, creds=creds, targets=tasks_args.get(account))
    applogger.info(f'Started {len(subqueue.workers)} TAG threads')
    
    # Wait for everything to finish
    subqueue.close()
    applogger.info(f'Tagged {len(session.get_tagged())} users out of {len(followers)}')

    update_message(session, follow_successful_text.format(len(session.get_tagged()), session.target), final=True)
    return (True, session)


def tag_job(session:InteractSession, creds:dict, targets:List[str]) -> Tuple[bool, Optional[InteractSession]]:
    global lock
    applogger.info(f'Starting Tag Job <{session.target}>')
    
    client = init_client()
    update_message(session, logging_in_text)
    try:
        client.login(list(creds.keys())[0], creds.get(list(creds.keys())[0]))
    except (InvalidUserError, InvaildPasswordError):
        client.disconnect()
        return (False, None)
    except VerificationCodeNecessary:
        client.disconnect()
        return (False, None)

    # GET POST
    try:
        post = client.get_post(session.post)
    except:
        applogger.exception(f'Impossible to get post of shortcode <{session.post}>')
        update_message(session, error_getting_post_text.format(session.post), final=True)
        return (False, session)


    users:List[List[str]] = list()
    sublist:List[str] = list()
    for user in targets:
        if len(sublist) < 5:
            sublist.append(user)
            continue
        users.append(sublist)
        sublist = list()
    if len(sublist) > 0:
        users.append(sublist)
    applogger.debug(f'Users Divided List: {users}')


    for sublist in users:
        text = ''
        for index, user in enumerate(sublist):
            text += f'@{user} '
        applogger.debug(f'Text: {text}')

        # Send DM to User
        url = 'https://www.instagram.com/p/{}/'.format(session.post)
        update_message(session, inform_tags_status_text.format(len(session.get_scraped()), url, len(session.get_tagged())))
        try:
            post.add_comment(text)
            with lock:
                session.add_tagged(sublist)
        except Exception as error:
            applogger.error(f'Error in tagging users to <{session.post}>', exc_info=error)
            with lock:
                for username in sublist:
                    session.add_failed(username)
        finally:
            if len(session.get_scraped()) > 15:
                text = inform_tags_status_text.format(len(session.get_scraped()), url, len(session.get_tagged())) + f'\nWaiting a bit...'
                update_message(session, text)
                action = randint(1, 3)
                scrolls = randrange(1, 3)
                interval = randrange(1, 3)
                if action is 1:
                    client.driver.get(ClientUrls.HOME_URL)
                    for scroll in range(scrolls):
                        client.scroll(interval=interval)
                else:
                    client.driver.get('https://www.instagram.com/explore/')
                    for scroll in range(scrolls):
                        client.scroll(interval=interval)
                time.sleep(randrange(5, 15))

    client.disconnect()
    return (True, session)


#################################################
### SCRAPE PROCESS ##################################
@error_proof
def scrape_job(session:InteractSession) -> Tuple[bool, Optional[InteractSession]]:
    client = init_client()

    update_message(session, logging_in_text)
    try:
        client.login(session.username, session.password)
    except (InvalidUserError, InvaildPasswordError):
        client.disconnect()
        return (False, None)
    except VerificationCodeNecessary:
        client.disconnect()
        return (False, None)

    update_message(session, waiting_scrape_text)
    try:
        followers = client.get_followers(session.target, session.count, deep_scrape=False)
        session.set_scraped(followers)
        session.save_scraped()
        client.disconnect()
        return (True, session)
    except Exception as error:
        applogger.error(f'Error in scraping <{session.target}>\'s followers: ', exc_info=error)
        client.disconnect()
        update_message(session, operation_error_text.format(len(session.get_scraped())))
        return (False, None)

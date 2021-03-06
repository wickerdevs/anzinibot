from logging import Filter

from telegram import update
from anzinibot import telelogger
from anzinibot.bot.commands.login import *
from anzinibot.bot.commands.help import *
from anzinibot.bot.commands.logout import *
from anzinibot.bot.commands.account import *
from anzinibot.bot.commands.start import *
from anzinibot.bot.commands.senddm import *
from anzinibot.bot.commands.tag import *
from anzinibot.bot.commands.delpinnedmsg import *
from anzinibot.bot.commands.clearscraped import *
from anzinibot.bot.commands.incorrect import *
from anzinibot.models.callbacks import *

applogger.debug('Setup module imported')

def setup(updater):
    telelogger.debug('Bot setup running...')
    dp:Dispatcher = updater.dispatcher

    instagram_handler = ConversationHandler(
        entry_points=[CommandHandler('login', ig_login), CallbackQueryHandler(ig_login, pattern=Callbacks.LOGIN, run_async=True)],
        states={
            InstaStates.INPUT_USERNAME: [MessageHandler(Filters.text, instagram_username, run_async=True)],
            InstaStates.INPUT_PASSWORD: [MessageHandler(Filters.text, instagram_password, run_async=True)],
            InstaStates.INPUT_SECURITY_CODE: [MessageHandler(Filters.text, instagram_security_code, run_async=True)],
        },
        fallbacks=[CallbackQueryHandler(cancel_instagram, pattern=Callbacks.CANCEL, run_async=True), CallbackQueryHandler(instagram_resend_scode, pattern=Callbacks.RESEND_CODE, run_async=True)]
    )


    # TODO implement senddm handler
    dm_handler = ConversationHandler(
        entry_points=[CommandHandler('dm', senddm_def)],
        states={
            InteractStates.SCRAPE: [CallbackQueryHandler(select_scrape)],
            InteractStates.SCRAPEACCOUNT: [MessageHandler(Filters.text, select_scrape_account)],
            InteractStates.POST_URL: [MessageHandler(Filters.text, input_dm_post_url)],
            InteractStates.COUNT: [CallbackQueryHandler(select_count)],
            InteractStates.MESSAGE: [MessageHandler(Filters.text, input_message)],
            InteractStates.INPUTACCOUNTS: [MessageHandler(Filters.document, input_accounts)],
            InteractStates.CONFIRM: [CallbackQueryHandler(confirm_dms)],
        },
        fallbacks=[CallbackQueryHandler(cancel_send_dm, pattern=Callbacks.CANCEL), CallbackQueryHandler(dm_skip, pattern=Callbacks.DMSKIP)]
    )

    tag_handler = ConversationHandler(
        entry_points=[CommandHandler('tag', tag_def)],
        states={
            TagStates.POST_URL: [MessageHandler(Filters.text, input_post_url)],
            TagStates.SCRAPE: [CallbackQueryHandler(select_tag_scrape)],
            TagStates.SCRAPEACCOUNT: [MessageHandler(Filters.text, select_tag_scrape_account)],
            TagStates.COUNT: [CallbackQueryHandler(select_tag_count)],
            TagStates.INPUTACCOUNTS: [MessageHandler(Filters.document, input_tag_accounts)],
            TagStates.CONFIRM: [CallbackQueryHandler(confirm_tags)],
        },
        fallbacks=[CallbackQueryHandler(cancel_tag, pattern=Callbacks.CANCEL), CallbackQueryHandler(tag_skip, pattern=Callbacks.TAGSKIP)]
    )


    # Commands
    dp.add_handler(CommandHandler('start', start_def))
    dp.add_handler(CommandHandler("help", help_def, run_async=True))
    # Check / Switch account 
    dp.add_handler(CommandHandler('account', check_account,  run_async=True))
    dp.add_handler(CallbackQueryHandler(check_account, pattern=Callbacks.ACCOUNT))
    dp.add_handler(CallbackQueryHandler(switch_account, pattern=Callbacks.SWITCH))
    dp.add_handler(CallbackQueryHandler(select_switched_account, pattern=Callbacks.SELECTSWITCH))
    dp.add_handler(CallbackQueryHandler(help_def, pattern=Callbacks.HELP))

    # Log Out
    dp.add_handler(CommandHandler('logout', instagram_log_out, run_async=True))
    dp.add_handler(CallbackQueryHandler(instagram_log_out, pattern=Callbacks.LOGOUT, run_async=True))

    # Clear Scraped Data
    dp.add_handler(CallbackQueryHandler(clear_scraped_def, pattern=Callbacks.SCRAPED_DATA))
    dp.add_handler(CallbackQueryHandler(confirm_clear_data, pattern=Callbacks.DELETE_SCRAPED_DATA))
    
    dp.add_handler(instagram_handler)
    dp.add_handler(dm_handler)
    dp.add_handler(tag_handler)

    # OTHERS
    dp.add_handler(CallbackQueryHandler(delpinnedmsg_def, pattern=Callbacks.DELETE_PINNED_MESSAGE))

    # FALLBACK
    dp.add_handler(MessageHandler(Filters.text, incorrect_command))
    dp.add_handler(MessageHandler(Filters.command, incorrect_command))

    dp.add_error_handler(error)
    telelogger.debug('Bot setup complete!')
    return updater

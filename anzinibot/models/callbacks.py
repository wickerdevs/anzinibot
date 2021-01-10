class Callbacks:
    """Object to store PTB conversations Callbacks"""
    # COMMANDS CALLBACKS
    ACCOUNT = 'ACCOUNT'
    EDIT_SETTINGS = 'EDIT_SETTINGS'
    NOTIFS = 'NOTIFS'
    LOGOUT = 'LOGOUT'
    LOGIN = 'LOGIN'
    SWITCH = 'SWITCH'
    HELP = 'HELP'
    DELETE_PINNED_MESSAGE = 'DELETE_PINNED_MESSAGE'
    SCRAPED_DATA = 'SCRAPED_DATA'


    # BUTTON CALLBACKS
    DMSKIP = 'DMSKIP'
    TAGSKIP = 'TAGSKIP'
    SELECTSWITCH = 'SELECTSWITCH'
    CANCEL = 'CANCEL'
    NONE = 'NONE'
    DONE= 'DONE'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    SELECT = 'SELECT'
    UNSELECT = 'UNSELECT'
    CONFIRM = 'CONFIRM'
    REQUEST_CODE = 'REQUEST_CODE'
    TEN = '10'
    TFIVE = '25'
    FIFTY = '50'
    SFIVE = '75'
    RESEND_CODE = 'RESEND_CODE'
    DELETE_SCRAPED_DATA = 'DELETE_SCRAPED_DATA'
    


class InstaStates:
    """Object to store PTB InstaSession Conversation Handler states indicators"""
    INPUT_VERIFICATION_CODE = 1
    INPUT_USERNAME = 2
    INPUT_PASSWORD = 3
    INPUT_SECURITY_CODE = 4


class ScrapeStates:
    """Object to store PTB Follow Conversation Handler states indicators"""
    ACCOUNT = 1
    COUNT = 2
    CONFIRM = 3


class InteractStates:
    SCRAPE = 1
    SCRAPEACCOUNT = 2
    COUNT = 3
    INPUTACCOUNTS = 7
    MESSAGE = 4
    CONFIRM = 5


class TagStates:
    POST_URL = 1
    SCRAPE = 2
    SCRAPEACCOUNT = 3
    COUNT = 4
    INPUTACCOUNTS = 5
    CONFIRM = 6


class SettingsStates:
    """Object to store PTB Settings Conversation Handler states indicators"""
    SELECT = 1
    COMMENT = 4
    INTERACTION_COUNT = 2
    CANCEL = 5


class StartStates:
    """Object to store PTB Start Conversation Handler states indicators"""
    TEXT = 1


class Objects:
    PERSISTENCE = 1
    INSTASESSION = 2
    SETTINGS = 3
    FOLLOW = 4
from anzinibot.modules import config
from typing import Optional, List
from anzinibot.models.interaction import Interaction
from anzinibot.models.persistence import Persistence, persistence_decorator
from anzinibot.models.instasession import InstaSession
import time


class InteractSession(InstaSession):
    def __init__(self, user_id:int, method:str=Persistence.INTERACT, target:str=None, post:str=None, message_id:int=None, text:str=None, accounts: Optional[dict]=None, proxies:Optional[List[str]]=None, interaction:Optional[Interaction]=None) -> None:
        super(InstaSession, self).__init__(method=method, user_id=user_id, message_id=message_id)
        self.target = target
        self.post = post
        self.count = 0
        self.text = text
        self.accounts = accounts
        self.proxies = proxies
        self.interaction = interaction

    def __repr__(self) -> str:
        return f'Follow<{self.target}>'

    def get_target(self):
        return self.target

    def get_count(self):
        return self.count

    def get_text(self):
        return self.text

    def get_scraped(self):
        if not self.interaction.scraped:
            return list()
        return self.interaction.scraped.copy()

    def get_messaged(self):
        if not self.interaction.messaged:
            return list()
        return self.interaction.messaged.copy()

    def get_tagged(self):
        if not self.interaction.tagged:
            return list()
        return self.interaction.tagged.copy()

    def get_failed(self):
        if not self.interaction.failed:
            return list()
        return self.interaction.failed.copy()

    @persistence_decorator
    def set_interaction(self, interaction):
        self.interaction = interaction

    @persistence_decorator
    def set_target(self, target):
        self.target = target

    @persistence_decorator
    def set_post(self, shortcode):
        self.post = shortcode

    @persistence_decorator
    def set_count(self, count):
        self.count = count

    @persistence_decorator
    def set_text(self, text):
        self.text = text

    @persistence_decorator
    def set_accounts(self, accounts:dict):
        self.accounts = accounts

    @persistence_decorator
    def set_proxies(self, proxies:list):
        self.proxies = proxies

    @persistence_decorator
    def set_scraped(self, scraped):
        self.interaction.scraped = scraped

    @persistence_decorator
    def set_messaged(self, messaged):
        self.interaction.messaged = messaged

    @persistence_decorator
    def set_tagged(self, tagged:list):
        self.interaction.tagged = tagged

    @persistence_decorator
    def set_failed(self, failed):
        self.interaction.failed = failed


    @persistence_decorator
    def add_failed(self, failed):
        if not self.interaction.failed:
            self.interaction.failed = list()
        self.interaction.failed.append(failed)


    @persistence_decorator
    def add_messaged(self, messaged):
        self.interaction.add_messaged(messaged)


    @persistence_decorator
    def add_tagged(self, tagged:str):
        self.interaction.add_tagged(tagged)


    def save_scraped(self):
        if self.interaction:
            config.set_scraped(self.interaction)

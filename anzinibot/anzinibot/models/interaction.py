from anzinibot.modules.config import get_message
from typing import Dict, List, Union, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from instaclient.instagram import *
    from instaclient.client.instaclient import InstaClient


class Interaction:
    def __init__(self,
    target:Union['Profile', str],
    scraped:List[str]=None,
    failed:List[str]=None,
    messaged:List[str]=None,
    tagged:List[str]=None) -> None:
        self.target = target
        self.scraped = scraped
        self.messaged = messaged
        self.tagged = tagged
        self.failed = failed
        

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Interaction):
            if self.target == o.target:
                for item in o.scraped:
                    if item not in self.scraped:
                        return False
                for item in o.messaged:
                    if item not in self.messaged:
                        return False
                for item in o.failed:
                    if item not in self.failed:
                        return False
                return True
        return False


    def __getitem__(self, item: str):
        return self.__dict__[item]


    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            value = self.__dict__[key]
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if hasattr(item, 'to_dict'):
                        value[index] = value[index].to_dict()
            else:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        return data


    @classmethod
    def de_json(cls, data: dict, client:Optional['InstaClient']=None):

        if not data:
            return None

        for key in data:
            if hasattr(data[key], 'de_json'):
                data[key] = Profile.de_json(data[key], client)

        obj = cls(**data)  # type: ignore[call-arg]
        return obj


    def set_scraped(self, scraped:List[str]):
        self.scraped = scraped


    def add_messaged(self, username:str):
        if not self.messaged:
            self.messaged = list()
        if username not in self.messaged:
            self.messaged.append(username)

    
    def add_tagged(self, username:str):
        if not self.tagged:
            self.tagged = list()
        
        if isinstance(username, str) and username not in self.tagged:
            self.tagged.append(username)
        elif isinstance(username, list):
            for user in username:
                if user not in self.tagged:
                    self.tagged.append(user)
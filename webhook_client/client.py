import requests
import os
import json

from .errors import WebhookError, InvalidWebhook
from .colour import Colour
from .types import *
from .embed import Embed

class WebhookClient:
    def __init__(self, webhook_url: str, username: str = None, avatar_url: str = None):
        """ Create a WebhookClient instance.
        :param webhook_url: the webhook url the client connects to
        :param username: (optional) the username the webhook should have
        :param avatar_url: (optional) the avatar url the webhook should have"""
        self.webhook_url = webhook_url
        self.username = username
        self.avatar_url = avatar_url
        self.check_webhook(str(webhook_url))

    def check_webhook(self, webhook_url):
        r = requests.get(str(webhook_url))
        if r.status_code in [200, 204]:
            pass
        else:
            raise InvalidWebhook('The webhook you provided is invalid.')

    def to_dict(self, embed):
        if isinstance(embed, (dict)):
            return embed
        elif isinstance(embed, (Embed)):
            return embed.to_dict()
        else:
            return {'title': 'Invalid Embed.'}

    def build_json(self, webhook_url, content: str = None, embeds: list = None, username: str = None, avatar_url: str = None, tts: bool = False):
        json_data = {}
        embed_list = []
        
        if embeds:
            for embed in embeds:
                embed_list.append(self.to_dict(embed))
        else:
            embed_data = {'embeds': None}
        
        json_data['content'] = content
        json_data['embeds'] = embed_list
        json_data['username'] = username
        json_data['avatar_url'] = avatar_url
        json_data['tts'] = tts

        return json_data
    
    def build_query(self, webhook_url: str, thread_id: int = None):
        base_url = f"{webhook_url}"
        if thread_id:
            base_url += f"?thread_id={str(thread_id)}"
        return str(base_url)

    def send(self, content: str = None, embeds: list = None, tts: bool = False, thread_id: int = None):
        """ Send a message to your WebhookClient.
        
        
        content: :class:`str`
            The content for the message.
        embeds: :class:`list`
            List of `Embed`s to send in the message.
        tts: :class:`bool`
            Whether or not the message should be sent as text-to-speech. Defaults to `False`.
        thread_id: :class:`int`
            The thread ID that the webhook should be posted in. Defaults to `None`. """
        json_data = self.build_json(self.webhook_url, content, embeds, self.username, self.avatar_url, tts)
        query_str = self.build_query(self.webhook_url, thread_id)
        r = requests.post(str(query_str), json=json_data)
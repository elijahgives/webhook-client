from typing import List, Literal, TypedDict

class _EmbedFooterOptional(TypedDict, total=False):
    icon_url: str
    proxy_icon_url: str

class EmbedFooter(_EmbedFooterOptional):
    text: str

class _EmbedFieldOptional(TypedDict, total=False):
    inline: bool

class EmbedField(_EmbedFieldOptional):
    name: str
    value: str

class EmbedThumbnail(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedVideo(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedImage(TypedDict, total=False):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedProvider(TypedDict, total=False):
    name: str
    url: str

class EmbedAuthor(TypedDict, total=False):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

EmbedType = Literal['rich', 'image', 'video', 'gifv', 'article', 'link']
import datetime
from typing import Any, Dict, Final, List, Mapping, Protocol, TYPE_CHECKING, Type, TypeVar, Union
from .colour import Colour
from .types import EmbedType

class _EmptyEmbed:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return 'Embed.Empty'

    def __len__(self) -> int:
        return 0


EmptyEmbed: Final = _EmptyEmbed()

class Embed:
    """Represents a Discord embed.
    
    title: :class:`str`
        The title of the embed.
    type: :class:`str`
        The type of embed. Usually "rich".
    description: :class:`str`
        The description of the embed.
    url: :class:`str`
        The URL of the embed.
    timestamp: :class:`datetime.datetime`
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone.
    colour: Union[:class:`Colour`, :class:`int`]
        The colour code of the embed. Aliased to ``color`` as well.
    Empty
        A special sentinel value used by ``EmbedProxy`` and this class
        to denote that the value or attribute is empty.
    """

    __slots__ = (
        'title',
        'url',
        'type',
        '_timestamp',
        '_colour',
        '_footer',
        '_image',
        '_thumbnail',
        '_video',
        '_provider',
        '_author',
        '_fields',
        'description',
    )

    Empty: Final = EmptyEmbed

    def __init__(
        self,
        *,
        colour: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
        color: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
        title: str = EmptyEmbed,
        type: EmbedType = 'rich',
        url: str = EmptyEmbed,
        description: str = EmptyEmbed,
        timestamp: datetime.datetime = None,
    ):

        self.colour = colour if colour else color
        self.title = title
        self.type = type
        self.url = url
        self.description = description

        if self.title is not EmptyEmbed:
            self.title = str(self.title)

        if self.description is not EmptyEmbed:
            self.description = str(self.description)

        if self.url is not EmptyEmbed:
            self.url = str(self.url)

        if timestamp:
            self.timestamp = timestamp

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        """Converts a :class:`dict` to a :class:`Embed` provided it is in the
        format that Discord expects it to be in.
        You can find out about this format in the `official Discord documentation`__.
        .. _DiscordDocs: https://discord.com/developers/docs/resources/channel#embed-object
        __ DiscordDocs_
        Parameters
        -----------
        data: :class:`dict`
            The dictionary to convert into an embed.
        """
        # we are bypassing __init__ here since it doesn't apply here
        self = cls.__new__(cls)

        # fill in the basic fields

        self.title = data.get('title', None)
        self.type = data.get('type', None)
        self.description = data.get('description', None)
        self.url = data.get('url', None)

        if self.title:
            self.title = str(self.title)

        if self.description:
            self.description = str(self.description)

        if self.url:
            self.url = str(self.url)

        try:
            self._colour = Colour(value=data['color'])
        except KeyError:
            pass

        for attr in ('thumbnail', 'video', 'provider', 'author', 'fields', 'image', 'footer'):
            try:
                value = data[attr]
            except KeyError:
                continue
            else:
                setattr(self, '_' + attr, value)

        return self

    def copy(self):
        """Returns a shallow copy of the embed."""
        return self.__class__.from_dict(self.to_dict())

    def __len__(self) -> int:
        total = len(self.title) + len(self.description)
        for field in getattr(self, '_fields', []):
            total += len(field['name']) + len(field['value'])

        try:
            footer_text = self._footer['text']
        except (AttributeError, KeyError):
            pass
        else:
            total += len(footer_text)

        try:
            author = self._author
        except AttributeError:
            pass
        else:
            total += len(author['name'])

        return total

    def __bool__(self) -> bool:
        return any(
            (
                self.title,
                self.url,
                self.description,
                self.colour,
                self.fields,
                self.timestamp,
                self.author,
                self.thumbnail,
                self.footer,
                self.image,
                self.provider,
                self.video,
            )
        )

    @property
    def colour(self):
        return getattr(self, '_colour', EmptyEmbed)

    @colour.setter
    def colour(self, value: Union[int, Colour]):  # type: ignore
        if isinstance(value, (Colour)):
            self._colour = value
        elif isinstance(value, int):
            self._colour = Colour(value=value)
        else:
            self._colour = None

    color = colour

    @property
    def timestamp(self):
        return getattr(self, '_timestamp', EmptyEmbed)

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                value = value.astimezone()
            self._timestamp = value
        elif isinstance(value, None):
            self._timestamp = value
        else:
            raise TypeError(f"Expected datetime.datetime or Embed.Empty received {value.__class__.__name__} instead")

    def set_footer(self, *, text: str, icon_url: str = None):
        """Sets the footer for the embed content.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        text: :class:`str`
            The footer text.
        icon_url: :class:`str`
            The URL of the footer icon. Only HTTP(S) is supported.
        """

        self._footer = {}
        if text:
            self._footer['text'] = str(text)

        if icon_url:
            self._footer['icon_url'] = str(icon_url)

        return self

    def set_image(self, *, url: str = None):
        """Sets the image for the embed content.
        This function returns the class instance to allow for fluent-style
        chaining.
        .. versionchanged:: 1.4
            Passing :attr:`Empty` removes the image.
        Parameters
        -----------
        url: :class:`str`
            The source URL for the image. Only HTTP(S) is supported.
        """

        if not url:
            try:
                del self._image
            except AttributeError:
                pass
        else:
            self._image = {
                'url': str(url),
            }

        return self

    def set_thumbnail(self, *, url: str = None):
        """Sets the thumbnail for the embed content.
        This function returns the class instance to allow for fluent-style
        chaining.
        .. versionchanged:: 1.4
            Passing :attr:`Empty` removes the thumbnail.
        Parameters
        -----------
        url: :class:`str`
            The source URL for the thumbnail. Only HTTP(S) is supported.
        """

        if not url:
            try:
                del self._thumbnail
            except AttributeError:
                pass
        else:
            self._thumbnail = {
                'url': str(url),
            }

        return self


    def set_author(self, *, name: str, url: str = None, icon_url: str = None):
        """Sets the author for the embed content.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        name: :class:`str`
            The name of the author.
        url: :class:`str`
            The URL for the author.
        icon_url: :class:`str`
            The URL of the author icon. Only HTTP(S) is supported.
        """

        self._author = {
            'name': str(name),
        }

        if url:
            self._author['url'] = str(url)

        if icon_url:
            self._author['icon_url'] = str(icon_url)

        return self

    def add_field(self, *, name: str, value: str, inline: bool = True):
        """Adds a field to the embed object.
        This function returns the class instance to allow for fluent-style
        chaining.
        Parameters
        -----------
        name: :class:`str`
            The name of the field.
        value: :class:`str`
            The value of the field.
        inline: :class:`bool`
            Whether the field should be displayed inline.
        """

        field = {
            'inline': inline,
            'name': str(name),
            'value': str(value),
        }

        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [field]

        return self

    def to_dict(self):
        """ Convert embed object to dict """
        result = {
            key[1:]: getattr(self, key)
            for key in self.__slots__
            if key[0] == '_' and hasattr(self, key)
        }
        try:
            colour = result.pop('colour')
        except KeyError:
            pass
        else:
            if colour:
                result['color'] = colour.value
        try:
            timestamp = result.pop('timestamp')
        except KeyError:
            pass
        else:
            if timestamp:
                if timestamp.tzinfo:
                    result['timestamp'] = timestamp.astimezone(tz=datetime.timezone.utc).isoformat()
                else:
                    result['timestamp'] = timestamp.replace(tzinfo=datetime.timezone.utc).isoformat()
        if self.type:
            result['type'] = self.type
        if self.description:
            result['description'] = self.description
        if self.url:
            result['url'] = self.url
        if self.title:
            result['title'] = self.title
        return result
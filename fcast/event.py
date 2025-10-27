from dataclasses import dataclass
from enum import Enum
from .event_type import EventType
from .media import MediaItem
import logging
from copy import copy

l = logging.getLogger(__name__)


class KeyNames(Enum):
	Left = "ArrowLeft"
	Right = "ArrowRight"
	Up = "ArrowUp"
	Down = "ArrowDown"
	Ok = "Enter"


@dataclass
class EventSub:
	@property
	def type(self) -> EventType:
		from .utils import EventSubToType
		l.debug(f"{type(self)} EventType: {EventSubToType[type(self)]}")
		return EventSubToType[type(self)]
	

@dataclass
class MediaItemStart(EventSub):
	...


@dataclass
class MediaItemEnd(EventSub):
	...


@dataclass
class MediaItemChange(EventSub):
	...


@dataclass
class KeyDown(EventSub):
	...


@dataclass
class KeyUp(EventSub):
	...


@dataclass
class Event:
	type: EventType
	@property
	def json(self) -> dict:
		return self.__dict__


@dataclass
class MediaItemE(Event):
	item: MediaItem
	
	@property
	def item(self) -> MediaItem:
		return self._item
	
	@item.setter
	def item(self, value: dict|MediaItem):
		if type(value) == dict:
			self._item = MediaItem(**value)
		elif isinstance(value, MediaItem):
			self._item = value
		else:
			raise KeyError(f"Invalid value provided for item: {value}")

	@property
	def json(self) -> dict:
		res = copy(self.__dict__)
		res.pop("_item")
		res["item"] = self.item.json
		return res


@dataclass
class Key(Event):
	key: str
	repeat: bool
	handled: bool
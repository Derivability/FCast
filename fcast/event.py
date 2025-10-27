from dataclasses import dataclass
from enum import Enum
from .event_type import EventType
from .media import MediaItem
import logging

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
		from .utils import EventToType
		l.debug(f"{type(self)} EventType: {EventToType[type(self)]}")
		return EventToType[type(self)]
	

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


@dataclass
class MediaItem(Event):
	item: MediaItem


@dataclass
class Key(Event):
	key: str
	repeat: bool
	handled: bool
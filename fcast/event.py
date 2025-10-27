from dataclasses import dataclass
from enum import Enum
from .event_type import EventType
import logging

l = logging.getLogger(__name__)


class KeyNames(Enum):
	Left = "ArrowLeft"
	Right = "ArrowRight"
	Up = "ArrowUp"
	Down = "ArrowDown"
	Ok = "Enter"


@dataclass
class Event:
	@property
	def type(self) -> EventType:
		from .utils import EventToType
		l.debug(f"{type(self)} EventType: {EventToType[type(self)]}")
		return EventToType[type(self)]
	

@dataclass
class MediaItemStart(Event):
	...


@dataclass
class MediaItemEnd(Event):
	...


@dataclass
class MediaItemChange(Event):
	...


@dataclass
class KeyDown(Event):
	...


@dataclass
class KeyUp(Event):
	...
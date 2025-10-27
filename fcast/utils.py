from .opcode import Opcode
from .message import *
from .event_type import EventType
from .event import *


OpcodeToMessage = {
    Opcode.play: Play,
    Opcode.pause: Pause,
    Opcode.resume: Resume,
    Opcode.stop: Stop,
    Opcode.seek: Seek,
    Opcode.playback_update: PlaybackUpdate,
    Opcode.volume_update: VolumeUpdate,
    Opcode.set_volume: SetVolume,
    Opcode.playback_error: PlaybackError,
    Opcode.set_speed: SetSpeed,
	Opcode.version: Version,
    Opcode.ping: Ping,
    Opcode.pong: Pong,
	Opcode.initial: Initial,
    Opcode.play_update: PlayUpdate,
    Opcode.set_playlist_item: SetPlaylistItem,
    Opcode.event: EventM
}

MessageToOpcode = {v:k for k,v in OpcodeToMessage.items()}


TypeToEvent = {
    EventType.MediaItemStart: MediaItemStart,
    EventType.MediaItemEnd: MediaItemEnd,
    EventType.MediaItemChange: MediaItemChange,
    EventType.KeyDown: KeyDown,
    EventType.KeyUp: KeyUp
}

EventToType = {v:k for k,v in TypeToEvent.items()}
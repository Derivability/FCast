from dataclasses import dataclass
from typing import Optional, Any
from enum import Enum


class ContentType(Enum):
	Playlist = 0


@dataclass
class MetadataType:
	title: str = None
	thumbnailUrl: str = None
	custom: Any = None


@dataclass
class MediaItem:
	container: str #The MIME type (video/mp4)
	url: Optional[str] = None #The URL to load (optional)
	content: Optional[str] = None #The content to load (i.e. a DASH manifest, optional)
	time: float = 0 #The time to start playing in seconds
	volume: float = None # The desired volume (0-1)
	speed: float = 1.0 #The factor to multiply playback speed by (defaults to 1.0)
	cache: bool = None # Indicates if the receiver should preload the media item
	showDuration: float = None # Indicates how long the item content is presented on screen in seconds
	headers: Optional[dict] = None #HTTP request headers to add to the play request Map<string, string>
	metadata: MetadataType = None


@dataclass
class PlaylistContent:
	items: list[MediaItem]
	contentType: ContentType = ContentType.Playlist
	offset: int = None# Start position of the first item to play from the playlist
	volume: float = None # The desired volume (0-1)
	speed: float = 1.0 #The factor to multiply playback speed by (defaults to 1.0)
	forwardCache: bool = None # Count of media items should be pre-loaded forward from the current view index
	backwardCache: bool = None # Count of media items should be pre-loaded backward from the current view index
	metadata: MetadataType = None

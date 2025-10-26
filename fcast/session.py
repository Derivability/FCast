import socket
from .message import *
from .utils import OpcodesToMessages
from typing import Callable
from threading import Lock
import asyncio
import logging

l = logging.getLogger(__name__)

class FCastSession:
	subs = {}
	connected = False

	def __init__(self, host, port=46899):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.lock = Lock()
		
	def send(self, msg: Message):
		l.debug(f"Sending message: {msg}")
		self.sock.sendall(msg.as_bytes)

	def _recv(self) -> Message:
		resp_size = struct.unpack("<I", self.sock.recv(4))[0]
		resp_opcode = struct.unpack("B", self.sock.recv(1))[0]
		resp_body = self.sock.recv(resp_size-1).decode(encoding="utf-8")
		message_type = OpcodesToMessages[resp_opcode]
		if resp_size > 1:
			msg = message_type(**json.loads(resp_body))
		else:
			msg = message_type()
		l.debug(f"Received message: {msg}")
		return msg
	
	def _notify(self, msg: Message):
		if s := self.subs.get(type(msg)):
			for i in s:
				i(msg)

	def subscribe(self, subscriber: tuple[Message,Callable]):
		msg_type = subscriber[0]
		callback = subscriber[1]
		if s:=self.subs.get(msg_type):
			s.append(callback)
		else:
			self.subs[msg_type] = [callback]
	
	def unsubscribe(self, unsub: tuple[Message,Callable]):
		msg_type = unsub[0]
		callback = unsub[1]
		if s:=self.subs.get(msg_type):
			s.remove(callback)

	def connect(self):
		self.sock.connect((self.host, self.port))
		self.connected = True
	
	def disconnect(self):
		self.connected = False
		with self.lock:
			self.sock.close()

	def receive(self):
		while self.connected:
			self.lock.acquire()
			try:
				msg = self._recv()
			except TypeError as e:
				l.error(e)
				continue
			if t:=type(msg) == Ping:
				self.send(Pong())
			elif t == Version:
				self.send(Version(3))
			elif t == Initial:
				self.send(Initial())
			self._notify(msg)
			self.lock.release()


class FCastSessionAsync(FCastSession):
	def __init__(self, host, port=46899):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(False)
		self.loop = asyncio.get_running_loop()
		self.lock = asyncio.Lock()

	async def _recv(self) -> Message:
		resp_size = struct.unpack("<I", await self.loop.sock_recv(self.sock, 4))[0]
		resp_opcode = struct.unpack("B", await self.loop.sock_recv(self.sock, 1))[0]
		resp_body = (await self.loop.sock_recv(self.sock,resp_size-1)).decode(encoding="utf-8")
		message_type = OpcodesToMessages[resp_opcode]
		if resp_size > 1:
			msg = message_type(**json.loads(resp_body))
		else:
			msg = message_type()
		l.debug(f"Received message: {msg}")
		return msg
	
	async def connect(self):
		await self.loop.sock_connect(self.sock, (self.host,self.port))
		self.connected = True

	async def send(self, msg: Message):
		l.debug(f"Sending message: {msg}")
		await self.loop.sock_sendall(self.sock, msg.as_bytes)

	async def receive(self):
		while self.connected:
			self.lock.acquire()
			try:
				msg = await self._recv()
			except TypeError as e:
				l.error(e)
				continue
			if t:=type(msg) == Ping:
				await self.send(Pong())
			elif t == Version:
				await self.send(Version(3))
			elif t == Initial:
				await self.send(Initial())
			self._notify(msg)
			self.lock.release()
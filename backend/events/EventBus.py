from typing import Callable, Any

from eventpy.eventdispatcher import EventDispatcher

from backend.decorator.Singleton import singleton
from backend.events.ApplicationMessagesEnum import ApplicationMessagesEnum


@singleton
class EventBus:
	def __init__(self):
		self.dispatcher = EventDispatcher()

	def add_listener(self, event_type: ApplicationMessagesEnum, listener):
		self.dispatcher.appendListener(event_type, listener)

	def remove_listener(self, event_type: ApplicationMessagesEnum, listener):
		self.dispatcher.removeListener(event_type, listener)

	def dispatch(self, event_type: ApplicationMessagesEnum, data: Any):
		self.dispatcher.dispatch(event_type, data)


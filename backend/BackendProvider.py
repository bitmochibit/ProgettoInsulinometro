# In this file it will be defined the asyncio event loop to be used around the code
import asyncio
import threading
from asyncio import AbstractEventLoop
from typing import Optional, Callable, Any


class BackendProvider:
	_loop_instance: Optional[AbstractEventLoop] = None
	_loop_thread = None

	@staticmethod
	def get_event_loop():
		"""Returns the asyncio event loop instance."""
		if BackendProvider._loop_instance is None:
			BackendProvider().start_event_loop()

		return BackendProvider._loop_instance

	@staticmethod
	def run_async(coro, callback: Callable[[Any, Any], None] = None, timeout = 100):
		"""Runs a coroutine safely in the event loop."""
		async def with_timeout():
			return await asyncio.wait_for(coro, timeout=timeout)

		future = asyncio.run_coroutine_threadsafe(with_timeout(), BackendProvider.get_event_loop())
		if callback:
			future.add_done_callback(
				lambda fut: callback(fut.result() if fut.exception() is None else None, fut.exception())
			)


	def start_event_loop(self):
		"""Starts the asyncio event loop in a background thread."""
		if self._loop_instance and self._loop_instance.is_running():
			print("Event loop already running.")
			return
		BackendProvider._loop_instance = asyncio.new_event_loop()
		BackendProvider._loop_thread = threading.Thread(target=self._loop_instance.run_forever, daemon=True)
		BackendProvider._loop_thread.start()
		print("Asyncio event loop started")

	def stop_event_loop(self):
		"""Stops the asyncio event loop and joins the thread."""
		if self._loop_instance and self._loop_instance.is_running():
			self._loop_instance.call_soon_threadsafe(self._loop_instance.stop)
			self._loop_thread.join(timeout=5)  # Avoid indefinite blocking
			BackendProvider._loop_instance = None
			print("Asyncio event loop stopped")


	def __aexit__(self, exc_type, exc, tb):
		self.stop_event_loop()
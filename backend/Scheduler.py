import asyncio
import threading
from asyncio import AbstractEventLoop, Future
from typing import Optional, Callable, Any, Awaitable

from backend.decorator.Singleton import singleton


@singleton
class Scheduler:

    def __init__(self):
        self._loop_instance: Optional[AbstractEventLoop] = None
        self._loop_thread = None
        self._tasks = set()  # To keep track of running tasks

    @property
    def event_loop(self):
        if self._loop_instance is None:
            self.start_event_loop()

        return self._loop_instance

    def run_async(self, coro: Awaitable, callback: Optional[Callable[[Any, Optional[Exception]], None]] = None, timeout: Optional[float] = None):
        """
        Runs a coroutine in the event loop.
        """
        async def with_timeout():
            try:
                if timeout:
                    return await asyncio.wait_for(coro, timeout=timeout)
                else:
                    return await coro
            except asyncio.TimeoutError:
                raise TimeoutError(f"The coroutine exceeded the timeout of {timeout} seconds")

        def handle_task(fut: Future):
            # Cleanup completed tasks from the set
            self._tasks.discard(fut)
            if callback:
                try:
                    result = fut.result()
                    callback(result, None)
                except Exception as e:
                    callback(None, e)

        # Schedule the coroutine
        task = asyncio.run_coroutine_threadsafe(with_timeout(), self.event_loop)
        self._tasks.add(task)
        task.add_done_callback(handle_task)

    def stop_task(self, task: Future):
        """
        Cancels a running task.
        """
        if task in self._tasks:
            task.cancel()
            self._tasks.discard(task)

    def start_event_loop(self):
        """
        Starts the asyncio event loop in a background thread.
        """
        if self._loop_instance and self._loop_instance.is_running():
            print("Event loop already running.")
            return
        self._loop_instance = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._loop_instance.run_forever, daemon=True)
        self._loop_thread.start()
        print("Asyncio event loop started")

    def stop_event_loop(self):
        """
        Stops the asyncio event loop and joins the thread.
        """
        if self._loop_instance and self._loop_instance.is_running():
            # Cancel all running tasks first
            tasks = asyncio.all_tasks(loop=self._loop_instance)
            for task in tasks:
                task.cancel()
            # Stop the loop
            self._loop_instance.call_soon_threadsafe(self._loop_instance.stop)
            self._loop_thread.join(timeout=5)
            self._loop_instance = None
            print("Asyncio event loop stopped")

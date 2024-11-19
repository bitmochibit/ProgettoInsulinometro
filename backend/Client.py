import asyncio
import threading
from typing import Callable, Any

from bleak import BleakClient, BleakError
from bleak.backends import device

from backend.device.DeviceInfo import DeviceInfo
from backend.device.Scanner import Scanner


def notification_handler(sender, data):
	output = list(data)
	print("GATHERED DATA FROM DEVICE", output)


class Client:
	def __init__(self):
		self.last_connected_device: DeviceInfo = None
		self.bleak_client: BleakClient = None
		self.scanner = Scanner()
		self.is_connected = False
		self.loop = None
		self.loop_thread = None

	def _start_event_loop(self):
		"""Starts the asyncio event loop in a background thread."""
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)
		self.loop_thread = threading.Thread(target=self.loop.run_forever, daemon=True)
		self.loop_thread.start()
		print("Asyncio event loop started")

	def _stop_event_loop(self):
		"""Stops the asyncio event loop and joins the thread."""
		if self.loop and self.loop.is_running():
			self.loop.call_soon_threadsafe(self.loop.stop)
			self.loop_thread.join()
			print("Asyncio event loop stopped")

	async def __aenter__(self):
		"""Async context manager entry: automatically starts the loop and connects."""
		if not self.last_connected_device:
			raise ValueError("Device not specified. Set `connected_device` before entering context.")
		self._start_event_loop()
		await self._connect(self.last_connected_device)
		return self

	async def __aexit__(self, exc_type, exc, tb):
		"""Async context manager exit: disconnects and stops the loop."""
		await self._disconnect()
		self._stop_event_loop()

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking connect method."""
		if not self.loop:
			self._start_event_loop()
		self.last_connected_device = device
		asyncio.run_coroutine_threadsafe(self._connect(device, callback), self.loop)

	async def _connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Async method to establish a connection to a BLE device."""
		if self.is_connected:
			await self._disconnect()
		self.last_connected_device = device
		self.bleak_client = BleakClient(device.id)

		try:
			await self.bleak_client.connect()
			if self.bleak_client.is_connected:
				self.is_connected = True
				print(f"Connected to {device.id} (Named {device.name})")
				if callback:
					callback(device, None)  # Pass success to callback
			else:
				raise BleakError("Failed to connect to device")
		except BleakError as e:
			print(f"An error occurred: {e}")
			if callback:
				callback(device, e)  # Pass failure to callback
			await self._disconnect()

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking disconnect method."""
		asyncio.run_coroutine_threadsafe(self._disconnect(callback), self.loop)

	async def _disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Async method to disconnect from the BLE device."""
		if self.bleak_client and self.is_connected:
			try:
				await self.bleak_client.disconnect()
				self.is_connected = False
				print(
					f"Disconnected from device {self.last_connected_device.id} (Named {self.last_connected_device.name})")
				if callback:
					callback(self.last_connected_device, None)  # Pass success to callback
			except BleakError as e:
				print(f"An error occurred: {e}")
				if callback:
					callback(self.last_connected_device, e)

	def read_data(self, characteristic_uuid: str, callback: Callable[[Any, Any], None] = None):
		"""Non-blocking read data method."""
		asyncio.run_coroutine_threadsafe(self._read_data(characteristic_uuid, callback), self.loop)

	async def _read_data(self, characteristic_uuid: str, callback: Callable[[Any, Any], None] = None):
		"""Async method to read data and pass it to the callback."""
		if not self.is_connected:
			print("Device is not connected")
			return
		try:
			services = await self.bleak_client.get_services()
			# Get service with UUID "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
			for service in services:
				if service.uuid == "A07498CA-AD5B-474E-940D-16F1FBE7E8CD".lower():
					for characteristic in service.characteristics:
						if characteristic.uuid == characteristic_uuid:
							print(f"Attempting to read from {characteristic.uuid}...")
							await self.bleak_client.start_notify(characteristic, notification_handler)
							data = await self.bleak_client.read_gatt_char(characteristic.uuid)
							print(f"Data read from device: {data}")
							if callback:
								callback(data, None)
							return
		except BleakError as e:
			print(f"Failed to read data: {e}")
			if callback:
				callback(None, e)
			return
		if callback:
			callback(None, None)
	def write_data(self, characteristic_uuid: str, data: bytes, callback=None):
		"""Non-blocking write data method."""
		asyncio.run_coroutine_threadsafe(self._write_data(characteristic_uuid, data, callback), self.loop)

	async def _write_data(self, characteristic_uuid: str, data: bytes, callback=None):
		"""Async method to write data to a BLE device."""
		if not self.is_connected:
			print("Device is not connected")
			return
		try:
			await self.bleak_client.write_gatt_char(characteristic_uuid, data)
			print(f"Data {data} written to device")
			if callback:
				callback(True)  # Pass success to callback
		except BleakError as e:
			print(f"Failed to write data: {e}")
			if callback:
				callback(False)  # Pass failure to callback

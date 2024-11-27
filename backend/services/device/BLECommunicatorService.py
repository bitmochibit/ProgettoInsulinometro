from backend import DeviceService

import asyncio

from typing import Callable, Any, Optional

from bleak import BleakClient

from backend.BackendProvider import BackendProvider
from backend.config.ConfigValue import BLEMapping
from backend.config.Configuration import Configuration
from backend.device.info.DeviceInfo import DeviceInfo
from backend.device.DeviceProperty import DeviceProperty
from backend.services.device.scanner.BLEScanner import BLEScanner

config = Configuration()

PROPERTY_MAPPING = {
	DeviceProperty.NAME: "00002a00-0000-1000-8000-00805f9b34fb",  # Standard BLE name characteristic

	DeviceProperty.FREQUENCY: config.read_ble_mapping(BLEMapping.FREQUENCY_BLE_UUID),
	DeviceProperty.PHASE: config.read_ble_mapping(BLEMapping.PHASE_BLE_UUID),
	DeviceProperty.MODULE: config.read_ble_mapping(BLEMapping.MODULE_BLE_UUID),
	"DEVICE_BASE_SERVICE": config.read_ble_mapping(BLEMapping.DEVICE_BASE_SERVICE_UUID)
}


class BLECommunicatorService(DeviceService):
	def __init__(self):
		self._last_connected_device: Optional[DeviceInfo] = None
		self._is_connected = False
		self.bleak_client: Optional[BleakClient]
		self.scanner = BLEScanner()
		self.loop = BackendProvider.get_event_loop()

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking connect method."""
		BackendProvider.run_async(self._connect(device), callback)

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking disconnect method."""
		BackendProvider.run_async(self._disconnect(), callback)

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None):
		"""Non-blocking read data method."""
		BackendProvider.run_async(self._read_data(device_property), callback)

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		"""Non-blocking write data method."""
		BackendProvider.run_async(self._write_data(device_property, data), callback)

	def is_connected(self) -> bool:
		"""Returns the connection status of the device."""
		return self._is_connected
		pass

	def last_connected_device(self) -> DeviceInfo:
		"""Returns the last connected device."""
		return self._last_connected_device
		pass

	# Internal handling methods

	async def _read_data(self, device_property: DeviceProperty):
		"""Async method to read data and pass it to the callback."""
		if not self._is_connected:
			print("Device is not connected")
			return
		services = self.bleak_client.services

		for service in services:
			if service.uuid == PROPERTY_MAPPING["DEVICE_BASE_SERVICE"]:
				print("List of characteristics", service.characteristics)
				for characteristic in service.characteristics:
					if characteristic.uuid != PROPERTY_MAPPING[device_property]:
						continue
					print(f"Attempting to read from {characteristic.uuid}, handle: {characteristic.handle} ")
					data = await self.bleak_client.read_gatt_char(characteristic.handle)
					print(f"Data read from device: {data}")
					return data

	async def _write_data(self, device_property: DeviceProperty, data: Any):
		"""Async method to write data to a BLE device."""
		if not self._is_connected:
			print("Device is not connected")
			return

		await self.bleak_client.write_gatt_char(PROPERTY_MAPPING[device_property], data)
		print(f"Data {data} written to device")

	async def _disconnect(self):
		"""Async method to disconnect from the BLE device."""
		if self.bleak_client and self._is_connected:
			await self.bleak_client.disconnect()
			self._is_connected = False
			print(
				f"Disconnected from device {self._last_connected_device.id} (Named {self._last_connected_device.name})")
			return self._last_connected_device

	async def _connect(self, device: DeviceInfo):
		"""Async method to establish a connection to a BLE device."""
		if self._is_connected:
			await self._disconnect()
		self._last_connected_device = device
		self.bleak_client = BleakClient(device.id)

		await self.bleak_client.connect()
		if self.bleak_client.is_connected:
			self._is_connected = True
			self._last_connected_device = device
			print(f"Connected to {device.id} (Named {device.name})")
			return device
		else:
			await self._disconnect()

	async def __aenter__(self):
		"""Async context manager entry: automatically starts the loop and connects."""
		if not self._last_connected_device:
			raise ValueError("Device not specified. Set `connected_device` before entering context.")
		await self._connect(self._last_connected_device)
		return self

	async def __aexit__(self, exc_type, exc, tb):
		"""Async context manager exit: disconnects and stops the loop."""
		await self._disconnect()

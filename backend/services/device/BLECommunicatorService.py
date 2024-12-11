from backend import DeviceService

import asyncio

from typing import Callable, Any, Optional

from bleak import BleakClient

from backend.AppState import AppState
from backend.Scheduler import Scheduler
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
	"DEVICE_BASE_SERVICE": config.read_ble_mapping(BLEMapping.DEVICE_BASE_SERVICE_UUID),
	DeviceProperty.COMMAND: config.read_ble_mapping(BLEMapping.COMMAND_CHARACTERISTIC_UUID)
}


class BLECommunicatorService(DeviceService):
	def __init__(self):
		self.bleak_client: Optional[BleakClient] = None
		self.app_state = AppState()

	@property
	def _is_connected(self):
		if not self.bleak_client:
			return False
		return self.bleak_client.is_connected

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking connect method."""
		Scheduler().run_async(self.connect_async(device), callback)

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		"""Non-blocking disconnect method."""
		Scheduler().run_async(self.disconnect_async(), callback)

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None):
		"""Non-blocking read data method."""
		Scheduler().run_async(self.read_data_async(device_property), callback)

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		"""Non-blocking write data method."""
		Scheduler().run_async(self.write_data_async(device_property, data), callback)

	def is_connected(self) -> bool:
		"""Returns the connection status of the device."""
		return self._is_connected
		pass

	# Internal handling methods

	async def read_data_async(self, device_property: DeviceProperty):
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

	async def write_data_async(self, device_property: DeviceProperty, data: Any):
		"""Async method to write data to a BLE device."""
		if not self._is_connected:
			print("Device is not connected")
			return

		# print every device characteristic

		print(f"Writing data {data} to device {device_property}")
		await self.bleak_client.write_gatt_char(PROPERTY_MAPPING[device_property], data)
		print(f"Data {data} written to device")

	async def disconnect_async(self):
		"""Async method to disconnect from the BLE device."""
		if self.bleak_client and self._is_connected:
			await self.bleak_client.disconnect()
			self.app_state.clear_connected_device()
			last_device = self.app_state.last_connected_device
			print(
				f"Disconnected from device {last_device.id} (Named {last_device.name})")
			return last_device
		else:
			raise Exception("No device connected")

	async def connect_async(self, device: DeviceInfo):
		"""Async method to establish a connection to a BLE device."""
		if self._is_connected:
			raise Exception(f"Already connected to a device, ${self.app_state.last_connected_device.id}")

		self.bleak_client = BleakClient(device.id)

		await self.bleak_client.connect()
		if self._is_connected:
			print(f"Connected to {device.id} (Named {device.name})")
			self.app_state.set_connected_device(device)
			return device
		else:
			return None

	async def __aexit__(self, exc_type, exc, tb):
		"""Async context manager exit: disconnects and stops the loop."""
		await self.disconnect_async()

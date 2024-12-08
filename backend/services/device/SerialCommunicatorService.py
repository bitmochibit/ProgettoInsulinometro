import asyncio
from typing import Callable, Any, Optional

import serial
from serial import Serial

from backend import DeviceService
from backend.AppState import AppState
from backend.Scheduler import Scheduler
from backend.device.DeviceProperty import DeviceProperty
from backend.device.info import DeviceInfo
from backend.device.info.SerialDeviceInfo import SerialDeviceInfo


class SerialCommunicatorService(DeviceService):
	def __init__(self):
		self.app_state = AppState()
		self._is_connected = False
		self._serial_device: Optional[Serial] = None
		pass

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		Scheduler().run_async(self.disconnect_async(), callback)
		pass

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		Scheduler().run_async(self.write_data_async(device_property, data), callback)
		pass

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None) -> Any:
		Scheduler().run_async(self.read_data_async(device_property), callback)
		pass

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		Scheduler().run_async(self.connect_async(device), callback)

		pass

	async def connect_async(self, device: DeviceInfo):
		self._serial_device = Serial(port=device.name, baudrate=115200, timeout = 1)
		# self._serial_device.setDTR(False)
		# self._serial_device.setRTS(False)

		if self._serial_device.is_open:
			self._is_connected = True
			self.app_state.set_connected_device(device)
			return device
		pass

	async def write_data_async(self, device_property: DeviceProperty, data: Any):
		#TODO: Handle DeviceProperty, since the demo for the serial connection is very simple

		self._serial_device.write(data)
		await asyncio.sleep(0.1)

		pass

	async def read_data_async(self, device_property: DeviceProperty):
		try:
			data = self._serial_device.readline()
			return data
		except serial.SerialTimeoutException:
			print("Read timeout occurred")
			return None

	async def disconnect_async(self):
		self._serial_device.close()
		self._is_connected = False
		self.app_state.clear_connected_device()
		return self.app_state.last_connected_device
		pass

	def is_connected(self) -> bool:
		return self._is_connected
		pass

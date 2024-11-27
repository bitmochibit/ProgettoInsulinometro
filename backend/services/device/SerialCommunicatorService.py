from typing import Callable, Any, Optional

from serial import Serial

from backend import DeviceService
from backend.BackendProvider import BackendProvider
from backend.device.DeviceProperty import DeviceProperty
from backend.device.info import DeviceInfo
from backend.device.info.SerialDeviceInfo import SerialDeviceInfo


class SerialCommunicatorService(DeviceService):
	def __init__(self):
		self._last_connected_device: Optional[SerialDeviceInfo] = None
		self._is_connected = False
		self._serial_device: Optional[Serial] = None
		pass

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		BackendProvider.run_async(self._async_disconnect(), callback)
		pass

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		BackendProvider.run_async(self._async_write(device_property, data), callback)
		pass

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None) -> Any:
		BackendProvider.run_async(self._async_read(device_property), callback)
		pass

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		BackendProvider.run_async(self._async_connect(device), callback)
		pass

	async def _async_connect(self, device: DeviceInfo):
		self._serial_device = Serial(port=device.name, baudrate=115200, timeout = 1)
		self._serial_device.setDTR(False)
		self._serial_device.setRTS(False)

		if self._serial_device.is_open:
			self._is_connected = True
			self._last_connected_device = device
			return device
		pass

	async def _async_write(self, device_property: DeviceProperty, data: Any):
		# Write data to the serial device
		if data is not bytearray:
			print("Data is not a bytearray, are you sure about that? *boom vine*")

		#TODO: Handle DeviceProperty, since the demo for the serial connection is very simple

		self._serial_device.write(data)
		pass

	async def _async_read(self, device_property: DeviceProperty):
		# TODO: Handle DeviceProperty, since the demo for the serial connection is very simple

		# Read data from the serial device
		data = self._serial_device.read()
		return data
		pass

	async def _async_disconnect(self):
		self._serial_device.close()
		self._is_connected = False
		return self._last_connected_device
		pass

	def last_connected_device(self) -> DeviceInfo:
		return self._last_connected_device
		pass

	def is_connected(self) -> bool:
		return self._is_connected
		pass

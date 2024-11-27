from typing import Callable, Any

from backend import DeviceService
from backend.device.DeviceProperty import DeviceProperty
from backend.device.info import DeviceInfo

class SerialCommunicatorService(DeviceService):
	""" Serial connection client class """

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		pass

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		pass

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None) -> Any:
		pass

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		pass

	def last_connected_device(self) -> DeviceInfo:
		pass

	def is_connected(self) -> bool:
		pass

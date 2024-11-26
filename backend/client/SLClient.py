from typing import Callable, Any

from backend import Client
from backend.device.DeviceProperty import DeviceProperty
from backend.device.info import DeviceInfo

class SLClient(Client):
	""" Serial connection client class """

	def disconnect(self, callback: Callable[[DeviceInfo, Any], None] = None):
		pass

	def write_data(self, device_property: DeviceProperty, data: Any, callback: Callable[[Any, Any], None] = None):
		pass

	def read_data(self, device_property: DeviceProperty, callback: Callable[[Any, Any], None] = None) -> Any:
		pass

	def connect(self, device: DeviceInfo, callback: Callable[[DeviceInfo, Any], None] = None):
		pass
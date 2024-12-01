from dependency_injector.providers import Selector

from backend import DeviceService
from backend.AppState import AppState
from backend.device.DeviceProperty import DeviceProperty
from backend.device.info.DeviceInfo import DeviceInfo


class DeviceController:
	def __init__(self, service_map: dict):
		self.device_map = service_map
		self.app_state = AppState()

	def _get_service(self, device_info: DeviceInfo) -> DeviceService:
		service = self.device_map[type(device_info)]
		if service is None:
			raise Exception("No service found for device info type: " + str(type(device_info)))
		return service

	def connect(self, device: DeviceInfo, callback):
		self._get_service(device).connect(device, callback)
		pass

	def disconnect(self, device: DeviceInfo, callback):
		self._get_service(device).disconnect(callback)
		pass

	def read_data(self, device: DeviceInfo, device_property: DeviceProperty, callback):
		self._get_service(device).read_data(device_property, callback)
		pass

	def write_data(self, device: DeviceInfo, device_property: DeviceProperty, data, callback):
		self._get_service(device).write_data(device_property, data, callback)

	def is_connected(self) -> bool:
		if self.app_state.connected_device is None:
			return False

		return self._get_service(self.app_state.connected_device).is_connected()

	def last_connected_device(self) -> DeviceInfo:
		return self.app_state.last_connected_device
	pass
from backend import DeviceService
from backend.device.info.DeviceInfo import DeviceInfo


class DeviceController:
	def __init__(self, device_service: DeviceService):
		self.deviceService = device_service

	def connect(self, device, callback):
		self.deviceService.connect(device, callback)
		pass

	def disconnect(self, callback):
		self.deviceService.disconnect(callback)
		pass

	def read_data(self, device_property, callback):
		self.deviceService.read_data(device_property, callback)
		pass

	def write_data(self, device_property, data, callback):
		self.deviceService.write_data(device_property, data, callback)

	def is_connected(self) -> bool:
		return self.deviceService.is_connected()

	def last_connected_device(self) -> DeviceInfo:
		return self.deviceService.last_connected_device()
	pass
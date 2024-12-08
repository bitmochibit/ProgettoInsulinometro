from typing import Optional

from backend.decorator.Singleton import singleton
from backend.device.info.DeviceInfo import DeviceInfo


@singleton
class AppState(object):
	"""Class to store the state of the app, such as the current connected device"""

	def __init__(self):
		self._connected_device: Optional[DeviceInfo] = None
		self._last_connected_device: Optional[DeviceInfo] = None

	def set_connected_device(self, device: DeviceInfo):
		if self._connected_device is not None:
			self._last_connected_device = self._connected_device

		self._connected_device = device

	def clear_connected_device(self):
		self._last_connected_device = self._connected_device
		self._connected_device = None

	@property
	def connected_device(self) -> Optional[DeviceInfo]:
		return self._connected_device

	@property
	def last_connected_device(self) -> Optional[DeviceInfo]:
		return self._last_connected_device

import asyncio
from typing import Dict

from bleak import BLEDevice, AdvertisementData, BleakScanner

from backend.EventLoopProvider import EventLoopProvider
from backend.device.info.BLEDeviceInfo import BLEDeviceInfo
from backend.services.device.scanner.AbstractScanner import AbstractScanner


class BLEScanner(AbstractScanner):
	def get_devices(self) -> Dict[str, BLEDeviceInfo]:
		return self.device_dict
		pass

	def __init__(self):
		self.device_dict: Dict[str, BLEDeviceInfo] = {}
		self.scanning = False
		self.loop = EventLoopProvider.get_event_loop()
		self.scan_time = 0
		self.scan_interval = 0.1

	async def on_discover(self, device: BLEDevice, advertisement_data: AdvertisementData):
		# If the same device with the same id exists in the dictionary, update it, otherwise create one
		if device.address in self.device_dict.keys():
			self.device_dict[device.address].update(device, advertisement_data)
		else:
			self.device_dict[device.address] = BLEDeviceInfo.from_device(device, advertisement_data)

	def start_scan(self, max_time):
		self.scanning = True
		asyncio.run_coroutine_threadsafe(self.run_scan(max_time), self.loop)

	def stop_scan(self):
		self.scanning = False

	async def run_scan(self, max_time):
		self.device_dict.clear()
		self.scan_time = 0
		async with BleakScanner(self.on_discover) as scanner:
			print("Starting BLE scan...")
			while self.scanning:
				if self.scan_time > max_time:
					await scanner.stop()
					self.scanning = False

				await asyncio.sleep(self.scan_interval)  # Keep scanning until stopped
				self.scan_time += self.scan_interval

		print("Stopping BLE scan...")

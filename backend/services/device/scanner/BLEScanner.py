import asyncio
from typing import Dict

from bleak import BLEDevice, AdvertisementData, BleakScanner

from backend.Scheduler import Scheduler
from backend.device.info.BLEDeviceInfo import BLEDeviceInfo
from backend.services.device.scanner.AbstractScanner import AbstractScanner


class BLEScanner(AbstractScanner):
	def get_devices(self) -> Dict[str, BLEDeviceInfo]:
		return self.device_dict
		pass

	def __init__(self):
		self.device_dict: Dict[str, BLEDeviceInfo] = {}
		self.scanning = False
		self.scan_time = 0
		self.scan_interval = 0.1

	async def on_discover(self, device: BLEDevice, advertisement_data: AdvertisementData):
		# If the same device with the same id exists in the dictionary, update it, otherwise create one
		if device.address in self.device_dict.keys():
			self.device_dict[device.address].update(device, advertisement_data)
		else:
			self.device_dict[device.address] = BLEDeviceInfo.from_device(device, advertisement_data)

	def start_scan(self):
		self.scanning = True
		Scheduler().run_async(self.run_scan(), None, None)

	def stop_scan(self):
		self.scanning = False

	async def run_scan(self):
		self.device_dict.clear()
		self.scan_time = 0
		async with BleakScanner(self.on_discover) as scanner:
			print("Starting BLE scan...")
			while self.scanning:
				await asyncio.sleep(self.scan_interval)

		print("Stopping BLE scan...")

import queue

from bleak import BleakScanner, BLEDevice, AdvertisementData
import asyncio


class Client:
	def __init__(self):
		self.device_queue: queue.Queue[BLEDevice] = queue.Queue()
		self.scanning = False

	async def on_discover(self, device: BLEDevice, advertisement_data: AdvertisementData):
		# Place discovered device in the queue for the Tkinter thread to access
		self.device_queue.put(device)

	async def start_scan(self):
		self.scanning = True
		async with BleakScanner(self.on_discover) as scanner:
			print("Starting BLE scan...")
			while self.scanning:
				await asyncio.sleep(0.1)  # Keep scanning until stopped
		print("Stopping BLE scan...")

	def stop_scan(self):
		self.scanning = False

	def run_scan(self):
		try:
			asyncio.run(self.start_scan())
		except KeyboardInterrupt:
			self.stop_scan()
			print("Scan stopped")
		except Exception as e:
			print(f"Error: {e}")

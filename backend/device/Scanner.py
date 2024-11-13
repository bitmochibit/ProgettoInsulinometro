import asyncio
from queue import Queue

from bleak import BLEDevice, AdvertisementData, BleakScanner

from backend.device.DeviceInfo import DeviceInfo


class Scanner:
    def __init__(self):
        self.device_queue: Queue[DeviceInfo] = Queue()
        self.scanning = False

    async def on_discover(self, device: BLEDevice, advertisement_data: AdvertisementData):
        # Place discovered device in the queue for the Tkinter thread to access
        self.device_queue.put(
            DeviceInfo(
                id = device.address,
                name = device.name,
                details = device.details
            )
        )

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
        self.device_queue.queue.clear()
        try:
            asyncio.run(self.start_scan())
        except KeyboardInterrupt:
            self.stop_scan()
            print("Scan stopped")
        except Exception as e:
            print(f"Error: {e}")

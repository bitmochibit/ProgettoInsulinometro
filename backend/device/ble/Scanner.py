import asyncio
from datetime import datetime
from queue import Queue

from bleak import BLEDevice, AdvertisementData, BleakScanner

from backend.device.info.BLEDeviceInfo import BLEDeviceInfo


class Scanner:
    def __init__(self):
        self.device_list: list[BLEDeviceInfo] = list()
        self.scanning = False

    async def on_discover(self, device: BLEDevice, advertisement_data: AdvertisementData):
        # Place discovered device in the queue for the Tkinter thread to access

        # If the device is already in the queue, update the device info
        for d in self.device_list:
            if d.id == device.address:
                d.name = device.name
                d.local_name = advertisement_data.local_name
                d.rssi = advertisement_data.rssi
                d.service_uuids = advertisement_data.service_uuids
                d.tx_power = advertisement_data.tx_power
                d.update_time = datetime.now()
                return

        # If the device is not in the queue, add it
        self.device_list.append(BLEDeviceInfo(
            id=device.address,
            name=device.name,
            local_name=advertisement_data.local_name,
            rssi=advertisement_data.rssi,
            service_uuids=advertisement_data.service_uuids,
            tx_power=advertisement_data.tx_power,
            update_time=datetime.now()
        ))

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
        self.device_list.clear()
        try:
            asyncio.run(self.start_scan())
        except KeyboardInterrupt:
            self.stop_scan()
            print("Scan stopped")
        except Exception as e:
            print(f"Error: {e}")

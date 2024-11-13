import asyncio
import threading

from bleak import BleakClient, BleakError

from backend.device.DeviceInfo import DeviceInfo
from backend.device.Scanner import Scanner


class Client:
    def __init__(self):
        self.connected_device = None
        self.bleak_client = None
        self.scanner = Scanner()
        self.is_connected = False
        self.loop = None
        self.loop_thread = None

    def _start_event_loop(self):
        """Starts the asyncio event loop in a background thread."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop_thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.loop_thread.start()
        print("Asyncio event loop started")

    def _stop_event_loop(self):
        """Stops the asyncio event loop and joins the thread."""
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.loop_thread.join()
            print("Asyncio event loop stopped")

    async def __aenter__(self):
        """Async context manager entry: automatically starts the loop and connects."""
        if not self.connected_device:
            raise ValueError("Device not specified. Set `connected_device` before entering context.")
        self._start_event_loop()
        await self._connect(self.connected_device)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Async context manager exit: disconnects and stops the loop."""
        await self._disconnect()
        self._stop_event_loop()

    def connect(self, device: DeviceInfo, callback=None):
        """Non-blocking connect method."""
        if not self.loop:
            self._start_event_loop()
        self.connected_device = device
        asyncio.run_coroutine_threadsafe(self._connect(device, callback), self.loop)

    async def _connect(self, device: DeviceInfo, callback=None):
        """Async method to establish a connection to a BLE device."""
        self.connected_device = device
        self.bleak_client = BleakClient(device.id)

        try:
            await self.bleak_client.connect()
            if self.bleak_client.is_connected:
                self.is_connected = True
                print(f"Connected to {device.name}")
                if callback:
                    callback(True)  # Pass success to callback
            else:
                raise BleakError("Failed to connect to device")
        except BleakError as e:
            print(f"An error occurred: {e}")
            if callback:
                callback(False)  # Pass failure to callback
            await self._disconnect()

    def disconnect(self, callback=None):
        """Non-blocking disconnect method."""
        future = asyncio.run_coroutine_threadsafe(self._disconnect(callback), self.loop)
        future.add_done_callback(lambda f: self._stop_event_loop())

    async def _disconnect(self, callback=None):
        """Async method to disconnect from the BLE device."""
        if self.bleak_client and self.is_connected:
            await self.bleak_client.disconnect()
            self.is_connected = False
            print("Disconnected from device")
            if callback:
                callback(True)  # Pass success to callback

    def read_data(self, characteristic_uuid: str, callback):
        """Non-blocking read data method."""
        asyncio.run_coroutine_threadsafe(self._read_data(characteristic_uuid, callback), self.loop)

    async def _read_data(self, characteristic_uuid: str, callback):
        """Async method to read data and pass it to the callback."""
        if not self.is_connected:
            print("Device is not connected")
            return
        try:
            data = await self.bleak_client.read_gatt_char(characteristic_uuid)
            print(f"Data read from device: {data}")
            if callback:
                callback(data)
        except BleakError as e:
            print(f"Failed to read data: {e}")

    def write_data(self, characteristic_uuid: str, data: bytes, callback=None):
        """Non-blocking write data method."""
        asyncio.run_coroutine_threadsafe(self._write_data(characteristic_uuid, data, callback), self.loop)

    async def _write_data(self, characteristic_uuid: str, data: bytes, callback=None):
        """Async method to write data to a BLE device."""
        if not self.is_connected:
            print("Device is not connected")
            return
        try:
            await self.bleak_client.write_gatt_char(characteristic_uuid, data)
            print(f"Data {data} written to device")
            if callback:
                callback(True)  # Pass success to callback
        except BleakError as e:
            print(f"Failed to write data: {e}")
            if callback:
                callback(False)  # Pass failure to callback

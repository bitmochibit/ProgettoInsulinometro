import sys
import logging
import asyncio
import threading
import random

from typing import Any, Union, cast

from bleak import normalize_uuid_str
from bless import (  # type: ignore
	BlessServer,
	BlessGATTCharacteristic,
	GATTCharacteristicProperties,
	GATTAttributePermissions,
)
from bless.backends.descriptor import BlessGATTDescriptor
from bless.backends.winrt.characteristic import BlessGATTCharacteristicWinRT
from bless.backends.winrt.service import BlessGATTServiceWinRT

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# NOTE: Some systems require different synchronization methods.
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
	trigger = threading.Event()
else:
	trigger = asyncio.Event()

# Globals for the dynamic data
read_x = 0
read_y = 0


def update_random_values():
	"""Simulates reading x and y values by generating random numbers."""
	global read_x, read_y
	read_x = random.randint(0, 100)  # Replace with actual sensor reading if available
	read_y = random.randint(0, 100)
	logger.debug(f"Updated values: read_x={read_x}, read_y={read_y}")


def read_request(characteristic: BlessGATTCharacteristic, options: dict = None, **kwargs) -> bytearray:
	"""Handles read requests by returning the current x and y values."""
	global read_x, read_y
	response = f"{read_x},{read_y}"
	logger.debug(f"Read request: returning {response}")
	return bytearray(response, 'utf-8')


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
	"""Handles write requests."""
	characteristic.value = value
	logger.debug(f"Char value set to {characteristic.value}")
	if characteristic.value == b"\x0f":
		logger.debug("NICE")
		trigger.set()


class WindowsGATTServer(BlessServer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# Implement abstract method add_new_descriptor to avoid error
	async def add_new_descriptor(self, service_uuid: str, characteristic_uuid: str, descriptor_uuid: str,
	                       descriptor_flags: int, value: Any, permissions: int):
		print("Supported only on BlueZ backend") # This method is not supported on Windows backend
		pass


def get_characteristic_uuid_from_code(code: int) -> str:
	# All BLE characteristics have a 16-bit UUID
	# In the form of 0000XXXX-0000-1000-8000-00805f9b34fb

	# Convert the code to a 4-digit hex string
	hex_code = format(code, "04x")
	return f"0000{hex_code}-0000-1000-8000-00805f9b34fb"


# Bluetooth accepted numbers https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Assigned_Numbers/out/en/Assigned_Numbers.pdf?v=1732012898562

async def run(loop):
	trigger.clear()

	# Instantiate the server
	server_name = "Insulinometro"
	server = WindowsGATTServer(name=server_name, loop=loop)
	server.read_request_func = read_request
	server.write_request_func = write_request

	# Add Service
	service_uuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
	await server.add_new_service(service_uuid)

	# Device Name Characteristic
	device_name_uuid = get_characteristic_uuid_from_code(0x2A00)  # Standard GAP Device Name UUID
	char_flags = GATTCharacteristicProperties.read
	permissions = GATTAttributePermissions.readable
	await server.add_new_characteristic(
		service_uuid, device_name_uuid, char_flags, bytearray(server_name, 'utf-8'), permissions
	)

	# Read X,Y Characteristic
	char_uuid = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B".lower()
	char_flags = (
			GATTCharacteristicProperties.read
			| GATTCharacteristicProperties.write
			| GATTCharacteristicProperties.indicate
	)
	# Set permissions to allow unrestricted access
	permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable
	await server.add_new_characteristic(
		service_uuid, char_uuid, char_flags, None, permissions
	)

	logger.debug(server.get_characteristic(char_uuid))
	await server.start()
	logger.debug("Advertising")
	logger.info(f"Read characteristic to get x and y values: {char_uuid}")

	# Periodically update x and y values
	async def update_values_periodically():
		while True:
			update_random_values()
			await asyncio.sleep(5)  # Update every 5 seconds

	# Start the periodic update task
	await asyncio.create_task(update_values_periodically())

	if trigger.__module__ == "threading":
		await trigger.wait()
	else:
		await trigger.wait()

	await asyncio.sleep(2)
	await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))

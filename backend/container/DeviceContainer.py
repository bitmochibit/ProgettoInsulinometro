from dependency_injector import containers, providers

from backend.controller.device.BLEScannerController import BLEScannerController
from backend.services.device.BLECommunicatorService import BLECommunicatorService
from backend.services.device.SerialCommunicatorService import SerialCommunicatorService
from backend.controller.device.DeviceController import DeviceController
from backend.services.device.scanner.BLEScanner import BLEScanner


class DeviceContainer(containers.DeclarativeContainer):

	# Connection service managers
	ble_service = providers.Singleton(BLECommunicatorService)
	serial_service = providers.Singleton(SerialCommunicatorService)

	ble_device_controller = providers.Factory(DeviceController, device_service=ble_service)
	serial_device_controller = providers.Factory(DeviceController, device_service=serial_service)

	# Device scanner service managers
	ble_scanner_service = providers.Factory(BLEScanner)
	ble_scanner_controller = providers.Factory(BLEScannerController, scanner_service=ble_scanner_service)
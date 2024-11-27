from dependency_injector import containers, providers

from backend.controller.device.BLEScannerController import BLEScannerController
from backend.controller.device.SerialScannerController import SerialScannerController
from backend.services.device.BLECommunicatorService import BLECommunicatorService
from backend.services.device.SerialCommunicatorService import SerialCommunicatorService
from backend.controller.device.DeviceController import DeviceController
from backend.services.device.scanner.BLEScanner import BLEScanner
from backend.services.device.scanner.SerialScanner import SerialScanner


class DeviceContainer(containers.DeclarativeContainer):

	# Device controllers and services
	ble_service = providers.Singleton(BLECommunicatorService)
	serial_service = providers.Singleton(SerialCommunicatorService)

	ble_device_controller = providers.Factory(DeviceController, device_service=ble_service)
	serial_device_controller = providers.Factory(DeviceController, device_service=serial_service)

	# BLE Scanner service and controller
	ble_scanner_service = providers.Factory(BLEScanner)
	ble_scanner_controller = providers.Factory(BLEScannerController, scanner_service=ble_scanner_service)

	# Serial Scanner service and controller
	serial_scanner_service = providers.Factory(SerialScanner)
	serial_scanner_controller = providers.Factory(SerialScannerController, scanner_service=serial_scanner_service)
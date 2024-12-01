from dependency_injector import containers, providers

from backend.controller.device.ScannerController import ScannerController
from backend.device.info.BLEDeviceInfo import BLEDeviceInfo
from backend.device.info.SerialDeviceInfo import SerialDeviceInfo
from backend.services.device.BLECommunicatorService import BLECommunicatorService
from backend.services.device.SerialCommunicatorService import SerialCommunicatorService
from backend.controller.device.DeviceController import DeviceController
from backend.services.device.scanner.BLEScanner import BLEScanner
from backend.services.device.scanner.SerialScanner import SerialScanner


class DeviceContainer(containers.DeclarativeContainer):

	# Device controllers and services
	device_services = providers.Dict({
		BLEDeviceInfo: providers.Singleton(BLECommunicatorService),
		SerialDeviceInfo: providers.Singleton(SerialCommunicatorService)
	})

	device_controller = providers.Factory(DeviceController, service_map=device_services)

	# BLE Scanner service and controller
	ble_scanner_service = providers.Factory(BLEScanner)
	ble_scanner_controller = providers.Factory(ScannerController, scanner_service=ble_scanner_service)

	# Serial Scanner service and controller
	serial_scanner_service = providers.Factory(SerialScanner)
	serial_scanner_controller = providers.Factory(ScannerController, scanner_service=serial_scanner_service)
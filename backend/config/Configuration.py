import os
import yaml

from backend.config.ConfigValue import BLEMapping
from backend.utils.BLEAddressFormatter import from_hex


class Configuration:
	_instance = None
	config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(Configuration, cls).__new__(cls)
		return cls._instance

	def __init__(self):
		# Check if configuration default YAML file exists, if not create it
		if not os.path.exists(self.config_file_path):
			self.create_default_config()


	def create_default_config(self):
		# Create a default configuration file
		config_map = {
			"BLE_MAPPINGS": {
				"DEVICE_BASE_SERVICE_UUID": from_hex(0x1809),
				"FREQUENCY_BLE_UUID": from_hex(0x2A1C),
				"VOLTAGE_BLE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
				"CURRENT_BLE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
				"COMMAND_CHARACTERISTIC_UUID": from_hex(0x2A56)
			}
		}
		with open(self.config_file_path, 'w') as file:
			file.write(yaml.dump(config_map, default_flow_style=False))

	def read_ble_mapping(self, key: BLEMapping):
		with open(self.config_file_path, 'r') as file:
			config = yaml.safe_load(file)
			return config["BLE_MAPPINGS"][key]
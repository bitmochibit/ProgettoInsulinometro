import os
import yaml

from backend.config.ConfigValue import BLEMapping
from backend.utils.Singleton import Singleton


class Configuration(metaclass=Singleton):
	config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

	def __init__(self):
		# Check if configuration default YAML file exists, if not create it
		if not os.path.exists(self.config_file_path):
			self.create_default_config()


	def create_default_config(self):
		# Create a default configuration file
		config_map = {
			"BLE_MAPPINGS": {
				"DEVICE_BASE_SERVICE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
				"FREQUENCY_BLE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
				"VOLTAGE_BLE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
				"CURRENT_BLE_UUID": "a07498ca-ad5b-474e-940d-16f1fbe7e8cd",
			}
		}
		with open(self.config_file_path, 'w') as file:
			file.write(yaml.dump(config_map, default_flow_style=False))

	def read_ble_mapping(self, key: BLEMapping):
		with open(self.config_file_path, 'r') as file:
			config = yaml.safe_load(file)
			return config["BLE_MAPPINGS"][key]
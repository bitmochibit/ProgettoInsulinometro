
""" This class is a singleton that holds the client objects """
from backend.client.BLEClient import BLEClient
from backend.client.SLClient import SLClient
from backend.utils.Singleton import Singleton


class ClientHolder(metaclass=Singleton):

	def __init__(self):
		self.ble_client = BLEClient()
		self.serial_client = SLClient()



""" This class is a singleton that holds the client objects """
from backend.client.BLEClient import BLEClient
from backend.client.SLClient import SLClient


class ClientHolder:
	ble_client = BLEClient()
	sl_client = SLClient()


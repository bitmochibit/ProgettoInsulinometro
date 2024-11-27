from typing import Dict

import customtkinter as ctk
from PIL.ImageOps import expand
from customtkinter import CTkFont, CTkFrame, CTkLabel
from eventpy.eventdispatcher import EventDispatcher

from app.events.ApplicationMessagesEnum import ApplicationMessagesEnum
from app.templates.SearchBar import SearchBar
from app.theme.AppTheme import AppTheme
from app.utils.Color import scale_lightness
from backend.container.Container import Container
from backend.controller.device import SerialScannerController
from backend.controller.device.BLEScannerController import BLEScannerController
from backend.controller.device.DeviceController import DeviceController
from backend.device.info.BLEDeviceInfo import BLEDeviceInfo
from backend.device.info.DeviceInfo import DeviceInfo
from backend.device.info.SerialDeviceInfo import SerialDeviceInfo


def format_info(device_info: DeviceInfo) -> Dict[str, str]:
	final_dict = {}
	device_name = device_info.name
	device_description = f"Indirizzo: {device_info.id} | Ultimo aggiornamento: {device_info.update_time.strftime('%H:%M:%S')}"

	if isinstance(device_info, BLEDeviceInfo):
		device_name = device_name or "Dispositivo BLE senza nome"
		device_name += f" ~ ({device_info.local_name})"
		device_description += f" | RSSI: {device_info.rssi} dBm"
	elif isinstance(device_info, SerialDeviceInfo):
		device_name = device_name or "Dispositivo seriale senza nome"
		device_description += f" | Porta: {device_info.name}"

	final_dict["name"] = device_name
	final_dict["description"] = device_description

	return final_dict


class DeviceWindow(ctk.CTkToplevel):
	def __init__(
			self,
			master: ctk.CTk,
			application_message_dispatcher: EventDispatcher,
			app_theme: AppTheme = AppTheme()):
		super().__init__(master, fg_color=app_theme.primary_background)

		self.master = master
		self.application_messanger = application_message_dispatcher
		self.app_theme = app_theme

		self.__setup()

		# This object maps an element box to the ID of the device
		self.device_map: Dict = {}

		# Coordinates for the top window to be centered (relative to master)

		self.searched_var = ctk.StringVar()

		width = 600
		height = 500

		master_x = master.winfo_x()
		master_y = master.winfo_y()
		master.update_idletasks()
		master_width = master.winfo_width()
		master_height = master.winfo_height()

		pos_x = master_x + (master_width - width) // 2
		pos_y = master_y + (master_height - height) // 2

		self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

		self.title("")

		self.__setup_window()

	def __setup(self):
		self.ble_ctr: DeviceController = Container.device_container.ble_device_controller()
		self.serial_ctr: DeviceController = Container.device_container.serial_device_controller()

		self.ble_scanner: BLEScannerController = Container.device_container.ble_scanner_controller()
		self.serial_scanner: SerialScannerController = Container.device_container.serial_scanner_controller()

		self.devices: Dict[str, DeviceInfo] = {}

	def __setup_window(self):
		container = ctk.CTkFrame(self, fg_color=self.app_theme.primary_background)
		container.pack(side="top", fill="both", padx=5, pady=5, expand=True)

		self.search_bar = SearchBar(container,
		                            fg_color=self.app_theme.element_background,
		                            placeholder_text="🔎 Find device",
		                            placeholder_text_color=self.app_theme.light_gray_text,
		                            text_color=self.app_theme.primary_text,
		                            textvariable=self.searched_var,
		                            corner_radius=5,
		                            border_width=1,
		                            border_color=self.app_theme.light_gray_text)
		self.search_bar.pack(side="top", fill="x")

		def on_type(e):
			self.__search()

		self.search_bar.bind_input("<KeyRelease>", on_type)

		super_scrollable_frame = ctk.CTkScrollableFrame(container, fg_color=self.app_theme.primary_background,
		                                                scrollbar_button_color=self.app_theme.secondary_background)
		super_scrollable_frame.pack(side="top", fill="both", expand=True)

		# Container for the connected device
		self.connected_device_container = ctk.CTkFrame(super_scrollable_frame,
		                                               fg_color=self.app_theme.primary_background)
		self.connected_device_container.pack(side="top", fill="both", expand=True)

		first_horizontal_separator = ctk.CTkFrame(super_scrollable_frame, fg_color=self.app_theme.light_gray_text,
		                                          height=5)
		first_horizontal_separator.pack(side="top", fill="x", pady=5)

		# Container for the discovered devices
		self.discovered_devices_serial = ctk.CTkScrollableFrame(super_scrollable_frame,
		                                                        fg_color=self.app_theme.primary_background)
		self.discovered_devices_serial.pack(side="top", fill="both", expand=True)

		second_horizontal_separator = ctk.CTkFrame(super_scrollable_frame, fg_color=self.app_theme.light_gray_text,
		                                           height=5)
		second_horizontal_separator.pack(side="top", fill="x", pady=5)

		# Container for the discovered BLE devices
		self.discovered_devices_ble = ctk.CTkScrollableFrame(super_scrollable_frame,
		                                                     fg_color=self.app_theme.primary_background)
		self.discovered_devices_ble.pack(side="top", fill="both", expand=True)

		self.__start_scan()

		pass

	def __search_match(self, device: BLEDeviceInfo, search_text: str) -> bool:
		"""
		Checks if a device matches the search query.
		"""
		if not search_text:  # If search text is empty, match everything
			return True

		search_text = search_text.lower()
		# Match search text against the device ID or name, both converted to lowercase
		return search_text in str(device.id).lower() or search_text in str(device.name or "").lower()

	def __search(self):
		search_query = self.searched_var.get().lower()
		matched_devices = [dev for dev in self.ble_devices.values() if self.__search_match(dev, search_query)]

		# Hide all devices
		for device_box in self.discovered_devices_ble.winfo_children():
			device_box.pack_forget()

		# Show matched devices
		for device in matched_devices:
			self.__show_device_box(device)

	def __create_device_box(self, device_info: DeviceInfo):
		if device_info.id is None:
			raise Exception("Invalid device id")

		if isinstance(device_info, BLEDeviceInfo):
			selected_controller = self.ble_ctr
		else:
			selected_controller = self.serial_ctr

		last_connected_device = selected_controller.last_connected_device()
		device_connected = last_connected_device is not None and last_connected_device.id == device_info.id and selected_controller.is_connected()

		if device_connected:
			selected_container = self.connected_device_container
		elif isinstance(device_info, SerialDeviceInfo):
			selected_container = self.discovered_devices_serial
		else:
			selected_container = self.discovered_devices_ble

		device_box = ctk.CTkFrame(selected_container, fg_color=self.app_theme.element_background,
		                          corner_radius=5)
		device_box.pack(side="top", fill="x", pady=5)

		device_info_container = ctk.CTkFrame(
			device_box,
			fg_color=self.app_theme.element_background
		)
		device_info_container.pack(side="left", fill="both", pady=2, padx=5)

		formatted_info = format_info(device_info)

		device_name_label = ctk.CTkLabel(device_info_container, text=formatted_info["name"],
		                                 text_color=self.app_theme.primary_text,
		                                 font=CTkFont(family="Poppins", size=14, weight="bold"),
		                                 anchor="w"
		                                 )
		device_name_label.pack(side="top", fill="both")

		device_description_label = ctk.CTkLabel(device_info_container, text=formatted_info["description"],
		                                        text_color=self.app_theme.secondary_text,
		                                        font=CTkFont(family="Poppins", size=12, weight="bold"),
		                                        anchor="w"
		                                        )
		device_description_label.pack(side="left", fill="both")

		button_container = ctk.CTkFrame(
			device_box,
			fg_color=self.app_theme.element_background
		)

		button_container.pack(side="right", fill="both", pady=2, padx=5)
		button_container.rowconfigure(0, weight=1)
		button_container.columnconfigure(0, weight=1)

		if device_connected:
			disconnect_device_button = ctk.CTkButton(button_container,
			                                         text="Disconnetti",
			                                         fg_color=self.app_theme.danger_button,
			                                         font=CTkFont(family="Poppins", size=14, weight="bold"),
			                                         text_color=self.app_theme.danger_button_text,
			                                         hover_color=scale_lightness(self.app_theme.danger_button, 0.95),
			                                         width=200,
			                                         corner_radius=5,
			                                         command=lambda: self.__disconnect_device(device_info)
			                                         )
			disconnect_device_button.grid(row=0, column=0)
		else:
			connect_device_button = ctk.CTkButton(button_container,
			                                      text="Connetti",
			                                      text_color=self.app_theme.primary_button_text,
			                                      fg_color=self.app_theme.primary_button,
			                                      font=CTkFont(family="Poppins", size=14, weight="bold"),
			                                      hover_color=scale_lightness(self.app_theme.primary_button, 0.95),
			                                      width=200,
			                                      corner_radius=5,
			                                      command=lambda: self.__connect_device(device_info)
			                                      )
			connect_device_button.grid(row=0, column=0)

		self.device_map[device_info.id] = {
			"device_box": device_box,
			"device_name_label": device_name_label,
			"device_description_label": device_description_label,
			"button_container": button_container,
		}
		pass

	def __update_device_box(self, device_info: DeviceInfo):
		if device_info.id not in self.device_map:
			return

		formatted_info = format_info(device_info)

		device_box: CTkFrame = self.device_map[device_info.id]["device_box"]
		device_name_label: CTkFrame = self.device_map[device_info.id]["device_name_label"]
		device_description_label: CTkLabel = self.device_map[device_info.id]["device_description_label"]
		button_container: CTkFrame = self.device_map[device_info.id]["button_container"]

		device_name_label.configure(text=formatted_info["name"])
		device_description_label.configure(text=formatted_info["description"])


	def __show_device_box(self, device_info: BLEDeviceInfo):
		self.device_map[device_info.id].pack(side="top", fill="x", pady=5)

	def __remove_device_box(self, device_info: DeviceInfo):
		if device_info.id in self.device_map:
			box = self.device_map[device_info.id]["device_box"]
			box.pack_forget()
			box.destroy()
			del self.device_map[device_info.id]

	def __hide_device_box(self, device_info: BLEDeviceInfo):
		if device_info.id in self.device_map:
			self.device_map[device_info.id].pack_forget()

	def __handle_connection(self, device_info: DeviceInfo, error=None):
		if error is not None:
			return print(f"Unable to connect to device, {error}")

		self.__remove_device_box(device_info)
		self.__create_device_box(device_info)
		self.application_messanger.dispatch(ApplicationMessagesEnum.START_VALUE_READER)

	def __handle_disconnection(self, device_info: DeviceInfo, error=None):
		if error is not None:
			return print(f"Unable to disconnect, {error}")

		self.__remove_device_box(device_info)
		self.__create_device_box(device_info)
		self.application_messanger.dispatch(ApplicationMessagesEnum.STOP_VALUE_READER)

	def __start_scan(self):
		self.ble_scanner.start_scan(60)
		self.serial_scanner.start_scan(60)

		self.__update_devices()

	def __stop_scan(self):
		self.ble_scanner.stop_scan()
		self.serial_scanner.stop_scan()

	def __connect_device(self, device_info: DeviceInfo):
		if isinstance(device_info, BLEDeviceInfo):
			self.ble_ctr.connect(device_info, self.__handle_connection)
		elif isinstance(device_info, SerialDeviceInfo):
			self.serial_ctr.connect(device_info, self.__handle_connection)

	def __disconnect_device(self, device_info: DeviceInfo):
		if isinstance(device_info, BLEDeviceInfo):
			self.ble_ctr.disconnect(self.__handle_disconnection)
		elif isinstance(device_info, SerialDeviceInfo):
			self.serial_ctr.disconnect(self.__handle_disconnection)


	def __update_devices(self):
		# Inside each of client, there's a scanner which contains the list of devices (and eventually they get updated)
		scanned_devices = {}
		for device in self.ble_scanner.get_devices().values():
			scanned_devices[device.id] = device
		for device in self.serial_scanner.get_devices().values():
			scanned_devices[device.id] = device

		for scanned_id, scanned_device in scanned_devices.items():
			# Check if the id is already in the list of devices
			# (if it is, update the device info if the current update_time is greater than the one stored), otherwise add it

			if scanned_id in self.devices:
				# Update the device if the new update_time is more recent
				if scanned_device.update_time > self.devices[scanned_id].update_time:
					self.devices[scanned_id] = scanned_device
					self.__update_device_box(scanned_device)
			else:
				# Add the new device to the devices dictionary
				self.devices[scanned_id] = scanned_device
				self.__create_device_box(scanned_device)

		# Find and remove devices that are no longer present in the scan
		for device_id, device in self.devices.items():
			if device_id not in list(scanned_devices.keys()):
				removed_device = self.devices.pop(device_id)  # Remove the device
				self.__remove_device_box(removed_device)

		self.after(1000, self.__update_devices)

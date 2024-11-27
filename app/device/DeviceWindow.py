from typing import Dict

import customtkinter as ctk
from customtkinter import CTkFont, CTkFrame
from eventpy.eventdispatcher import EventDispatcher

from app.events.ApplicationMessagesEnum import ApplicationMessagesEnum
from app.templates.SearchBar import SearchBar
from app.theme.AppTheme import AppTheme
from app.utils.Color import scale_lightness
from backend.container.Container import Container
from backend.controller.device.BLEScannerController import BLEScannerController
from backend.controller.device.DeviceController import DeviceController
from backend.device.info.BLEDeviceInfo import BLEDeviceInfo


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

		self.ble_controller: DeviceController = Container.device_container.ble_device_controller()
		self.serial_controller: DeviceController = Container.device_container.serial_device_controller()

		self.ble_scanner_controller: BLEScannerController = Container.device_container.ble_scanner_controller()

		self.devices: Dict[str, BLEDeviceInfo] = {}

		self.searched_var = ctk.StringVar()

		# This object maps an element box to the ID of the device
		self.device_map: Dict[str, CTkFrame] = {}

		# Coordinates for the top window to be centered (relative to master)
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

	def __setup_window(self):
		container = ctk.CTkFrame(self, fg_color=self.app_theme.primary_background)
		container.pack(side="top", fill="both", padx=5, pady=5, expand=True)

		# TODO inserire chiamata a funzione che crea searchbar/creare searchbar
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
		self.discovered_devices_container = ctk.CTkScrollableFrame(container,
		                                                           fg_color=self.app_theme.primary_background)
		self.discovered_devices_container.pack(side="top", fill="both", expand=True)

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
		matched_devices = [dev for dev in self.devices.values() if self.__search_match(dev, search_query)]

		# Hide all devices
		for device_box in self.discovered_devices_container.winfo_children():
			device_box.pack_forget()

		# Show matched devices
		for device in matched_devices:
			self.__show_device_box(device)

	def __create_device_box(self, device_info: BLEDeviceInfo):
		if device_info.id is None:
			raise Exception("Invalid device id")

		device_name = device_info.name or "Dispositivo senza nome"
		if device_info.local_name is not None and device_info.local_name != device_info.name:
			device_name += f" ~ ({device_info.local_name})"

		device_box = ctk.CTkFrame(self.discovered_devices_container, fg_color=self.app_theme.element_background,
		                          corner_radius=5)
		device_box.pack(side="top", fill="x", pady=5)

		device_info_container = ctk.CTkFrame(
			device_box,
			fg_color=self.app_theme.element_background
		)
		device_info_container.pack(side="left", fill="both", pady=2, padx=5)

		device_name_label = ctk.CTkLabel(device_info_container, text=device_name,
		                                 text_color=self.app_theme.primary_text,
		                                 font=CTkFont(family="Poppins", size=14, weight="bold"),
		                                 anchor="w"
		                                 )
		device_name_label.pack(side="top", fill="both")

		device_description_label = ctk.CTkLabel(device_info_container, text=f"Indirizzo: {device_info.id}",
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

		if self.ble_controller.last_connected_device().id == device_info.id and self.ble_controller.is_connected():
			disconnect_device_button = ctk.CTkButton(button_container,
			                                         text="Disconnetti",
			                                         fg_color=self.app_theme.danger_button,
			                                         font=CTkFont(family="Poppins", size=14, weight="bold"),
			                                         text_color=self.app_theme.danger_button_text,
			                                         hover_color=scale_lightness(self.app_theme.danger_button, 0.95),
			                                         width=200,
			                                         corner_radius=5,
			                                         command=lambda: self.ble_controller.disconnect(
				                                         self.__handle_disconnection)
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
			                                      command=lambda: self.ble_controller.connect(device_info,
			                                                                              self.__handle_connection)
			                                      )
			connect_device_button.grid(row=0, column=0)

		self.device_map[device_info.id] = device_box
		pass

	def __update_device_box(self, device_info: BLEDeviceInfo):
		if device_info.id not in self.device_map:
			return

		self.__remove_device_box(device_info)
		self.__create_device_box(device_info)

	def __show_device_box(self, device_info: BLEDeviceInfo):
		self.device_map[device_info.id].pack(side="top", fill="x", pady=5)

	def __remove_device_box(self, device_info: BLEDeviceInfo):
		if device_info.id in self.device_map:
			self.device_map[device_info.id].pack_forget()
			self.device_map[device_info.id].destroy()
			del self.device_map[device_info.id]

	def __hide_device_box(self, device_info: BLEDeviceInfo):
		if device_info.id in self.device_map:
			self.device_map[device_info.id].pack_forget()

	# passare errore di connect in modo tale da mandarlo al log
	def __handle_connection(self, device_info: BLEDeviceInfo, error=None):
		if error is not None:
			return print(f"Unable to connect to device, {error}")

		self.__update_device_box(device_info)
		self.application_messanger.dispatch(ApplicationMessagesEnum.START_VALUE_READER)

	def __handle_disconnection(self, device_info: BLEDeviceInfo, error=None):
		if error is not None:
			return print(f"Unable to disconnect, {error}")

		self.__update_device_box(device_info)
		self.application_messanger.dispatch(ApplicationMessagesEnum.STOP_VALUE_READER)

	# Backend methods

	def __start_scan(self):
		self.ble_scanner_controller.start_scan(60)

		self.__update_devices()

	def __update_devices(self):
		# Inside each of client, there's a scanner which contains the list of devices (and eventually they get updated)
		scanned_devices = self.ble_scanner_controller.get_devices()

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

		# Schedule the next poll
		self.after(1000, self.__update_devices)

	def __stop_scan(self):
		self.ble_scanner_controller.stop_scan()

import asyncio
import threading

import customtkinter as ctk
from customtkinter import CTkFont

from app.theme.AppTheme import AppTheme
from backend import Client
from backend.device.DeviceInfo import DeviceInfo


class DeviceWindow(ctk.CTkToplevel):
    def __init__(
            self,
            master: ctk.CTk,
            client: Client,
            app_theme: AppTheme = AppTheme()):
        super().__init__(master, fg_color=app_theme.primary_background)

        self.app_theme = app_theme
        self.client = client
        self.devices = []

        # This object maps an element box to the ID of the device
        self.device_map = {}

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

        self.discovered_devices_container = ctk.CTkScrollableFrame(container,
                                                                   fg_color=self.app_theme.primary_background)
        self.discovered_devices_container.pack(side="top", fill="both", expand=True)

        self.__start_scan()

        pass

    def __add_device(self, device_info: DeviceInfo):
        if device_info.id is None:
            raise Exception("Invalid device id")

        device_name = device_info.name or "Dispositivo senza nome"

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

        add_device_button = ctk.CTkButton(button_container,
                                          text="Connetti",
                                          text_color=self.app_theme.primary_button_text,
                                          fg_color=self.app_theme.primary_button,
                                          width=200,
                                          command=lambda: self.connect_device(device_info)
                                          )
        add_device_button.grid(row=0, column=0)

        self.device_map[device_box] = device_info.id
        pass

    # Backend methods
    def connect_device(self, device_info: DeviceInfo):
        self.client.connect(device_info)

    def __start_scan(self):
        self._scan_thread = threading.Thread(target=self.client.scanner.run_scan)
        self._scan_thread.start()

        self.__poll_devices()

    def __poll_devices(self):
        while not self.client.scanner.device_queue.empty():
            device = self.client.scanner.device_queue.get()
            if device not in self.devices:
                self.devices.append(device)
                self.__add_device(device)

        self.after(1000, self.__poll_devices)

    def __stop_scan(self):
        self.client.scanner.stop_scan()
        if self._scan_thread:  # Gracefully stop the scan thread
            self._scan_thread.join()

import customtkinter as ctk
from customtkinter import CTkFont

from app.theme.AppTheme import AppTheme
from app.utils.Color import scale_lightness
from backend.device.DeviceInfo import DeviceInfo


class DeviceWindow(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, app_theme: AppTheme = AppTheme()):
        super().__init__(master)
        self.app_theme = app_theme

        # This object maps an element box to the ID of the device
        self.element_map = {}

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
        container.pack(side="top", fill="both", padx=2)

        self.my_devices_container = ctk.CTkFrame(container, fg_color=self.app_theme.primary_background)
        self.my_devices_container.pack(side="top", fill="x")

        divider = ctk.CTkFrame(container, fg_color=self.app_theme.gray_text, height=2)
        divider.pack(side="top", fill="x", pady=1)

        self.discovered_devices_container = ctk.CTkFrame(container, fg_color=self.app_theme.primary_background)
        self.discovered_devices_container.pack(side="top", fill="x")

        button_container = ctk.CTkFrame(container, fg_color=self.app_theme.primary_background)
        button_container.pack(side="top", fill="both")

        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)

        start_scan_button = ctk.CTkButton(button_container, text="Refresh", fg_color=self.app_theme.element_background,
                                          font=CTkFont(family="Poppins", size=14, weight="bold"),
                                          text_color=self.app_theme.primary_button_text, corner_radius=5,
                                          hover_color=scale_lightness(self.app_theme.element_background, 0.95),
                                          width=70)
        start_scan_button.grid(row=0, column=0, sticky="ns")

        self.__add_device(DeviceInfo("1", "Device 1"))
        self.__add_device(DeviceInfo("2", "Device 2"))
        self.__add_device(DeviceInfo("2", "Device 3"), is_personal=True)

        pass

    def __add_device(self, device_info: DeviceInfo, is_personal=False):
        if device_info.id is None:
            raise Exception("Invalid device id")
        device_name = device_info.name or "Default"

        box_container = self.discovered_devices_container
        if is_personal:
            box_container = self.my_devices_container

        device_box = ctk.CTkFrame(box_container, fg_color=self.app_theme.element_background, corner_radius=5)
        device_box.pack(side="top", fill="x", padx=5, pady=5)

        device_name_label = ctk.CTkLabel(device_box, text=device_name, text_color=self.app_theme.primary_text,
                                         font=CTkFont(family="Poppins", size=14, weight="bold"),
                                         anchor="w", padx = 2
                                         )
        device_name_label.pack(side="top", fill="both")

        device_info_container = ctk.CTkFrame(
            device_box,
            fg_color=self.app_theme.element_background
        )
        device_info_container.pack(side="top", fill="both", pady=2)

        device_description_label = ctk.CTkLabel(device_info_container, text="Dispositivo fiero",
                                                text_color=self.app_theme.secondary_text,
                                                font=CTkFont(family="Poppins", size=12),
                                                anchor="w"
                                                )
        device_description_label.pack(side="left", fill="both")

        add_device_button = ctk.CTkButton(device_info_container, text="Connetti",
                                          width=200,
                                          )
        add_device_button.pack(side="right")

        self.element_map[device_box] = device_info.id
        pass
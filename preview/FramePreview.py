from tkinter import PhotoImage
from zipfile import sizeEndCentDir

import customtkinter as ctk
import pywinstyles
from CTkMenuBar import CTkTitleMenu

appTheme = {
    "button": "red",
    "plot": "green",
    "container": "blue",
    "input": "purple",
    "loadingBar": "yellow",
    "dataContainer": "pink",
    "mainContainer": "#FFFFFF",
}


class MainApplication(ctk.CTk):

    def __main_frame(self):
        self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW)


    def __bottom_frame(self):
        self.bottom_frame.grid(row=1, column=0, sticky=ctk.NSEW)

        container = ctk.CTkFrame(self.bottom_frame, fg_color=appTheme["container"], corner_radius=0)
        container.pack(side="top", fill="both", expand=True)

        data_container = ctk.CTkFrame(container, fg_color=appTheme["container"], corner_radius=0)
        data_container.pack(side="top", fill="both", expand=True, padx = 5, pady = (0,5))

        tool_container = ctk.CTkFrame(data_container, fg_color=appTheme["container"], corner_radius=0)
        tool_container.pack(side="top", fill="y", anchor="w", padx=30, pady=(5,5))

        tool_container.columnconfigure(0, weight=1)
        tool_container.columnconfigure(1, weight=1)
        tool_container.columnconfigure(2, weight=2)

        button1_frame = ctk.CTkFrame(tool_container, fg_color=appTheme["button"], corner_radius=0, width=40, height=40)
        button1_frame.grid(row=0, column=0, padx=(0,10))

        button2_frame = ctk.CTkFrame(tool_container, fg_color=appTheme["button"], corner_radius=0, width=40, height=40)
        button2_frame.grid(row=0, column=1, padx=(0,30))

        loading_bar_frame = ctk.CTkFrame(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400, height=20)
        loading_bar_frame.grid(row=0, column=2)



        table_frame = ctk.CTkFrame(data_container,fg_color=appTheme["dataContainer"], corner_radius=0)
        table_frame.pack(side="top", fill="both", expand=True)





    def __init__(self, app_theme=None):
        super().__init__()
        if app_theme is None:
            app_theme = appTheme

        # Informazioni finestra
        self.title("Frame Preview")
        self.geometry("800x600")

        # Barra della finestra
        menu = CTkTitleMenu(master=self, title_bar_color=0xFFFFFF)
        menu.add_cascade("        ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("          ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)

        # Suddivisione finestra
        self.main_frame = ctk.CTkFrame(self, fg_color=appTheme["mainContainer"], corner_radius=0)
        self.bottom_frame = ctk.CTkFrame(self, fg_color=appTheme["mainContainer"], corner_radius=0)

        # Suddivisione griglia
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=100)

        # Creazione finestre
        self.__main_frame()
        self.__bottom_frame()


if __name__ == "__main__":
    application = MainApplication(appTheme)
    application.mainloop()

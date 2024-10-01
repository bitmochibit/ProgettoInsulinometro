from tkinter import PhotoImage

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

        graph_control_container = ctk.CTkFrame(self.main_frame, fg_color=appTheme["container"], corner_radius=0)
        graph_control_container.columnconfigure(0, weight=2)
        graph_control_container.columnconfigure(1, weight=1)
        graph_control_container.rowconfigure(0, weight=100)

        # Plot container
        plot_container = ctk.CTkFrame(graph_control_container, fg_color=appTheme["container"], corner_radius=0)

        bode_container = ctk.CTkFrame(plot_container, fg_color=appTheme["container"], corner_radius=0)
        bode_container.pack(side="left", fill="both", expand=True, padx=(5,5))

        bode_graph_1_container = ctk.CTkFrame(bode_container, fg_color=appTheme["plot"], corner_radius=0)
        bode_graph_1_container.pack(side="top", fill="both", expand=True, pady=(0,5))

        bode_graph_2_container = ctk.CTkFrame(bode_container, fg_color=appTheme["plot"], corner_radius=0)
        bode_graph_2_container.pack(side="bottom", fill="both", expand=True, pady=(0,0))

        nyquist_container = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=0, width=280)
        nyquist_container.pack(side="right", fill="both", expand=True, padx=(0,5))
        plot_container.grid(row=0, column=0, sticky=ctk.NSEW)


        # Control container
        control_container = ctk.CTkFrame(graph_control_container, fg_color="purple", corner_radius=0, width=280)
        control_container.grid(row=0, column=1, sticky=ctk.NSEW)

        graph_control_container.pack(side="top", fill="both", expand=True)

    def __bottom_frame(self):
        self.bottom_frame.grid(row=1, column=0, sticky="nswe")

    def __init__(self, app_theme=None):
        super().__init__()
        if app_theme is None:
            app_theme = appTheme

        self.title("Frame Preview")
        self.geometry("800x600")

        menu = CTkTitleMenu(master=self, title_bar_color=0xFFFFFF)
        menu.add_cascade("        ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("          ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)
        menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)

        self.main_frame = ctk.CTkFrame(self, fg_color="grey", corner_radius=0)
        self.bottom_frame = ctk.CTkFrame(self, fg_color=appTheme["mainContainer"], corner_radius=0)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=100)


        self.__main_frame()
        self.__bottom_frame()


if __name__ == "__main__":
    application = MainApplication(appTheme)
    application.mainloop()

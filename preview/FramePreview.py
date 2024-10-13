# import customtkinter as ctk
# from CTkMenuBar import CTkTitleMenu
#
# # Legenda colori
# appTheme = {
#     "button": "red",
#     "plot": "green",
#     "container": "blue",
#     "input": "purple",
#     "loadingBar": "yellow",
#     "dataContainer": "pink",
#     "mainContainer": "#FFFFFF",
# }
#
#
# class MainApplication(ctk.CTk):
#
#     def __main_frame(self):
#         # Sezione dei grafici e dei controlli
#         self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW)
#         graph_section_container = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
#         graph_section_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
#
#         # Sezione dei grafici
#
#         # Suddivisione finestra
#         plot_container = ctk.CTkFrame(graph_section_container, fg_color="transparent", corner_radius=0)
#         plot_container.pack(side="left", fill="both", expand=True)
#
#         plot_container.columnconfigure(0, weight=1)
#         plot_container.columnconfigure(1, weight=1)
#         plot_container.columnconfigure(2, weight=1)
#
#         plot_container.rowconfigure(0, weight=1)
#         plot_container.rowconfigure(1, weight=1)
#
#         # Grafici
#         bode1_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
#         bode1_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=ctk.NSEW)
#
#         bode2_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
#         bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)
#
#         nyquist_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
#         nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)
#
#         # Sezione dei controlli
#
#         # Suddivisione finestra
#         controller_container = ctk.CTkFrame(graph_section_container, fg_color=appTheme["container"], corner_radius=5)
#         controller_container.pack(side="right", fill="both")
#
#         # Pulsanti
#         tab_container = ctk.CTkFrame(controller_container, fg_color="transparent")
#         tab_container.pack(side="top", fill="both")
#
#         fixed_tab = ctk.CTkButton(tab_container, text="", fg_color=appTheme["button"], height=50, corner_radius=5,
#                                   background_corner_colors=[
#                                       appTheme["mainContainer"], appTheme["button"], appTheme["button"],
#                                       appTheme["button"]
#                                   ])
#         fixed_tab.pack(anchor="n", side="left", fill="x", ipadx=1)
#
#         sweep_tab = ctk.CTkButton(tab_container, text="", fg_color=appTheme["button"], height=50, corner_radius=5,
#                                   background_corner_colors=[
#                                       appTheme["button"], appTheme["mainContainer"], appTheme["button"],
#                                       appTheme["button"]
#                                   ])
#         sweep_tab.pack(anchor="n", side="right", fill="x")
#
#         # Finestre di input
#         input_container = ctk.CTkFrame(controller_container, fg_color="transparent")
#         input_container.pack(side="top", fill="both")
#
#         input1 = ctk.CTkEntry(input_container, fg_color=appTheme["input"], corner_radius=5)
#         input1.pack(side="top", fill="x", padx=5, pady=5)
#
#         input2 = ctk.CTkEntry(input_container, fg_color=appTheme["input"], corner_radius=5)
#         input2.pack(side="top", fill="x", padx=5, pady=5)
#
#         input3 = ctk.CTkEntry(input_container, fg_color=appTheme["input"], corner_radius=5)
#         input3.pack(side="top", fill="x", padx=5, pady=5)
#
#         # Pulsanti di controllo
#         control_container = ctk.CTkFrame(controller_container, fg_color="transparent")
#         control_container.pack(anchor="s", side="bottom", fill="both", pady=(0, 10))
#
#         control_container.columnconfigure(0, weight=1)
#         control_container.columnconfigure(1, weight=1)
#         control_container.columnconfigure(2, weight=1)
#
#         button1 = ctk.CTkButton(control_container, text="", fg_color=appTheme["button"], corner_radius=0, width=70)
#         button1.grid(row=0, column=0)
#
#         button2 = ctk.CTkButton(control_container, text="", fg_color=appTheme["button"], corner_radius=0, width=70)
#         button2.grid(row=0, column=1)
#
#         button3 = ctk.CTkButton(control_container, text="", fg_color=appTheme["button"], corner_radius=0, width=40)
#         button3.grid(row=0, column=2)
#
#         pass
#
#     def __bottom_frame(self):
#         # Sezione dati
#         self.bottom_frame.grid(row=1, column=0, sticky=ctk.NSEW)
#
#         data_container = ctk.CTkFrame(self.bottom_frame, fg_color=appTheme["container"], corner_radius=0)
#         data_container.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))
#
#         # Sezione dei pulsanti
#
#         # Suddivisione finestra
#         tool_container = ctk.CTkFrame(data_container, fg_color=appTheme["container"], corner_radius=0)
#         tool_container.pack(side="top", fill="y", anchor="w", padx=30, pady=(5, 5))
#
#         tool_container.columnconfigure(0, weight=1)
#         tool_container.columnconfigure(1, weight=1)
#         tool_container.columnconfigure(2, weight=2)
#
#         # Pulsanti
#         button1_frame = ctk.CTkButton(tool_container, text="", fg_color=appTheme["button"], corner_radius=0, width=40,
#                                       height=40)
#         button1_frame.grid(row=0, column=0, padx=(0, 10))
#
#         button2_frame = ctk.CTkButton(tool_container, text="", fg_color=appTheme["button"], corner_radius=0, width=40,
#                                       height=40)
#         button2_frame.grid(row=0, column=1, padx=(0, 30))
#
#         # Barra di caricamento
#         loading_bar_frame = ctk.CTkFrame(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400,
#                                          height=20)
#         # loading_bar_frame = ctk.CTkProgressBar(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400, height=20)
#         loading_bar_frame.grid(row=0, column=2)
#
#         # Tabella dei dati
#         table_frame = ctk.CTkFrame(data_container, fg_color=appTheme["dataContainer"], corner_radius=0)
#         table_frame.pack(side="top", fill="both", expand=True)
#         pass
#
#     def __init__(self, app_theme=None):
#         super().__init__()
#         if app_theme is None:
#             app_theme = appTheme
#
#         # Informazioni finestra
#         self.title("Frame Preview")
#         self.geometry("800x600")
#
#         # Barra della finestra
#         menu = CTkTitleMenu(master=self, title_bar_color=0xFFFFFF)
#         menu.add_cascade("        ", fg_color=appTheme["button"], corner_radius=0)
#         menu.add_cascade("          ", fg_color=appTheme["button"], corner_radius=0)
#         menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)
#         menu.add_cascade("     ", fg_color=appTheme["button"], corner_radius=0)
#
#         # Suddivisione finestra
#         self.main_frame = ctk.CTkFrame(self, fg_color=appTheme["mainContainer"], corner_radius=0)
#         self.bottom_frame = ctk.CTkFrame(self, fg_color=appTheme["container"], corner_radius=0)
#
#         # Suddivisione griglia
#         self.rowconfigure(0, weight=2)
#         self.rowconfigure(1, weight=1)
#
#         self.columnconfigure(0, weight=100)
#
#         # Creazione finestre
#         self.__main_frame()
#         self.__bottom_frame()
#
#
# if __name__ == "__main__":
#     application = MainApplication(appTheme)
#     application.mainloop()

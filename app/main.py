import customtkinter as ctk
from CTkMenuBar import CTkTitleMenu

# emoji come icone temporanee

# Legenda colori
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
		# Sezione dei grafici e dei controlli
		self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW)
		graph_section_container = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
		graph_section_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)

		# Sezione dei grafici
		# Suddivisione finestra
		plot_container = ctk.CTkFrame(graph_section_container, fg_color="transparent", corner_radius=0)
		plot_container.pack(side="left", fill="both", expand=True)

		plot_container.columnconfigure(0, weight=1)
		plot_container.columnconfigure(1, weight=1)
		plot_container.columnconfigure(2, weight=1)

		plot_container.rowconfigure(0, weight=1)
		plot_container.rowconfigure(1, weight=1)

		# Grafici
		bode1_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
		bode1_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=ctk.NSEW)

		bode2_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
		bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)

		nyquist_frame = ctk.CTkFrame(plot_container, fg_color=appTheme["plot"], corner_radius=5)
		nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)

		# Sezione dei controlli
		# Suddivisione finestra
		controller_container = ctk.CTkFrame(graph_section_container, fg_color=appTheme["container"], corner_radius=5)
		controller_container.pack(side="right", fill="both")

		# Pulsanti per cambiare metodo di campionamento
		tab_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		tab_container.pack(side="top", fill="both")

		fixed_tab = ctk.CTkButton(tab_container, text="Fixed", fg_color=appTheme["button"], height=50, corner_radius=5,
								  background_corner_colors=[
									  appTheme["mainContainer"], appTheme["button"], appTheme["button"],
									  appTheme["button"]
								  ], command=self.__fixed_button)
		fixed_tab.pack(anchor="n", side="left", fill="x", ipadx=1)

		sweep_tab = ctk.CTkButton(tab_container, text="Sweep", fg_color=appTheme["button"], height=50, corner_radius=5,
								  background_corner_colors=[
									  appTheme["button"], appTheme["mainContainer"], appTheme["button"],
									  appTheme["button"]
								  ], command=self.__sweep_button)
		sweep_tab.pack(anchor="n", side="right", fill="x")

		# Finestre di input
		input_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		input_container.pack(side="top", fill="both")

		frequency = LabelledInput(input_container, "Frequenza")
		frequency.pack(side="top", fill="x", padx=5, pady=5)

		magnitude = LabelledInput(input_container, "Ampiezza")
		magnitude.pack(side="top", fill="x", padx=5, pady=5)

		# Pulsanti di controllo
		control_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		control_container.pack(anchor="s", side="bottom", fill="both", pady=(0, 10))

		control_container.columnconfigure(0, weight=1)
		control_container.columnconfigure(1, weight=1)
		control_container.columnconfigure(2, weight=1)

		start_button = ctk.CTkButton(control_container, text="Start", fg_color=appTheme["button"], corner_radius=0, width=70,
								command=self.__start_button)
		start_button.grid(row=0, column=0)

		stop_button = ctk.CTkButton(control_container, text="Stop", fg_color=appTheme["button"], corner_radius=0, width=70,
								command=self.__stop_button)
		stop_button.grid(row=0, column=1)

		marker_button = ctk.CTkButton(control_container, text="📌", fg_color=appTheme["button"], corner_radius=0, width=40,
								command=self.__marker_button)
		marker_button.grid(row=0, column=2)

		pass

	def __bottom_frame(self):
		# Sezione dati
		self.bottom_frame.grid(row=1, column=0, sticky=ctk.NSEW)

		data_container = ctk.CTkFrame(self.bottom_frame, fg_color=appTheme["container"], corner_radius=0)
		data_container.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))

		# Sezione dei pulsanti

		# Suddivisione finestra
		tool_container = ctk.CTkFrame(data_container, fg_color=appTheme["container"], corner_radius=0)
		tool_container.pack(side="top", fill="y", anchor="w", padx=30, pady=(5, 5))

		tool_container.columnconfigure(0, weight=1)
		tool_container.columnconfigure(1, weight=1)
		tool_container.columnconfigure(2, weight=2)

		# Pulsanti
		button1_frame = ctk.CTkButton(tool_container, text="Data", fg_color=appTheme["button"], corner_radius=0,
									  width=40,
									  height=40, command=self.__data_button)
		button1_frame.grid(row=0, column=0, padx=(0, 10))

		button2_frame = ctk.CTkButton(tool_container, text="Logs", fg_color=appTheme["button"], corner_radius=0,
									  width=40,
									  height=40, command=self.__logs_button)
		button2_frame.grid(row=0, column=1, padx=(0, 30))

		# Barra di caricamento
		loading_bar_frame = ctk.CTkFrame(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400,
										 height=20)
		# loading_bar_frame = ctk.CTkProgressBar(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400, height=20)
		loading_bar_frame.grid(row=0, column=2)

		# Tabella dei dati
		# Aggiungere le tre colonne (todo)
		table_frame = ctk.CTkFrame(data_container, fg_color=appTheme["dataContainer"], corner_radius=0)
		table_frame.pack(side="top", fill="both", expand=True)
		pass

	def __init__(self, app_theme=None):
		super().__init__()
		if app_theme is None:
			app_theme = appTheme

		# Informazioni finestra
		self.title("Frame Preview")
		self.geometry("800x600")

		# Barra della finestra
		menu = CTkTitleMenu(master=self, title_bar_color=0xFFFFFF)
		menu.add_cascade("File", fg_color=appTheme["button"], corner_radius=0, command=self.__file_button)
		menu.add_cascade("Device", fg_color=appTheme["button"], corner_radius=0, command=self.__device_button)
		menu.add_cascade("🔋", fg_color=appTheme["button"], corner_radius=0, command=self.__battery_button)
		menu.add_cascade("📶", fg_color=appTheme["button"], corner_radius=0, command=self.__signal_button)

		# Suddivisione finestra
		self.main_frame = ctk.CTkFrame(self, fg_color=appTheme["mainContainer"], corner_radius=0)
		self.bottom_frame = ctk.CTkFrame(self, fg_color=appTheme["container"], corner_radius=0)

		# Suddivisione griglia
		self.rowconfigure(0, weight=2)
		self.rowconfigure(1, weight=1)

		self.columnconfigure(0, weight=100)

		# Creazione finestre
		self.__main_frame()
		self.__bottom_frame()

	# Funzioni dei pulsanti
	def __start_button(self):
		print("start button")

	def __stop_button(self):
		print("stop button")

	def __marker_button(self):
		print("marker button")

	def __logs_button(self):
		print("logs button")

	def __data_button(self):
		print("data button")

	def __file_button(self):
		print("file button")

	def __device_button(self):
		print("device button")

	def __battery_button(self):
		print("battery button")

	def __signal_button(self):
		print("signal button")

	def __fixed_button(self):
		print("fixed button")

	def __sweep_button(self):
		print("sweep button")


# Finestre di input
class LabelledInput():
	def __init__(self, master, text):
		self.container = ctk.CTkFrame(master, fg_color="transparent")
		self.input = ctk.CTkEntry(self.container, fg_color=appTheme["input"])
		self.label = ctk.CTkLabel(self.container, text=text, anchor="w", fg_color="transparent")
		self.label.pack(side="top", fill="both")
		self.input.pack(side="top", fill="both")

	#Metodi della classa per posizionare il self.container
	def pack(self, **kwargs):
		self.container.pack(**kwargs)

	def grid(self, **kwargs):
		self.container.grid(**kwargs)

	def place(self, **kwargs):
		self.container.place(**kwargs)


if __name__ == "__main__":
	application = MainApplication(appTheme)
	application.mainloop()

from typing import Union, Optional, Tuple

import customtkinter as ctk
from CTkMenuBar import CTkTitleMenu
from customtkinter import CTkFrame, CTkImage, CTkEntry, CTkFont


# from PIL import Image, ImageDraw, ImageFont


# emoji come icone temporanee

# Classe per la definizione statica del tema
class AppTheme:
	def __init__(self, button="red", plot="green", container="blue", input="purple", loading_bar="yellow",
	             data_container="pink", main_container="white"):
		self.button = button
		self.plot = plot
		self.container = container
		self.input = input
		self.loading_bar = loading_bar
		self.data_container = data_container
		self.main_container = main_container


# Classe estesa per il menu personalizzato, per qualche strano motivo quello di base supporta solo il testo
class ExtendedTitleMenu(CTkTitleMenu):
	def __init__(self,
	             master,
	             title_bar_color=0xFFFFFF,
	             padx: int = 10,
	             width: int = 10,
	             x_offset: int = None,
	             y_offset: int = None,
	             app_theme: AppTheme = AppTheme()
	             ):
		super().__init__(master, title_bar_color, padx, width, x_offset, y_offset)
		self.app_theme = app_theme

	def add_frame(self, frame: CTkFrame):
		frame.grid(row=0, column=self.num, padx=(0, self.padding))


# Elementi

# def emoji(emoji, size=32):
# 	font = ImageFont.truetype("seguiemj.ttf", size=int(size / 1.5))
# 	img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
# 	draw = ImageDraw.Draw(img)
# 	draw.text((size / 2, size / 2), emoji,
# 	          embedded_color=True, font=font, anchor="mm")
# 	img = CTkImage(img, size=(size, size))
# 	return img


class LabelledInput(CTkEntry):
	class EntryOptions:
		def __init__(self,
		             width: int = 140,
		             height: int = 28,
		             corner_radius: Optional[int] = None,
		             border_width: Optional[int] = None,

		             bg_color: Union[str, Tuple[str, str]] = "transparent",
		             fg_color: Optional[Union[str, Tuple[str, str]]] = None,
		             border_color: Optional[Union[str, Tuple[str, str]]] = None,
		             text_color: Optional[Union[str, Tuple[str, str]]] = None,
		             placeholder_text_color: Optional[Union[str, Tuple[str, str]]] = None,

		             textvariable: Union[ctk.Variable, None] = None,
		             placeholder_text: Union[str, None] = None,
		             font: Optional[Union[tuple, CTkFont]] = None,
		             state: str = ctk.NORMAL,
		             **kwargs):
			self.width = width
			self.height = height
			self.corner_radius = corner_radius
			self.border_width = border_width
			self.bg_color = bg_color
			self.fg_color = fg_color
			self.border_color = border_color
			self.text_color = text_color
			self.placeholder_text_color = placeholder_text_color
			self.textvariable = textvariable
			self.placeholder_text = placeholder_text
			self.font = font
			self.state = state
			self.kwargs = kwargs

	class LabelOptions:
		def __init__(self,
		             width: int = 0,
		             height: int = 28,
		             corner_radius: Optional[int] = None,

		             bg_color: Union[str, Tuple[str, str]] = "transparent",
		             fg_color: Optional[Union[str, Tuple[str, str]]] = None,
		             text_color: Optional[Union[str, Tuple[str, str]]] = None,
		             text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

		             text: str = "CTkLabel",
		             font: Optional[Union[tuple, CTkFont]] = None,
		             image: Union[CTkImage, None] = None,
		             compound: str = "center",
		             anchor: str = "w",  # label anchor: center, n, e, s, w
		             wraplength: int = 0,
		             **kwargs):
			self.width = width
			self.height = height
			self.corner_radius = corner_radius
			self.bg_color = bg_color
			self.fg_color = fg_color
			self.text_color = text_color
			self.text_color_disabled = text_color_disabled
			self.text = text
			self.font = font
			self.image = image
			self.compound = compound
			self.anchor = anchor
			self.wraplength = wraplength
			self.kwargs = kwargs

	def __init__(self,
	             master,
	             entry_options: EntryOptions = EntryOptions(),
	             label_options: LabelOptions = LabelOptions(),
	             app_theme: AppTheme = AppTheme(),
	             **kwargs):
		super().__init__(master, **kwargs)
		self.current_input_variable = entry_options.textvariable
		self.container = ctk.CTkFrame(master, fg_color="transparent", **kwargs)
		self.input = ctk.CTkEntry(self.container,
		                          width=entry_options.width,
		                          height=entry_options.height,
		                          corner_radius=entry_options.corner_radius,
		                          border_width=entry_options.border_width,
		                          bg_color=entry_options.bg_color,
		                          fg_color=entry_options.fg_color if entry_options.fg_color is not None else app_theme.input,
		                          border_color=entry_options.border_color,
		                          text_color=entry_options.text_color,
		                          placeholder_text_color=entry_options.placeholder_text_color,
		                          placeholder_text=entry_options.placeholder_text,
		                          font=entry_options.font,
		                          state=entry_options.state,
		                          **entry_options.kwargs
		                          )
		self.label = ctk.CTkLabel(self.container,
		                          width=label_options.width,
		                          height=label_options.height,
		                          corner_radius=label_options.corner_radius,
		                          bg_color=label_options.bg_color,
		                          fg_color=label_options.fg_color,
		                          text_color=label_options.text_color,
		                          text_color_disabled=label_options.text_color_disabled,
		                          text=label_options.text,
		                          font=label_options.font,
		                          image=label_options.image,
		                          compound=label_options.compound,
		                          anchor=label_options.anchor,
		                          wraplength=label_options.wraplength,
		                          **label_options.kwargs
		                          )
		if entry_options.textvariable is not None:
			# Aggiungi un listener all'input per aggiornare il valore della textvariable
			def update_variable(e):
				self.current_input_variable.set(self.input.get())
			self.input.bind("<KeyRelease>", update_variable)

		self.label.pack(side="top", fill="both")
		self.input.pack(side="top", fill="both")

	# Metodi della classe per posizionare il self.container
	def pack(self, **kwargs):
		self.container.pack(**kwargs)

	def grid(self, **kwargs):
		self.container.grid(**kwargs)

	def place(self, **kwargs):
		self.container.place(**kwargs)

	def get(self):
		return self.input.get()


class MainApplication(ctk.CTk):
	def __title_menu(self):
		self.title("Insulinometro")
		self.geometry("800x600")
		menu = ExtendedTitleMenu(master=self)
		menu.add_cascade("File", fg_color=self.app_theme.button, command=self.__file_button)
		menu.add_cascade("Device", fg_color=self.app_theme.button, command=self.__device_button)
		menu.add_cascade("🔋", fg_color=self.app_theme.button, command=self.__battery_button)
		menu.add_cascade("📶", fg_color=self.app_theme.button, command=self.__signal_button)

	def __main_frame(self):
		self.main_frame = ctk.CTkFrame(self, fg_color=self.app_theme.main_container, corner_radius=0)
		self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW)
		# Sezione dei grafici e dei controlli
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
		bode1_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.plot, corner_radius=5)
		bode1_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=ctk.NSEW)

		bode2_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.plot, corner_radius=5)
		bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)

		nyquist_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.plot, corner_radius=5)
		nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)

		# Sezione dei controlli
		# Suddivisione finestra
		controller_container = ctk.CTkFrame(graph_section_container, fg_color=self.app_theme.container, corner_radius=5)
		controller_container.pack(side="right", fill="both")

		# Pulsanti per cambiare metodo di campionamento
		tab_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		tab_container.pack(side="top", fill="both")

		# noinspection PyTypeChecker
		fixed_tab = ctk.CTkButton(tab_container, text="Fixed", fg_color=self.app_theme.button, height=50,
		                          corner_radius=5,
		                          background_corner_colors=(
			                          self.app_theme.main_container,
			                          self.app_theme.button,
			                          self.app_theme.button,
			                          self.app_theme.button
		                          ), command=self.__fixed_button)
		fixed_tab.pack(anchor="n", side="left", fill="x", ipadx=1)
		# noinspection PyTypeChecker
		sweep_tab = ctk.CTkButton(tab_container, text="Sweep", fg_color=self.app_theme.button, height=50,
		                          corner_radius=5,
		                          background_corner_colors=(
			                          self.app_theme.button,
			                          self.app_theme.main_container,
			                          self.app_theme.button,
			                          self.app_theme.button
		                          ), command=self.__sweep_button)
		sweep_tab.pack(anchor="n", side="right", fill="x")

		# Finestre di input
		input_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		input_container.pack(side="top", fill="both")

		frequency_input = LabelledInput(input_container,
		                                     entry_options=LabelledInput.EntryOptions(
			                                     textvariable=self.frequency_string,
			                                     placeholder_text="Frequenza (Hz)",
		                                     ),
		                                     label_options=LabelledInput.LabelOptions(
			                                     text="Frequenza",
		                                     ),
		                                     app_theme=self.app_theme
		                                     )
		frequency_input.pack(side="top", fill="x", padx=5, pady=5)

		magnitude_input = LabelledInput(input_container,
		                                     entry_options=LabelledInput.EntryOptions(
			                                     textvariable=self.magnitude_string,
			                                     placeholder_text="Ampiezza (mV)",
		                                     ),
		                                     label_options=LabelledInput.LabelOptions(
			                                     text="Ampiezza",
		                                     ),
		                                     app_theme=self.app_theme
		                                     )
		magnitude_input.pack(side="top", fill="x", padx=5, pady=5)

		# Pulsanti di controllo
		control_container = ctk.CTkFrame(controller_container, fg_color="transparent")
		control_container.pack(anchor="s", side="bottom", fill="both", pady=(0, 10))

		control_container.columnconfigure(0, weight=1)
		control_container.columnconfigure(1, weight=1)
		control_container.columnconfigure(2, weight=1)

		start_button = ctk.CTkButton(control_container, text="Start", fg_color=self.app_theme.button, corner_radius=0,
		                             width=70,
		                             command=self.__start_button)
		start_button.grid(row=0, column=0)

		stop_button = ctk.CTkButton(control_container, text="Stop", fg_color=self.app_theme.button, corner_radius=0,
		                            width=70,
		                            command=self.__stop_button)
		stop_button.grid(row=0, column=1)

		marker_button = ctk.CTkButton(control_container, text="📌", fg_color=self.app_theme.button, corner_radius=0,
		                              width=40,
		                              command=self.__marker_button)
		marker_button.grid(row=0, column=2)

		pass

	def __bottom_frame(self):
		# Sezione dati
		self.bottom_frame = ctk.CTkFrame(self, fg_color=self.app_theme.container, corner_radius=0)
		self.bottom_frame.grid(row=1, column=0, sticky=ctk.NSEW)

		data_container = ctk.CTkFrame(self.bottom_frame, fg_color=self.app_theme.container, corner_radius=0)
		data_container.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))

		# Sezione dei pulsanti
		# Suddivisione finestra
		tool_container = ctk.CTkFrame(data_container, fg_color=self.app_theme.container, corner_radius=0)
		tool_container.pack(side="top", fill="y", anchor="w", padx=30, pady=(5, 5))

		tool_container.columnconfigure(0, weight=1)
		tool_container.columnconfigure(1, weight=1)
		tool_container.columnconfigure(2, weight=2)

		# Pulsanti
		data_button = ctk.CTkButton(tool_container, text="Data", fg_color=self.app_theme.button, corner_radius=0,
		                            width=40,
		                            height=40, command=self.__data_button)
		data_button.grid(row=0, column=0, padx=(0, 10))

		logs_button = ctk.CTkButton(tool_container, text="Logs", fg_color=self.app_theme.button, corner_radius=0,
		                            width=40,
		                            height=40, command=self.__logs_button)
		logs_button.grid(row=0, column=1, padx=(0, 30))

		# Barra di caricamento
		loading_bar_frame = ctk.CTkFrame(tool_container, fg_color=self.app_theme.loading_bar, corner_radius=0,
		                                 width=400,
		                                 height=20)
		# loading_bar_frame = ctk.CTkProgressBar(tool_container, fg_color=appTheme["loadingBar"], corner_radius=0, width=400, height=20)
		loading_bar_frame.grid(row=0, column=2)

		# Tabella dei dati
		table_frame = ctk.CTkFrame(data_container, fg_color=self.app_theme.data_container, corner_radius=0)
		table_frame.pack(side="top", fill="both", expand=True)

		table_frame.columnconfigure(0, weight=1)
		table_frame.columnconfigure(1, weight=1)
		table_frame.columnconfigure(2, weight=1)

		table_frame.rowconfigure(0, weight=1)
		table_frame.rowconfigure(1, weight=1)
		table_frame.rowconfigure(2, weight=1)

		frequency_label = ctk.CTkLabel(table_frame, text="Frequenza", text_color="black")
		frequency_label.grid(row=0, column=0, sticky="nsew")

		phase_label = ctk.CTkLabel(table_frame, text="Fase", text_color="black")
		phase_label.grid(row=0, column=1, sticky="nsew")

		magnitude_label = ctk.CTkLabel(table_frame, text="Ampiezza", text_color="black")
		magnitude_label.grid(row=0, column=2, sticky="nsew")

		datas1_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas1_text.grid(row=1, column=0, sticky="nsew")
		datas2_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas2_text.grid(row=1, column=1, sticky="nsew")
		datas3_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas3_text.grid(row=1, column=2, sticky="nsew")

		datas4_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas4_text.grid(row=2, column=0, sticky="nsew")
		datas5_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas5_text.grid(row=2, column=1, sticky="nsew")
		datas6_text = ctk.CTkLabel(table_frame, text="Data", text_color="black")
		datas6_text.grid(row=2, column=2, sticky="nsew")
		pass

	def __init__(self, app_theme: AppTheme = AppTheme()):
		super().__init__()
		self.app_theme = app_theme

		self.frequency_string = ctk.StringVar()
		self.magnitude_string = ctk.StringVar()

		# Menu titolo finestra
		self.__title_menu()

		# Suddivisione griglia layout finestra
		self.rowconfigure(0, weight=2)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=100)

		# Creazione finestre
		self.__main_frame()
		self.__bottom_frame()

	# Funzioni dei pulsanti
	def __start_button(self):
		print(f"Frequenza: {self.frequency_string.get()} \nAmpiezza: {self.magnitude_string.get()}")

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


if __name__ == "__main__":
	application = MainApplication(AppTheme())
	application.mainloop()

import tkinter.font
from tkinter import Widget
from typing import Union, Optional, Tuple, Callable, Any

import customtkinter as ctk
from CTkMenuBar import CTkTitleMenu
from PIL.ImageCms import buildTransformFromOpenProfiles
from customtkinter import CTkFrame, CTkImage, CTkEntry, CTkFont, CTkTabview, CTkButton, CTkSegmentedButton, CTkCanvas
import colorsys


# from PIL import Image, ImageDraw, ImageFont


def scale_lightness(hexStr, scale_l):
	# Convert hexStr to rgb (tuple of 3 floats)
	rgb = [int(hexStr[i:i + 2], 16) / 255.0 for i in range(1, 6, 2)]
	h, l, s = colorsys.rgb_to_hls(*rgb)
	# manipulate h, l, s values and return as rgb
	new_rgb = colorsys.hls_to_rgb(h, min(1, l * scale_l), s=s)
	return "#" + "".join(f"{int(255 * x):02x}" for x in new_rgb)


# emoji come icone temporanee

# Classe per la definizione statica del tema, sara' possibile estenderla per sovrascrivere i colori
class AppTheme:
	def __init__(self,
	             transparent="transparent",

	             primary_background="#F9F8FD",
	             secondary_background="#F1F2F7",
	             element_background="#FFFFFF",
	             element_secondary_background="#F3EDF7",

	             primary_text="#1D1E4D",
	             secondary_text="#535178",
	             light_text="#FFFFFF",
	             gray_text="#434242",
	             light_gray_text="#CAC4D0",

	             primary_button="#EBFFFC",
	             primary_button_text="#003830",

	             warning_button="#FFF9EB",
	             warning_button_text="#422E00",

	             danger_button="#FFEBEF",
	             danger_button_text="#800019",

	             ):
		self.transparent = transparent

		self.primary_background = primary_background
		self.secondary_background = secondary_background
		self.element_background = element_background
		self.element_secondary_background = element_secondary_background

		self.primary_text = primary_text
		self.secondary_text = secondary_text
		self.light_text = light_text
		self.gray_text = gray_text
		self.light_gray_text = light_gray_text

		self.primary_button = primary_button
		self.primary_button_text = primary_button_text

		self.warning_button = warning_button
		self.warning_button_text = warning_button_text

		self.danger_button = danger_button
		self.danger_button_text = danger_button_text
		pass


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


# Classe estesa per il tabview personalizzato, che e' fatta MALISSIMO
class ExtendedTabview(CTkTabview):
	def __init__(self,
	             master: Any,
	             width: int = 300,
	             height: int = 250,
	             corner_radius: Optional[int] = None,
	             border_width: Optional[int] = None,

	             bg_color: Union[str, Tuple[str, str]] = "transparent",
	             fg_color: Optional[Union[str, Tuple[str, str]]] = None,
	             border_color: Optional[Union[str, Tuple[str, str]]] = None,

	             segmented_button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
	             segmented_button_selected_color: Optional[Union[str, Tuple[str, str]]] = None,
	             segmented_button_selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
	             segmented_button_unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
	             segmented_button_unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
	             segmented_button_font: Optional[CTkFont] = None,


	             text_color: Optional[Union[str, Tuple[str, str]]] = None,
	             text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

	             command: Union[Callable, Any] = None,
	             anchor: str = "center",
	             state: str = "normal",
	             app_theme: AppTheme = AppTheme(),
	             **kwargs):
		super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
		                 segmented_button_fg_color, segmented_button_selected_color,
		                 segmented_button_selected_hover_color,
		                 segmented_button_unselected_color, segmented_button_unselected_hover_color, text_color,
		                 text_color_disabled, command, anchor, state, **kwargs)
		self.app_theme = app_theme


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
		                          fg_color=entry_options.fg_color if entry_options.fg_color is not None else app_theme.element_background,
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
			# Aggiungi un listener all'input per aggiornare il valore della textvariable (devo fare cosi' per forza perche' senno' sparisce il placeholder)
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

		file_button_container = ctk.CTkFrame(menu, fg_color="transparent")
		file_button = ctk.CTkButton(file_button_container, text="File", text_color=self.app_theme.primary_text,
		                            fg_color=self.app_theme.transparent, corner_radius=0, command=self.__file_button)

		device_button_container = ctk.CTkFrame(menu, fg_color="transparent")
		device_button = ctk.CTkButton(device_button_container, text="Device", text_color=self.app_theme.primary_text,
		                              fg_color=self.app_theme.transparent, corner_radius=0,
		                              command=self.__device_button)

		battery_button_container = ctk.CTkFrame(menu, fg_color="transparent")
		battery_button = ctk.CTkButton(battery_button_container, text="🔋", text_color=self.app_theme.primary_text,
		                               fg_color=self.app_theme.transparent, corner_radius=0,
		                               command=self.__battery_button)

		signal_button_container = ctk.CTkFrame(menu, fg_color="transparent")
		signal_button = ctk.CTkButton(signal_button_container, text="📶", text_color=self.app_theme.primary_text,
		                              fg_color=self.app_theme.transparent, corner_radius=0,
		                              command=self.__signal_button)

		menu.add_frame(file_button_container)
		menu.add_frame(device_button_container)
		menu.add_frame(battery_button_container)
		menu.add_frame(signal_button_container)

	def __main_frame(self):
		self.main_frame = ctk.CTkFrame(self, fg_color=self.app_theme.secondary_background, corner_radius=0)
		self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW)
		# Sezione dei grafici e dei controlli
		graph_section_container = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
		graph_section_container.pack(side="top", fill="both", expand=True, padx=10, pady=25)

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
		bode1_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.element_background, corner_radius=5)
		bode1_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=ctk.NSEW)

		bode2_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.element_background, corner_radius=5)
		bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)

		nyquist_frame = ctk.CTkFrame(plot_container, fg_color=self.app_theme.element_background, corner_radius=5)
		nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)

		# Sezione dei controlli
		# Suddivisione finestra
		controller_container = ctk.CTkFrame(graph_section_container, fg_color=self.app_theme.transparent,
		                                    corner_radius=5)
		controller_container.pack(side="left", fill="both")

		# Tab view dei controlli (Fixed, Sweep)
		measurement_mode_tabview = ctk.CTkTabview(controller_container,
		                                          fg_color=self.app_theme.element_background,
		                                          text_color=(
			                                          self.app_theme.light_gray_text, self.app_theme.primary_text),
		                                          width=250,
		                                          segmented_button_fg_color=self.app_theme.element_secondary_background,
		                                          segmented_button_selected_color=scale_lightness(
			                                          self.app_theme.element_secondary_background, 0.96),
		                                          segmented_button_unselected_color=self.app_theme.element_secondary_background,
		                                          segmented_button_unselected_hover_color=scale_lightness(
			                                          self.app_theme.element_secondary_background, 0.95),
		                                          segmented_button_selected_hover_color=scale_lightness(
			                                          self.app_theme.element_secondary_background, 0.96),
		                                          corner_radius=5,
		                                          border_width=0,
		                                          anchor="e"
		                                          )
		measurement_mode_tabview.pack(side="top", fill="both")

		tabview_segmented_button: CTkSegmentedButton | None = measurement_mode_tabview.children.get(
			"!ctksegmentedbutton")  # 🍆

		fixed_tab = measurement_mode_tabview.add("Fixed")
		sweep_tab = measurement_mode_tabview.add("Sweep")
		measurement_mode_tabview.set("Fixed")

		tabview_segmented_button.configure(
			font=CTkFont(family="Poppins", size=16, weight="bold"),
			background_corner_colors=(
				self.app_theme.secondary_background, self.app_theme.secondary_background,
				self.app_theme.element_secondary_background, self.app_theme.element_secondary_background
			),
			height=40
		)
		tabview_segmented_button.grid_configure(row=0, sticky="news", padx=(0, 0))

		# Finestre di input
		input_container = ctk.CTkFrame(fixed_tab, fg_color=self.app_theme.element_background, corner_radius=5)
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
		controls_section = ctk.CTkFrame(controller_container, fg_color=self.app_theme.element_background,
		                                corner_radius=5)
		controls_section.pack(fill="both", expand=True)

		button_container = ctk.CTkFrame(controls_section, fg_color="transparent")
		button_container.pack(anchor="s", side="bottom", fill="both", pady=(0, 10))

		button_container.columnconfigure(0, weight=1)
		button_container.columnconfigure(1, weight=1)
		button_container.columnconfigure(2, weight=1)

		start_button = ctk.CTkButton(button_container, text="START", fg_color=self.app_theme.primary_button,
		                             font=CTkFont(family="Poppins", size=14, weight="bold"),
		                             text_color=self.app_theme.primary_button_text, corner_radius=5,
		                             hover_color=scale_lightness(self.app_theme.primary_button, 0.95),
		                             width=70,
		                             command=self.__start_button)
		start_button.grid(row=0, column=0)

		stop_button = ctk.CTkButton(button_container, text="STOP", fg_color=self.app_theme.danger_button,
		                            font=CTkFont(family="Poppins", size=14, weight="bold"),
		                            text_color=self.app_theme.danger_button_text, corner_radius=5,
		                            hover_color=scale_lightness(self.app_theme.danger_button, 0.95),
		                            width=70,
		                            command=self.__stop_button)
		stop_button.grid(row=0, column=1)

		marker_button = ctk.CTkButton(button_container, text="📌", fg_color=self.app_theme.warning_button,
		                              text_color=self.app_theme.warning_button_text, corner_radius=5,
		                              hover_color=scale_lightness(self.app_theme.warning_button, 0.95),
		                              width=40,
		                              command=self.__marker_button)
		marker_button.grid(row=0, column=2)

		pass

	def __bottom_frame(self):
		# Sezione dati
		self.bottom_frame = ctk.CTkFrame(self, fg_color=self.app_theme.primary_background, corner_radius=0)
		self.bottom_frame.grid(row=1, column=0, sticky=ctk.NSEW)

		data_container = ctk.CTkFrame(self.bottom_frame, fg_color=self.app_theme.transparent, corner_radius=0)
		data_container.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))

		# Tab view dei dati e dei log
		tools_tabview = ctk.CTkTabview(data_container,
		                               fg_color=self.app_theme.transparent,
		                               text_color=(self.app_theme.light_gray_text, self.app_theme.primary_text),

		                               segmented_button_fg_color=self.app_theme.primary_background,
		                               segmented_button_selected_color=self.app_theme.primary_background,
		                               segmented_button_unselected_color=self.app_theme.primary_background,
		                               segmented_button_unselected_hover_color=self.app_theme.primary_background,
		                               segmented_button_selected_hover_color=self.app_theme.primary_background,
		                               corner_radius=5,
		                               anchor="w",

		                               )
		tabview_segmented_button: CTkSegmentedButton | None = tools_tabview.children.get("!ctksegmentedbutton")  # 🍆
		tabview_segmented_button.configure(
			font=CTkFont(family="Poppins", size=16, weight="bold")
		)
		tools_tabview.pack(side="top", fill="both", anchor="n", padx=30)
		data_tab = tools_tabview.add("Data")
		logs_tab = tools_tabview.add("Logs")
		tools_tabview.set("Data")

		# Dictionary to store canvas objects for each button
		button_underlines = {}

		def set_selected_underline(b: CTkButton):

			# Remove underline from all buttons by deleting the lines from the canvas
			for btn, canvas in button_underlines.items():
				if canvas:
					# Optionally hide the canvas or remove it from the grid to avoid overlap
					canvas.place_forget()

			# Create or retrieve the canvas for the underline for the selected button
			if b not in button_underlines:
				# Create the canvas only if it doesn't already exist for the selected button
				canvas = CTkCanvas(b, width=b.winfo_width(), height=4, highlightthickness=0)
				button_underlines[b] = canvas  # Store the canvas in the dictionary
			else:
				canvas = button_underlines[b]

			# Draw the underline (a line at the bottom of the button)
			canvas.create_line(0, 0, b.winfo_width(), 0, fill=self.app_theme.primary_text, width=4, capstyle="round")

			# Place the canvas just below the button
			canvas.place(x=0, y=b.winfo_height() - 4)

		# Bind the events to the buttons in the tabview
		for button in tools_tabview._segmented_button._buttons_dict.values():
			button.grid_configure(padx=(0, 40))

			# Change text color on hover
			button.bind("<Enter>", lambda e, i=button: i.configure(text_color=self.app_theme.secondary_text))
			button.bind("<Leave>", lambda e, i=button: i.configure(text_color=self.app_theme.primary_text))

			# Handle button click to set underline
			button.bind("<Button-1>", lambda e, i=button: set_selected_underline(i))

		loading_bar_container = ctk.CTkFrame(tabview_segmented_button, fg_color=self.app_theme.transparent,
		                                     corner_radius=0)
		loading_bar_container.grid(row=0, column=2, sticky="nswe")
		loading_bar = ctk.CTkProgressBar(loading_bar_container, corner_radius=5, width=400,
		                                 fg_color=self.app_theme.light_gray_text,
		                                 progress_color=self.app_theme.primary_text)
		loading_bar.pack(side="left", anchor="c")

		# Tabella dei log
		logs_frame = ctk.CTkFrame(logs_tab, fg_color=self.app_theme.element_background, corner_radius=5)
		logs_frame.pack(side="top", fill="both", expand=True)

		# Tabella dei dati
		table_frame = ctk.CTkFrame(master=data_tab, fg_color=self.app_theme.element_background,
		                           corner_radius=0)
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
		super().__init__(fg_color=app_theme.primary_background)
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

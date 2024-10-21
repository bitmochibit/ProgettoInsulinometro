import re
from ast import literal_eval
from tkinter import Widget, ttk, StringVar, IntVar
from typing import Union, Optional, Tuple, Callable, Any

import customtkinter as ctk
from CTkMenuBar import CTkTitleMenu
from PIL.ImageOps import expand

from customtkinter import CTkFrame, CTkImage, CTkEntry, CTkFont, CTkTabview, CTkButton, CTkSegmentedButton, CTkCanvas
import colorsys

import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots


# from tkfontawesome import icon_to_image


# from PIL import Image, ImageDraw, ImageFont


def clamp(value, min_val, max_val):
	if value <= min_val:
		return min_val
	elif value >= max_val:
		return max_val

	return value


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


def color_str_to_hex(color: str) -> int:
	return int(color[1:], 16)


# Classe estesa per il menu personalizzato, per qualche strano motivo quello di base supporta solo il testo 🍡
class ExtendedTitleMenu(CTkTitleMenu):
	def __init__(self,
	             master,
	             title_bar_color=0xFFFFFF,
	             padx: int = 10,
	             width: int = 10,
	             x_offset: int = None,
	             y_offset: int = None,
	             min_width: int = 800,
	             min_height: int = 600,
	             app_theme: AppTheme = AppTheme()
	             ):
		super().__init__(master, title_bar_color, padx, width, x_offset, y_offset)
		self.master.minsize(min_width, min_height)
		self.app_theme = app_theme

	def add_cascade(self, text=None, postcommand=None, hover_text_color=None, **kwargs) -> CTkButton:
		btn = super().add_cascade(text, postcommand, **kwargs)
		if hover_text_color is not None:
			btn.bind("<Enter>", lambda e, i=btn: i.configure(text_color=hover_text_color))
			btn.bind("<Leave>",
			         lambda e, i=btn, default_color=kwargs.get("text_color"): i.configure(text_color=default_color))
		return btn

	def add_frame(self, frame: CTkFrame):
		frame.grid(row=0, column=self.num, padx=(0, self.padding))


# Classe estesa per il tabview di customtkinter
class ExtendedTabView(CTkTabview):
	DEFAULT_UNDERLINE_WIDTH = 4
	DEFAULT_SELECTED_STYLE = None

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
	             segmented_button_background_corner_colors: Optional[Tuple[str, str, str, str]] = None,
	             segmented_button_height: Optional[int] = None,
	             segmented_button_width: Optional[int] = None,
	             segmented_button_padding_x: Union[float, Tuple[float, float]] = 0.0,
	             segmented_button_padding_y: Union[float, Tuple[float, float]] = 0.0,
	             segmented_button_sticky: Optional[str] = None,
	             segmented_button_row: Optional[int] = None,
	             segmented_button_column: Optional[int] = None,
	             button_padding_x: Union[float, Tuple[float, float]] = 0.0,
	             button_padding_y: Union[float, Tuple[float, float]] = 0.0,
	             selected_style: Optional[str] = None,
	             selected_style_color: Optional[str] = None,
	             underline_width: int = DEFAULT_UNDERLINE_WIDTH,
	             text_color: Optional[Union[str, Tuple[str, str]]] = None,
	             text_hover_color: Optional[str] = None,
	             text_color_unselected: Optional[str] = None,
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

		self.segmented_button: CTkSegmentedButton | None = self.children.get("!ctksegmentedbutton")
		self._app_theme = app_theme

		# Style and layout settings
		self._selected_style = selected_style or self.DEFAULT_SELECTED_STYLE
		self._selected_style_color = selected_style_color
		self._text_color = text_color
		self._text_color_unselected = text_color_unselected or text_color
		self._text_hover_color = text_hover_color
		self._underline_width = underline_width

		self._segmented_button_font = segmented_button_font
		self._segmented_button_background_corner_colors = segmented_button_background_corner_colors
		self._segmented_button_height = segmented_button_height
		self._segmented_button_width = segmented_button_width
		self._segmented_button_sticky = segmented_button_sticky
		self._segmented_button_row = segmented_button_row
		self._segmented_button_column = segmented_button_column

		# Button layout settings
		self._button_padding_x = button_padding_x
		self._button_padding_y = button_padding_y
		self._segmented_button_padding_x = segmented_button_padding_x
		self._segmented_button_padding_y = segmented_button_padding_y

		# Maintain button states and underlines
		self._button_underlines = {}
		self._binded_buttons = {}

		self._initialize_buttons()

	def _initialize_buttons(self):
		"""Initial setup for buttons and their event bindings."""
		if not self.segmented_button:
			return

		# Apply configuration for segmented button
		self.segmented_button.configure(
			font=self._segmented_button_font,
			background_corner_colors=self._segmented_button_background_corner_colors,
			height=self._segmented_button_height,
			width=self._segmented_button_width,
		)
		self.segmented_button.grid_configure(
			padx=self._segmented_button_padding_x,
			pady=self._segmented_button_padding_y,
			sticky=self._segmented_button_sticky,
			row=self._segmented_button_row,
			column=self._segmented_button_column
		)

		# Initialize each button in segmented button
		for button in self.segmented_button._buttons_dict.values():
			self._setup_button(button)

	def _setup_button(self, button: CTkButton):
		"""Setup button: bind events and style."""
		button.grid_configure(padx=self._button_padding_x, pady=self._button_padding_y)
		if button not in self._binded_buttons:
			self._bind_button_events(button)
			self._binded_buttons[button] = True
		self._update_button_style(button)
		self._apply_selected_style(button) if button.cget("text") == self._current_name else None

	def _bind_button_events(self, button: CTkButton):
		"""Bind hover and click events for a button."""
		button.bind("<Enter>",
		            lambda e: button.configure(text_color=self._text_hover_color) if self._text_hover_color else None)
		button.bind("<Leave>", lambda e: button.configure(text_color=self._get_button_text_color(button)))
		button.bind("<Button-1>", lambda e: self._on_button_click(button))

	def _on_button_click(self, button: CTkButton):
		"""Handle button click: apply selected style and update other buttons."""
		self._apply_selected_style(button)
		for btn in self._binded_buttons.keys():
			self._update_button_style(btn)

	def _apply_selected_style(self, button: CTkButton):
		"""Apply the selected style to the clicked button."""
		if self._selected_style == "underline":
			self._set_selected_underline(button)

	def _set_selected_underline(self, button: CTkButton):
		"""Set an underline for the selected button."""
		for btn, canvas in self._button_underlines.items():
			canvas.place_forget() if canvas else None  # Hide all underlines

		button.update_idletasks()

		canvas = self._button_underlines.get(button)
		if not canvas:
			canvas = CTkCanvas(button, width=button.winfo_reqwidth(), height=self._underline_width,
			                   highlightthickness=0)
			self._button_underlines[button] = canvas

		# Create and place underline
		canvas.delete("all")
		canvas.create_line(0, 0, button.winfo_reqwidth(), 0, fill=self._selected_style_color,
		                   width=self._underline_width, capstyle="round")
		canvas.place(x=0, y=button.winfo_reqheight() - self._underline_width)

	def _update_button_style(self, button: CTkButton):
		"""Update text color of the button based on selection."""
		is_selected = button.cget("text") == self._current_name
		button.configure(text_color=self._text_color if is_selected else self._text_color_unselected)

	def _get_button_text_color(self, button: CTkButton) -> str:
		"""Return appropriate text color for hover/leave events."""
		return self._text_color if button.cget("text") == self._current_name else self._text_color_unselected

	def add(self, text: str) -> CTkFrame:
		"""Add a new tab and update button styles."""
		frame = super().add(text)
		self._initialize_buttons()  # Ensure new buttons are properly initialized
		return frame

	def set(self, text: str):
		"""Set the currently selected tab."""
		super().set(text)
		self._initialize_buttons()


# Elementi

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
		             minvalue: Optional[int] = None,  # only for num var
		             maxvalue: Optional[int] = None,

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
			self.minvalue = minvalue
			self.maxvalue = maxvalue
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
		self._entry_options = entry_options
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
				curr_input = self.input.get()
				if type(self.current_input_variable) is IntVar:
					# remove all non numeric characters from curr_input
					try:
						int_input = int(curr_input or 0, 10)
					except:
						int_input = 0

					if self._entry_options.maxvalue is not None and self._entry_options.minvalue is not None:
						clamped_value = clamp(int_input, self._entry_options.minvalue, self._entry_options.maxvalue)
						self.current_input_variable.set(value=clamped_value)

				# self.current_input_variable.set(curr_input)

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

		menu = ExtendedTitleMenu(self, app_theme=self.app_theme,
		                         title_bar_color=color_str_to_hex(self.app_theme.element_background),
		                         y_offset=4,
		                         min_width=self._min_width,
		                         min_height=self._min_height
		                         )

		file_btn = menu.add_cascade("File",
		                            command=self.__file_button,
		                            font=CTkFont(family="Poppins", size=14, weight="bold"),
		                            text_color=self.app_theme.primary_text,
		                            hover_text_color=self.app_theme.secondary_text,
		                            fg_color=self.app_theme.element_background,
		                            bg_color=self.app_theme.transparent,
		                            hover_color=self.app_theme.element_background,
		                            corner_radius=0,
		                            )
		file_btn.grid_configure(padx=(0, 15))

		device_btn = menu.add_cascade("Device",
		                              command=self.__device_button,
		                              font=CTkFont(family="Poppins", size=14, weight="bold"),
		                              text_color=self.app_theme.primary_text,
		                              hover_text_color=self.app_theme.secondary_text,
		                              fg_color=self.app_theme.element_background,
		                              bg_color=self.app_theme.transparent,
		                              hover_color=self.app_theme.element_background,
		                              corner_radius=0,
		                              )

		device_btn.grid_configure(padx=(0, 30))
		signal_btn = menu.add_cascade("📶",
		                              command=self.__signal_button,
		                              text_color=self.app_theme.primary_text,
		                              fg_color=self.app_theme.element_background,
		                              bg_color=self.app_theme.transparent,
		                              hover_color=self.app_theme.element_background,
		                              corner_radius=0,
		                              # image=icon_to_image("wifi", scale_to_width=14, fill=self.app_theme.primary_text)
		                              )

		battery_btn = menu.add_cascade("🔋",
		                               command=self.__battery_button,
		                               text_color=self.app_theme.primary_text,
		                               fg_color=self.app_theme.element_background,
		                               bg_color=self.app_theme.transparent,
		                               hover_color=self.app_theme.element_background,
		                               corner_radius=0,
		                               # image=icon_to_image("battery-full", scale_to_width=14, fill=self.app_theme.primary_text)
		                               )

	def __main_frame(self):
		self.main_frame = ctk.CTkFrame(self, fg_color=self.app_theme.secondary_background, corner_radius=0)
		self.main_frame.grid(row=1, column=0, sticky=ctk.NSEW)
		# Sezione dei grafici e dei controlli
		graph_section = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
		graph_section.pack(side="top", fill="both", padx=10, pady=25)

		graph_section.columnconfigure(0, weight=1)
		graph_section.columnconfigure(1, weight=1)
		graph_section.columnconfigure(2, weight=3)

		graph_section.rowconfigure(0, weight=1)
		graph_section.rowconfigure(1, weight=1)

		# Grafici
		bode1_frame = ctk.CTkFrame(graph_section, fg_color=self.app_theme.element_background, corner_radius=5)
		bode1_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky=ctk.NSEW)

		bode1_fig = plt.figure.Figure(dpi=72)
		ax = bode1_fig.subplots()

		bode1_graph = FigureCanvasTkAgg(bode1_fig, bode1_frame)
		bode1_graph.draw()

		bode1_graph.get_tk_widget().pack(side="top", fill="both", padx=2, pady=2)

		bode2_frame = ctk.CTkFrame(graph_section, fg_color=self.app_theme.element_background, corner_radius=5)
		bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)

		bode2_fig = plt.figure.Figure(dpi=72)
		ax = bode2_fig.add_subplot()

		bode2_graph = FigureCanvasTkAgg(bode2_fig, bode2_frame)
		bode2_graph.draw()
		bode2_graph.get_tk_widget().pack(side="top", fill="both", padx=2, pady=2)

		nyquist_frame = ctk.CTkFrame(graph_section, fg_color=self.app_theme.element_background, corner_radius=5)
		nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)

		nyquist_fig = plt.figure.Figure(dpi=72)
		ax = nyquist_fig.subplots()

		nyquist_graph = FigureCanvasTkAgg(nyquist_fig, nyquist_frame)
		nyquist_graph.draw()
		nyquist_graph.get_tk_widget().pack(side="top", fill="both", padx=2, pady=2)

		# Sezione dei controlli
		# Suddivisione finestra
		graph_controls_container = ctk.CTkFrame(graph_section, fg_color=self.app_theme.transparent,
		                                        corner_radius=5)
		graph_controls_container.grid(row=0, column=3, sticky=ctk.NSEW, rowspan=2)

		# Tab view dei controlli (Fixed, Sweep)
		measurement_mode_tabview = ExtendedTabView(graph_controls_container,
		                                           fg_color=self.app_theme.element_background,
		                                           text_color=(
			                                           self.app_theme.light_gray_text, self.app_theme.primary_text),
		                                           text_color_unselected=self.app_theme.gray_text,
		                                           width=250,
		                                           height=0,
		                                           segmented_button_fg_color=self.app_theme.element_secondary_background,
		                                           segmented_button_selected_color=scale_lightness(
			                                           self.app_theme.element_secondary_background, 0.96),
		                                           segmented_button_unselected_color=self.app_theme.element_secondary_background,
		                                           segmented_button_unselected_hover_color=scale_lightness(
			                                           self.app_theme.element_secondary_background, 0.95),
		                                           segmented_button_selected_hover_color=scale_lightness(
			                                           self.app_theme.element_secondary_background, 0.96),
		                                           segmented_button_font=CTkFont(family="Poppins", size=16,
		                                                                         weight="bold"),
		                                           segmented_button_background_corner_colors=(
			                                           self.app_theme.secondary_background,
			                                           self.app_theme.secondary_background,
			                                           self.app_theme.element_secondary_background,
			                                           self.app_theme.element_secondary_background
		                                           ),
		                                           segmented_button_height=40,
		                                           segmented_button_padding_x=(0, 0),
		                                           segmented_button_padding_y=(0, 0),

		                                           segmented_button_sticky="news",
		                                           segmented_button_row=0,

		                                           corner_radius=5,
		                                           border_width=0,
		                                           anchor="n"
		                                           )
		measurement_mode_tabview.pack(side="top", fill="both", expand=True)

		fixed_tab = measurement_mode_tabview.add("Fixed")
		sweep_tab = measurement_mode_tabview.add("Sweep")
		measurement_mode_tabview.set("Fixed")  # settata tab di default

		# Finestre di input - Fixed
		fixed_input_container = ctk.CTkFrame(fixed_tab, fg_color=self.app_theme.element_background, corner_radius=5)
		fixed_input_container.pack(side="top", fill="both")

		text_fixed_input = LabelledInput(fixed_input_container,
		                                 entry_options=LabelledInput.EntryOptions(
			                                 textvariable=self.fixed_test_string,
			                                 placeholder_text="Test (Ohm)",
			                                 minvalue=1,
			                                 maxvalue=500
		                                 ),
		                                 label_options=LabelledInput.LabelOptions(
			                                 text="Test"
		                                 ),
		                                 app_theme=self.app_theme
		                                 )
		text_fixed_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_input = LabelledInput(fixed_input_container,
		                                entry_options=LabelledInput.EntryOptions(
			                                textvariable=self.fixed_frequency_string,
			                                placeholder_text="Frequenza (Hz)",
		                                ),
		                                label_options=LabelledInput.LabelOptions(
			                                text="Frequenza",
		                                ),
		                                app_theme=self.app_theme
		                                )
		frequency_input.pack(side="top", fill="x", padx=5, pady=5)

		fixed_magnitude_input = LabelledInput(fixed_input_container,
		                                      entry_options=LabelledInput.EntryOptions(
			                                      textvariable=self.fixed_magnitude_string,
			                                      placeholder_text="Ampiezza (mV)",
		                                      ),
		                                      label_options=LabelledInput.LabelOptions(
			                                      text="Ampiezza",
		                                      ),
		                                      app_theme=self.app_theme
		                                      )
		fixed_magnitude_input.pack(side="top", fill="x", padx=5, pady=5)

		# Finestre di input - Sweep
		sweep_input_container = ctk.CTkScrollableFrame(sweep_tab, fg_color=self.app_theme.element_background,
		                                               corner_radius=5,
		                                               scrollbar_button_color=self.app_theme.light_gray_text,
		                                               scrollbar_button_hover_color=scale_lightness(
			                                               self.app_theme.light_gray_text, 0.94))
		sweep_input_container.pack(side="top", fill="both", expand=True)

		text_sweep_input = LabelledInput(sweep_input_container,
		                                 entry_options=LabelledInput.EntryOptions(
			                                 textvariable=self.sweep_test_string,
			                                 placeholder_text="Test (Ohm)"
		                                 ),
		                                 label_options=LabelledInput.LabelOptions(
			                                 text="Test"
		                                 ),
		                                 app_theme=self.app_theme
		                                 )
		text_sweep_input.pack(side="top", fill="x", padx=5, pady=5)

		sweep_magnitude_input = LabelledInput(sweep_input_container,
		                                      entry_options=LabelledInput.EntryOptions(
			                                      textvariable=self.sweep_magnitude_string,
			                                      placeholder_text="Ampiezza (mV)",
		                                      ),
		                                      label_options=LabelledInput.LabelOptions(
			                                      text="Ampiezza",
		                                      ),
		                                      app_theme=self.app_theme
		                                      )
		sweep_magnitude_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_start_input = LabelledInput(sweep_input_container,
		                                      entry_options=LabelledInput.EntryOptions(
			                                      textvariable=self.frequency_start_string,
			                                      placeholder_text="Frequenza (Hz)",
		                                      ),
		                                      label_options=LabelledInput.LabelOptions(
			                                      text="Frequenza iniziale",
		                                      ),
		                                      app_theme=self.app_theme
		                                      )
		frequency_start_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_end_input = LabelledInput(sweep_input_container,
		                                    entry_options=LabelledInput.EntryOptions(
			                                    textvariable=self.frequency_end_string,
			                                    placeholder_text="Frequenza (Hz)",
		                                    ),
		                                    label_options=LabelledInput.LabelOptions(
			                                    text="Frequenza finale",
		                                    ),
		                                    app_theme=self.app_theme
		                                    )
		frequency_end_input.pack(side="top", fill="x", padx=5, pady=5)

		points_number_input = LabelledInput(sweep_input_container,
		                                    entry_options=LabelledInput.EntryOptions(
			                                    textvariable=self.points_number,
			                                    placeholder_text="Numero di punti",
		                                    ),
		                                    label_options=LabelledInput.LabelOptions(
			                                    text="Numero di punti",
		                                    ),
		                                    app_theme=self.app_theme
		                                    )
		points_number_input.pack(side="top", fill="x", padx=5, pady=5)

		cycles_number_input = LabelledInput(sweep_input_container,
		                                    entry_options=LabelledInput.EntryOptions(
			                                    textvariable=self.cycles_number,
			                                    placeholder_text="Numero di cicli",
		                                    ),
		                                    label_options=LabelledInput.LabelOptions(
			                                    text="Numero di cicli",
		                                    ),
		                                    app_theme=self.app_theme
		                                    )
		cycles_number_input.pack(side="top", fill="x", padx=5, pady=5)

		# Pulsanti di controllo
		controls_section = ctk.CTkFrame(graph_controls_container, fg_color=self.app_theme.element_background,
		                                corner_radius=5)
		controls_section.pack(fill="both")

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

		marker_button = ctk.CTkButton(button_container, text="⫯", fg_color=self.app_theme.warning_button,
		                              font=CTkFont(family="Poppins", size=19),
		                              text_color=self.app_theme.warning_button_text, corner_radius=5,
		                              hover_color=scale_lightness(self.app_theme.warning_button, 0.95),
		                              width=40,
		                              # image=icon_to_image("map-pin", scale_to_width=8, fill=self.app_theme.warning_button_text),
		                              command=self.__marker_button)
		marker_button.grid(row=0, column=2)

		pass

	def __bottom_frame(self):
		# Sezione dati
		self.bottom_frame = ctk.CTkFrame(self, fg_color=self.app_theme.primary_background, corner_radius=0)
		self.bottom_frame.grid(row=2, column=0, sticky=ctk.NSEW)

		bottom_container = ctk.CTkFrame(self.bottom_frame, fg_color=self.app_theme.transparent, corner_radius=0)
		bottom_container.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))

		# Tab view dei dati e dei log
		tools_tabview = ExtendedTabView(bottom_container,
		                                fg_color=self.app_theme.transparent,
		                                text_color=(self.app_theme.light_gray_text, self.app_theme.primary_text),
		                                text_color_unselected=self.app_theme.gray_text,
		                                text_hover_color=self.app_theme.secondary_text,
		                                segmented_button_fg_color=self.app_theme.primary_background,
		                                segmented_button_selected_color=self.app_theme.primary_background,
		                                segmented_button_unselected_color=self.app_theme.primary_background,
		                                segmented_button_unselected_hover_color=self.app_theme.primary_background,
		                                segmented_button_selected_hover_color=self.app_theme.primary_background,
		                                segmented_button_font=CTkFont(family="Poppins", size=16, weight="bold"),
		                                corner_radius=5,
		                                button_padding_x=(0, 50),
		                                selected_style="underline",
		                                selected_style_color=self.app_theme.primary_text,
		                                anchor="w",
		                                )
		tools_tabview.pack(side="top", fill="both", anchor="n", padx=30)
		data_tab = tools_tabview.add("Data")
		logs_tab = tools_tabview.add("Logs")
		tools_tabview.set("Data")

		loading_bar_container = ctk.CTkFrame(tools_tabview.segmented_button, fg_color=self.app_theme.transparent,
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
		                           corner_radius=5)
		table_frame.pack(side="top", fill="both", expand=True)

		treeview_style = ttk.Style()
		treeview_style.theme_use('default')
		treeview_style.configure("data.Treeview",
		                         background=self.app_theme.element_background,
		                         foreground=self.app_theme.secondary_text,
		                         borderwidth=0,
		                         font=CTkFont(family="Poppins", size=14, weight="bold")
		                         )

		treeview_style.configure("data.Treeview.Heading",
		                         background=self.app_theme.element_background,
		                         foreground=self.app_theme.primary_text,
		                         fieldbackground="cyan",
		                         borderwidth=0,
		                         font=CTkFont(family="Poppins", size=14, weight="bold")
		                         )

		area = ("Frequenza", "Fase", "Ampiezza")

		data_table = ttk.Treeview(table_frame, columns=area, show='headings', height=7, style='data.Treeview')
		for i in range(3):
			data_table.column(i, width=70, anchor='c')
			data_table.heading(i, text=area[i])
		for i in range(10):
			data_table.insert('', -1, i, values=("data1 " + str(i), "data2 " + str(i), "data3 " + str(i)))

		data_table.pack(side="top", fill="both", padx=2, pady=2)
		pass

	def __init__(self, app_theme: AppTheme = AppTheme()):
		super().__init__(fg_color=app_theme.primary_background)
		self.app_theme = app_theme
		self.geometry("800x600")
		self.title("")
		self.minsize(800, 600)

		self.fixed_test_string = ctk.IntVar()
		self.sweep_test_string = ctk.StringVar()

		self.fixed_frequency_string = ctk.StringVar()
		self.fixed_magnitude_string = ctk.StringVar()

		self.sweep_magnitude_string = ctk.StringVar()
		self.frequency_start_string = ctk.StringVar()
		self.frequency_end_string = ctk.StringVar()
		self.points_number = ctk.StringVar()
		self.cycles_number = ctk.StringVar()

		# Suddivisione griglia layout finestra
		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=2)
		self.rowconfigure(2, weight=1)

		self.columnconfigure(0, weight=1)

		# Creazione finestre

		self.__title_menu()
		self.__main_frame()
		self.__bottom_frame()

	# Funzioni dei pulsanti
	def __start_button(self):
		print(f"Test: {self.fixed_test_string.get()}")

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

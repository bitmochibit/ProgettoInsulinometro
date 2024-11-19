from tkinter import ttk
from typing import Optional

import customtkinter as ctk
import matplotlib as plt
import scipy.signal as signal
from customtkinter import CTkFont
from eventpy.eventdispatcher import EventDispatcher
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import figure

from app.device.DeviceWindow import DeviceWindow
from app.events.ApplicationMessagesEnum import ApplicationMessagesEnum
from app.templates.CustomTabView import CustomTabView
from app.templates.CustomTitleMenu import CustomTitleMenu
from app.templates.LabelledInput import LabelledInput
from app.utils.Color import color_str_to_hex, scale_lightness
from backend import Client

from theme.AppTheme import AppTheme


class MainApplication(ctk.CTk):

	def __title_menu(self):
		menu = CustomTitleMenu(self, app_theme=self.app_theme,
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

		plt.pyplot.style.use('seaborn-v0_8')

		self.bode1_graph = figure(dpi=72)
		self.bode1_graph.subplots_adjust(top=0.9, bottom=0.2)
		bode1_ax = self.bode1_graph.add_subplot(ylabel="Ampiezza")
		bode1_ax.grid(False)
		bode1_ax.set_title("Diagramma di Bode")

		bode1_renderer = FigureCanvasTkAgg(self.bode1_graph, bode1_frame)
		bode1_renderer.draw()
		bode1_renderer.get_tk_widget().pack(anchor='c', fill="both", padx=2, pady=2, expand=True)

		bode2_frame = ctk.CTkFrame(graph_section, fg_color=self.app_theme.element_background, corner_radius=5)
		bode2_frame.grid(row=1, column=0, padx=(0, 5), sticky=ctk.NSEW)

		self.bode2_graph = plt.figure.Figure(dpi=72)
		self.bode2_graph.subplots_adjust(top=0.9, bottom=0.2)
		bode2_ax = self.bode2_graph.add_subplot(ylabel="Fase", xlabel="Frequenza")

		bode2_graph = FigureCanvasTkAgg(self.bode2_graph, bode2_frame)
		bode2_graph.draw()
		bode2_graph.get_tk_widget().pack(anchor='c', fill="both", padx=2, pady=2, expand=True)

		nyquist_frame = ctk.CTkFrame(graph_section, fg_color=self.app_theme.element_background, corner_radius=5)
		nyquist_frame.grid(row=0, column=1, rowspan=2, columnspan=2, padx=(0, 5), sticky=ctk.NSEW)

		self.nyquist_graph = plt.figure.Figure(dpi=72)
		self.nyquist_graph.subplots_adjust(left=0.18, right=0.9)

		nyquist_ax = self.nyquist_graph.add_subplot(xlabel="Reale", ylabel="Immaginario")
		nyquist_ax.set_title("Diagramma di Nyquist")

		# Placeholder nyquist transfer function plot
		num = [1, 1]
		den = [1, 2, 2]
		system = signal.TransferFunction(num, den)
		w, H = signal.freqresp(system)

		nyquist_ax.plot(H.real, H.imag, 'b', label='H(s) Imaginary +')
		nyquist_ax.plot(H.real, -H.imag, 'r', label='H(s) Imaginary -')

		nyquist_graph = FigureCanvasTkAgg(self.nyquist_graph, nyquist_frame)
		nyquist_graph.draw()
		nyquist_graph.get_tk_widget().pack(anchor='c', fill="both", padx=2, pady=2, expand=True)

		# Sezione dei controlli
		# Suddivisione finestra
		graph_controls_container = ctk.CTkFrame(graph_section, fg_color=self.app_theme.transparent,
												corner_radius=5)
		graph_controls_container.grid(row=0, column=3, sticky=ctk.NSEW, rowspan=2)

		# Tab view dei controlli (Fixed, Sweep)
		measurement_mode_tabview = CustomTabView(graph_controls_container,
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

		self.test_ohm_input = LabelledInput(fixed_input_container,
											entry_options=LabelledInput.EntryOptions(
												textvariable=self.fixed_test_string,
												placeholder_text="Test (Ohm)",
												border_width=1,
												border_color=self.app_theme.light_gray_text,
												minvalue=1,
												maxvalue=500,
												type="number"
											),
											label_options=LabelledInput.LabelOptions(
												text_color=self.app_theme.secondary_text,
												font=CTkFont(family="Poppins", size=12, weight="bold"),
												text="Test value (Ohm)"
											),
											app_theme=self.app_theme
											)
		self.test_ohm_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_input = LabelledInput(fixed_input_container,
										entry_options=LabelledInput.EntryOptions(
											textvariable=self.fixed_frequency_string,
											placeholder_text="Frequenza (Hz)",
											border_width=1,
											border_color=self.app_theme.light_gray_text,
											type="number"
										),
										label_options=LabelledInput.LabelOptions(
											text_color=self.app_theme.secondary_text,
											font=CTkFont(family="Poppins", size=12, weight="bold"),
											text="Frequenza",
										),
										app_theme=self.app_theme
										)
		frequency_input.pack(side="top", fill="x", padx=5, pady=5)

		fixed_magnitude_input = LabelledInput(fixed_input_container,
											  entry_options=LabelledInput.EntryOptions(
												  textvariable=self.fixed_magnitude_string,
												  placeholder_text="Ampiezza (mV)",
												  border_width=1,
												  border_color=self.app_theme.light_gray_text,
												  type="number"
											  ),
											  label_options=LabelledInput.LabelOptions(
												  text_color=self.app_theme.secondary_text,
												  font=CTkFont(family="Poppins", size=12, weight="bold"),
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
											 placeholder_text="Test (Ohm)",
											 border_width=1,
											 border_color=self.app_theme.light_gray_text,
											 type="number"
										 ),
										 label_options=LabelledInput.LabelOptions(
											 text_color=self.app_theme.secondary_text,
											 font=CTkFont(family="Poppins", size=12, weight="bold"),
											 text="Test"
										 ),
										 app_theme=self.app_theme
										 )
		text_sweep_input.pack(side="top", fill="x", padx=5, pady=5)

		sweep_magnitude_input = LabelledInput(sweep_input_container,
											  entry_options=LabelledInput.EntryOptions(
												  textvariable=self.sweep_magnitude_string,
												  placeholder_text="Ampiezza (mV)",
												  border_width=1,
												  border_color=self.app_theme.light_gray_text,
												  type="number"
											  ),
											  label_options=LabelledInput.LabelOptions(
												  text_color=self.app_theme.secondary_text,
												  font=CTkFont(family="Poppins", size=12, weight="bold"),
												  text="Ampiezza",
											  ),
											  app_theme=self.app_theme
											  )
		sweep_magnitude_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_start_input = LabelledInput(sweep_input_container,
											  entry_options=LabelledInput.EntryOptions(
												  textvariable=self.frequency_start_string,
												  placeholder_text="Frequenza (Hz)",
												  border_width=1,
												  border_color=self.app_theme.light_gray_text,
												  type="number"
											  ),
											  label_options=LabelledInput.LabelOptions(
												  text_color=self.app_theme.secondary_text,
												  font=CTkFont(family="Poppins", size=12, weight="bold"),
												  text="Frequenza iniziale",
											  ),
											  app_theme=self.app_theme
											  )
		frequency_start_input.pack(side="top", fill="x", padx=5, pady=5)

		frequency_end_input = LabelledInput(sweep_input_container,
											entry_options=LabelledInput.EntryOptions(
												textvariable=self.frequency_end_string,
												placeholder_text="Frequenza (Hz)",
												border_width=1,
												border_color=self.app_theme.light_gray_text,
												type="number"
											),
											label_options=LabelledInput.LabelOptions(
												text_color=self.app_theme.secondary_text,
												font=CTkFont(family="Poppins", size=12, weight="bold"),
												text="Frequenza finale",
											),
											app_theme=self.app_theme
											)
		frequency_end_input.pack(side="top", fill="x", padx=5, pady=5)

		points_number_input = LabelledInput(sweep_input_container,
											entry_options=LabelledInput.EntryOptions(
												textvariable=self.points_number,
												placeholder_text="Numero di punti",
												border_width=1,
												border_color=self.app_theme.light_gray_text,
												type="number"
											),
											label_options=LabelledInput.LabelOptions(
												text_color=self.app_theme.secondary_text,
												font=CTkFont(family="Poppins", size=12, weight="bold"),
												text="Numero di punti",
											),
											app_theme=self.app_theme
											)
		points_number_input.pack(side="top", fill="x", padx=5, pady=5)

		cycles_number_input = LabelledInput(sweep_input_container,
											entry_options=LabelledInput.EntryOptions(
												textvariable=self.cycles_number,
												placeholder_text="Numero di cicli",
												border_width=1,
												border_color=self.app_theme.light_gray_text,
												type="number"
											),
											label_options=LabelledInput.LabelOptions(
												text_color=self.app_theme.secondary_text,
												font = CTkFont(family="Poppins", size=12, weight="bold"),
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
		tools_tabview = CustomTabView(bottom_container,
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
		table_frame.pack(side="top", fill="both")

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

		area = ("Ascissa", "Ordinata")

		self.data_table = ttk.Treeview(table_frame, columns=area, show='headings', style='data.Treeview')
		for i in range(2):
			self.data_table.column(i, width=70, anchor='c')
			self.data_table.heading(i, text=area[i])

		self.data_table.pack(side="top", fill="both", padx=2, pady=2, expand=True)
		pass

	def __init__(self, app_theme: AppTheme = AppTheme()):
		super().__init__(fg_color=app_theme.primary_background)
		self.app_theme = app_theme
		self.geometry("1000x650")
		self.title("")
		self.minsize(800, 600)

		self.application_message_dispatcher = EventDispatcher()
		self.__setup_listeners()

		self.client = Client()

		self.fixed_test_string = ctk.IntVar(value=1)
		self.sweep_test_string = ctk.StringVar()

		self.fixed_frequency_string = ctk.StringVar()
		self.fixed_magnitude_string = ctk.StringVar()

		self.sweep_magnitude_string = ctk.StringVar()
		self.frequency_start_string = ctk.StringVar()
		self.frequency_end_string = ctk.StringVar()
		self.points_number = ctk.StringVar()
		self.cycles_number = ctk.StringVar()

		self.updating_values = False

		# self.graph_yvalues = []
		# self.graph_xvalues = []

		self.graph_values = []

		# Suddivisione griglia layout finestra
		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=2)
		self.rowconfigure(2, weight=1)

		self.columnconfigure(0, weight=1)

		# Creazione finestre

		self.toplevel_window: Optional[DeviceWindow] = None
		self.__title_menu()
		self.__main_frame()
		self.__bottom_frame()

	def __setup_listeners(self):
		self.application_message_dispatcher.appendListener(ApplicationMessagesEnum.START_VALUE_READER, self.start_value_reader)
		self.application_message_dispatcher.appendListener(ApplicationMessagesEnum.STOP_VALUE_READER, self.stop_value_reader)
		pass

	def _update_graph_value(self, figure: Figure):
		axs = figure.get_axes()
		x_values = [xval[0] for xval in self.graph_values]
		y_values = [yval[1] for yval in self.graph_values]
		axs[0].plot(x_values, y_values, color='blue', marker='o')
		figure.canvas.draw()

	# self.bode1_fig.canvas.flush_events()

	def _add_table_value(self, x, y):
		self.data_table.insert('', -1, values=(x, y))

	def add_graph_value(self, x, y):
		self.graph_values.append((x, y))
		self._update_graph_value(self.bode1_graph)
		self._update_graph_value(self.bode2_graph)
		self._add_table_value(x, y)

	# Funzioni dei pulsanti
	def __start_button(self):
		self.test_ohm_input.validate()
		self.add_graph_value(len(self.graph_values), self.fixed_test_string.get())

	def __stop_button(self):
		pass

	def __marker_button(self):
		print("marker button")

	def __logs_button(self):
		print("logs button")

	def __data_button(self):
		print("data button")

	def __file_button(self):
		print("file button")

	def __device_button(self):
		if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
			self.toplevel_window = DeviceWindow(self, self.client, self.application_message_dispatcher, self.app_theme)
		elif self.toplevel_window.state() == "iconic":
			self.toplevel_window.deiconify()
			self.toplevel_window.focus()

	def __battery_button(self):
		print("battery button")

	def __signal_button(self):
		print("signal button")

	def __fixed_button(self):
		print("fixed button")

	def __sweep_button(self):
		print("sweep button")

	def start_value_reader(self):
		print("Starting value reader")
		self.updating_values = True
		self.__read_value_from_device()
		pass

	def stop_value_reader(self):
		print("Stopping value reader")
		self.updating_values = False
		pass

	def __read_value_from_device(self):
		# Read value from device
		try:
			self.client.read_data("51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B".lower(), self.__on_data_read)
		except Exception as e:
			print(e)
			self.updating_values = False

		# Schedule the read value function every 1 second
		if self.updating_values:
			self.after(1000, self.__read_value_from_device)

	def __on_data_read(self, data, error):
		# Data is a string like "x,y", where x and y are the values to plot
		#Convert bytearray (data) to str
		string_data = data.decode("utf-8")

		split_data = string_data.split(",")
		x = split_data[0]
		y = split_data[1]

		self.add_graph_value(x, y)

		pass



if __name__ == "__main__":
	application = MainApplication(AppTheme())
	application.mainloop()

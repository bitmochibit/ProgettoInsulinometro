from typing import Optional, Union, Tuple

import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont

from app.theme.AppTheme import AppTheme

class SearchBar(CTkEntry):
	def __init__(self,
				 master,
				 width: int = 140,
				 height: int = 28,
				 corner_radius: Optional[int] = 0,
				 border_width: Optional[int] = 0,

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
		super().__init__(master, **kwargs)
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

		self.container = ctk.CTkFrame(master, fg_color="transparent", **kwargs)
		self.input = ctk.CTkEntry(self.container,
								  width=self.width,
								  height=self.height,
								  corner_radius=self.corner_radius,
								  border_width=self.border_width,
								  bg_color=self.bg_color,
								  fg_color=self.fg_color,
								  border_color=self.border_color,
								  text_color=self.text_color,
								  placeholder_text_color=self.placeholder_text_color,
								  textvariable=self.textvariable,
								  placeholder_text=self.placeholder_text,
								  font=self.font,
								  state=self.state,
								  **self.kwargs)
		self.input.pack(side=ctk.TOP, fill=ctk.BOTH)

		if self.textvariable is not None:
			# Aggiungi un listener all'input per aggiornare il valore della textvariable (devo fare cosi' per forza perche' senno' sparisce il placeholder)
			def update_variable(e):
				curr_input = self.input.get()
				self.textvariable.set(curr_input)

			self.input.bind("<KeyRelease>", update_variable)

	# Metodi della classe per posizionare il self.container
	def pack(self, **kwargs):
		self.container.pack(**kwargs)

	def grid(self, **kwargs):
		self.container.grid(**kwargs)

	def place(self, **kwargs):
		self.container.place(**kwargs)

	def get(self):
		return self.input.get()

	def bind_input(self, sequence=None, command=None, add=True):
		self.input.bind(sequence, command, add)
from typing import Optional, Union, Tuple

import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont

from app.theme.AppTheme import AppTheme

class SearchBar(CTkEntry):
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


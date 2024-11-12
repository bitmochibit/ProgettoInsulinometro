from typing import Any

from CTkMenuBar import CTkTitleMenu
import customtkinter as ctk
from customtkinter import CTkButton, CTkFrame

from app.theme.AppTheme import AppTheme


class CustomTitleMenu(CTkTitleMenu):
    def __init__(self,
                 master: ctk.CTk | Any,
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
        master.minsize(min_width, min_height)
        self.app_theme = app_theme

    def add_cascade(self, text=None, postcommand=None, hover_text_color=None, **kwargs) -> CTkButton:
        btn = super().add_cascade(text, postcommand, **kwargs)
        if hover_text_color is not None:
            btn.bind("<Enter>", lambda e, i=btn: i.configure(text_color=hover_text_color))
            btn.bind("<Leave>",
                     lambda e, i=btn, default_color=kwargs.get("text_color"): i.configure(text_color=default_color))
        return btn

    def add_frame(self, frame: CTkFrame) -> CTkFrame:
        frame.grid(row=0, column=self.num, padx=(0, self.padding))
        return frame

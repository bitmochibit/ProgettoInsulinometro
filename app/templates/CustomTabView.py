from typing import Any, Optional, Tuple, Union, Callable

from customtkinter import CTkTabview, CTkSegmentedButton, CTkButton, CTkCanvas, CTkFrame, CTkFont

from app.theme.AppTheme import AppTheme


class CustomTabView(CTkTabview):
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

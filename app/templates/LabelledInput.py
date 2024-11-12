from typing import Union, Optional, Tuple

import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkImage

from app.theme.AppTheme import AppTheme


class LabelledInput(CTkEntry):
    class EntryOptions:
        ENTRY_TYPE = Union["text", "number"]

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

                     type: ENTRY_TYPE = "text",

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
            self.type = type
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

    def _validate_digit(self, P):
        if str.isdigit(P):
            return True
        return False

    def _validate_range(self, P):
        # If the input is an empty string, return True
        if not self._validate_digit(P):
            return False

        # Try to convert the input to an integer, if it fails, return False
        try:
            int_input = int(P)
        except ValueError:
            return False

        # Retrieve minvalue and maxvalue from entry options
        minval = self._entry_options.minvalue
        maxval = self._entry_options.maxvalue

        # If both min and max are None, any integer is valid
        if minval is None and maxval is None:
            self._last_valid_value = P  # Update last valid value
            return True

        # If both minvalue and maxvalue are defined, check if the input is within the range
        if minval is not None and maxval is not None:
            if minval <= int_input <= maxval:
                self._last_valid_value = P  # Update last valid value
                return True
            return False

        # If only minvalue is defined, check that the input is greater or equal to minvalue
        if minval is not None:
            if int_input >= minval:
                self._last_valid_value = P  # Update last valid value
                return True
            return False

        # If only maxvalue is defined, check that the input is less or equal to maxvalue
        if maxval is not None:
            if int_input <= maxval:
                self._last_valid_value = P  # Update last valid value
                return True
            return False

        return False

    def _revert_to_last_valid(self):
        # This function is called if validation fails, and restores the last valid value
        valid_value = self._last_valid_value or self._entry_options.minvalue or 0
        self.input.delete(0, "end")
        self.input.insert(0, valid_value)
        self.current_input_variable.set(valid_value)

    def validate(self):
        # Validate the current input
        if self._entry_options.type == "number":
            if not self._validate_range(self.input.get()):
                self._revert_to_last_valid()

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
        self._last_valid_value = None
        if self._entry_options.maxvalue is not None or self._entry_options.minvalue is not None and self._entry_options.type == "number":
            validate_ra = (self.register(self._validate_range))
            invalid_ra = (self.register(self._revert_to_last_valid))
            self.input.configure(validate="focusout",
                                 validatecommand=(validate_ra, "%P"))  # %P = valore attuale dell'entry
            self.input._entry.configure(invalidcommand=invalid_ra)

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
                self.current_input_variable.set(curr_input)

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

from dataclasses import dataclass


@dataclass
class AppTheme:
    transparent: str = "transparent"

    primary_background: str = "#F9F8FD"
    secondary_background: str = "#F1F2F7"
    element_background: str = "#FFFFFF"
    element_secondary_background: str = "#F3EDF7"

    primary_text: str = "#1D1E4D"
    secondary_text: str = "#535178"
    light_text: str = "#FFFFFF"
    gray_text: str = "#434242"
    light_gray_text: str = "#CAC4D0"

    primary_button: str = "#EBFFFC"
    primary_button_text: str = "#003830"

    warning_button: str = "#FFF9EB"
    warning_button_text: str = "#422E00"

    danger_button: str = "#FFEBEF"
    danger_button_text: str = "#800019"

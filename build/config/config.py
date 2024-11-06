# config.py

BG_COLOR_DARK = '#2b2b2b'
BG_COLOR_LIGHT = '#FFFFFF'
class Config:

    selected_file_path = None
    last_save_path = None 
    appearance_mode = "dark"  # Default to dark mode
    theme = "green"  # Default theme
# You can extend this class with more configuration options if needed
    def _update_label_colors():
        appearance_mode = Config.appearance_mode # Get the appearance mode
        if appearance_mode == "dark":
            return "white", "white", "gray"  # Dark mode colors
        else:
            return "black", "black", "gray"  # Light mode colors

    def get_dynamic_bg_color():
        if Config.appearance_mode == 'dark':
            return BG_COLOR_DARK
        else:
            return BG_COLOR_LIGHT
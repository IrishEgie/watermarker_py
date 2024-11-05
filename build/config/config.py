# config.py
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
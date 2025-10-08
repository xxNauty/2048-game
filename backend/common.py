def get_geometry(previous_window, width, height):
    if width < 440:
        width = 440

    if height < 600:
        height = 600

    screen_width = previous_window.winfo_screenwidth()
    screen_height = previous_window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    return f"{width}x{height}+{x}+{y}"

def unhide_previous_window(previous_window, current_window):
    previous_window.deiconify()
    current_window.destroy()
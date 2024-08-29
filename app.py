import time
import psutil
import platform
import cpuinfo
import customtkinter as ctk
import threading

ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"

cpu_info = cpuinfo.get_cpu_info()

def Center_Window(screen: ctk, width: int, height: int, scale_factor: float = 1.0):
    # centers the window to open center of main screen
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2))* scale_factor)
    y = int(((screen_height/2)-(height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

def fetch_system_info():
        # Fetchs cpu and memory usage
        cpu_usage = psutil.cpu_percent(interval = 0.5, percpu = False)
        mem_info = psutil.virtual_memory()
        total_memory = mem_info.total / 1024 / 1024 / 1024
        mem_usage = mem_info.used / 1024 / 1024 / 1024
        mem_percent = mem_info.percent

        # Updates label in realtime
        cpu_usage_lbl.configure(text = f'{cpu_usage}%')
        cpu_usage_bar.set(cpu_usage / 100)

        # Updates memory label and progress bar
        mem_usage_lbl.configure(text=f'{mem_usage:.2f}GB')
        mem_bar.set(mem_percent / 100)

def fetch_drive_info(drive):
    # Fetchs drive info and updates drive info label for selected drive
    usage = psutil.disk_usage(drive)
    total_size = usage.total / 1024 / 1024 / 1024
    used_size = usage.used / 1024 / 1024 / 1024
    free_size = usage.free / 1024 / 1024 / 1024
    used_percent = usage.percent

    drive_info_lbl.configure(text=f"Drive: {drive}\nTotal: {total_size:.2f} GB\nUsed: {used_size:.2f} GB\nFree: {free_size:.2f} GB")

    drive_used_bar.set(used_percent / 100)

def update_drive_info(event):
    # Event handeler for drive selection via comboBox
    selected_drive = drive_combobox.get()
    fetch_drive_info(selected_drive)

def rt_system_info():
    # Updates System info every 0.5 secs in a seprate thread
    while True:
        fetch_system_info()
        time.sleep(0.5)

# Main app setup
window = ctk.CTk()
window.title('')
window.geometry(Center_Window(window, 800, 600, window._get_window_scaling()))
window.iconbitmap('empty.ico')
window.resizable(False, False)

# Font Variables
font = ctk.CTkFont(family = 'Arial', size = 14)
bold_font = ctk.CTkFont(family = 'Arial', size = 50, weight = 'bold')
bold_drive_font = ctk.CTkFont(family = 'Arial', size = 18, weight = 'bold')

### Widgets ###
# Top frames & widgets
title_lbl = ctk.CTkLabel(window, text = 'System information', font = ('Arial', 24))

os_frame = ctk.CTkFrame(window)
os_lbl = ctk.CTkLabel(os_frame, text = (f'Operating System: {platform.platform()}'), font = font)

arch_frame = ctk.CTkFrame(window)
arch_lbl = ctk.CTkLabel(arch_frame, text = (f'Archiecture: {platform.architecture()[0]}'), font = font)

cpu_name_frame = ctk.CTkFrame(window)
cpu_name_lbl = ctk.CTkLabel(cpu_name_frame, text = (f'CPU: {cpu_info["brand_raw"]}'), font = font)

cpu_core_frame = ctk.CTkFrame(window)
cpu_core_lbl = ctk.CTkLabel(cpu_core_frame, text = (f'CPU Cores / Threads Count: {psutil.cpu_count(logical=False)} / {psutil.cpu_count()}'), font = font)

cpu_freq_frame = ctk.CTkFrame(window)
cpu_freq_lbl = ctk.CTkLabel(cpu_freq_frame, text = (f'CPU Base Frequency: {cpu_info["hz_advertised_friendly"]}'), font = font)

memory_frame = ctk.CTkFrame(window)
memory_lbl = ctk.CTkLabel(memory_frame, text = (f'Total RAM: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB'), font = font)

# Bottom frames & widgets
bottom_base_frame = ctk.CTkFrame(window, height = 300, fg_color = 'transparent')
bottom_base_frame.pack_propagate(False)

# Bottom left frame with Memory usage inside
bottom_frame_left = ctk.CTkFrame(bottom_base_frame)
bottom_frame_left.pack_propagate(False)
left_title_lbl = ctk.CTkLabel(bottom_frame_left, text = 'Memory usage', font = ('Arial', 18))
mem_usage_lbl = ctk.CTkLabel(bottom_frame_left, text = '%', font = bold_font)
mem_bar = ctk.CTkProgressBar(bottom_frame_left, progress_color = '#38a3a5')

# Bottom mid frame with cpu usage inside
bottom_frame_mid = ctk.CTkFrame(bottom_base_frame)
bottom_frame_mid.pack_propagate(False)
mid_title_lbl = ctk.CTkLabel(bottom_frame_mid, text = 'CPU usage', font = ('Arial', 18))
cpu_usage_lbl = ctk.CTkLabel(bottom_frame_mid, text = '%', font = bold_font)
cpu_usage_bar = ctk.CTkProgressBar(bottom_frame_mid,  progress_color = '#38a3a5')

# Bottom right frame & widgets with drive info inside
bottom_frame_right = ctk.CTkFrame(bottom_base_frame)
bottom_frame_right.pack_propagate(False)
right_title_lbl = ctk.CTkLabel(bottom_frame_right, text = 'Drive Info', font = ('Arial', 18))
drive_used_bar = ctk.CTkProgressBar(bottom_frame_right,  progress_color = '#38a3a5')
drive_info_lbl = ctk.CTkLabel(bottom_frame_right, text='Drive: \nTotal: \nUsed: \nFree: ', font = bold_drive_font)
drive_combobox = ctk.CTkComboBox(bottom_frame_right, values=[part.device for part in psutil.disk_partitions(all=False)], command=update_drive_info)

### Layout ###
# Top Layout
title_lbl.pack(padx = 20, pady = (20, 10))

os_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
os_lbl.pack(padx = 10, pady = 5, side = 'left')

arch_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
arch_lbl.pack(padx = 10, pady = 5, side = 'left')

cpu_name_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
cpu_name_lbl.pack(padx = 10, pady = 5, side = 'left')

cpu_core_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
cpu_core_lbl.pack(padx = 10, pady = 5, side = 'left')

cpu_freq_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
cpu_freq_lbl.pack(padx = 10, pady = 5, side = 'left')

memory_frame.pack(padx = 20, pady = 5, fill = 'x', anchor = 'n',)
memory_lbl.pack(padx = 10, pady = 5, side = 'left')

# Bottom layout
bottom_base_frame.pack(side = 'left', padx = 20, pady = (10, 20), expand = True, fill = 'both')
bottom_frame_left.pack(side = 'left', padx = 0, expand = True, fill = 'both')
bottom_frame_mid.pack(side = 'left', padx = 10, expand = True, fill = 'both')
bottom_frame_right.pack(side = 'left', padx = 0, expand = True, fill = 'both')

# Bottom left frame
left_title_lbl.pack(padx=10, pady=(5, 5), fill='both', expand=True)
mem_usage_lbl.pack(padx=10, pady=5, fill='both', expand=True)
mem_bar.pack(padx=10, pady=5, fill='x', expand=True)

# Bottom mid frame
mid_title_lbl.pack(padx=10, pady=(5, 5), fill='both', expand=True)
cpu_usage_lbl.pack(padx=10, pady=5, fill='both', expand=True)
cpu_usage_bar.pack(padx=10, pady=5, fill='x', expand=True)

# Bottom right frame
drive_combobox.pack(padx=10, pady=5, fill='x', expand=True)
drive_info_lbl.pack(padx=10, pady=5, fill='both', expand=True)
drive_used_bar.pack(padx=10, pady=10, fill='x', expand=True)

fetch_system_info()
fetch_drive_info(drive_combobox.get())

# starts a seprate thread to update system info in realtime.
threading.Thread(target = rt_system_info, daemon = True).start()

window.mainloop()
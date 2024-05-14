import socket, threading, tkinter as tk, queue, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

data_queue, data_store, additional_data_store = queue.Queue(), {'te':[],'al':[],'hu':[],'pr':[],'alt_speed':[], 'pi':[], 'ro':[]}, {'la':[],'lo':[],'pi':[],'ro':[]}
altitude_history, time_history = [], []

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("192.168.126.34", 1337))
        while True:
            data, _ = s.recvfrom(1024)
            if data: data_queue.put(data.decode("utf-8"))

def read_data_from_file():
    try:
        file_path = os.path.join(os.getcwd(), "data.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():
                    data_queue.put(line.strip())
                    # Introduce a small delay to simulate data transmission speed
                    #time.sleep(0.001)  # Adjust the delay time as needed
    except FileNotFoundError:
        print("File not found.")

def parse_data(line):
    parts = line.split('|')
    if len(parts) != 3 or parts[1] != 'd': return None, None
    kv = {k:float(v) if v.replace('.', '', 1).isdigit() else None for k,v in (x.split(':') for x in parts[2].split(',')) if v != 'e'}
    for k,v in kv.items():
        if v is not None:
            if k in data_store: data_store[k].append(int(v) if k in ['al', 'pr'] else v)
            else: additional_data_store[k].append(v)
    return parts[0], kv

def calc_altitude_speed():
    return 0 if len(altitude_history) < 2 else (altitude_history[-1] - altitude_history[-2]) / (time_history[-1] - time_history[-2]) if time_history[-1] - time_history[-2] else 0

def update_gui():
    if not data_queue.empty():
        raw_data = data_queue.get()
        timestamp, data_dict = parse_data(raw_data)
        if data_dict:
            for key, value in data_dict.items():
                if value is not None:
                    if key == 'al':
                        altitude_history.append(value)
                        time_history.append(time.time())
                        data_store['alt_speed'].append(calc_altitude_speed())
                    elif key in ['pi', 'ro']:
                        additional_data_store[key].append(value)
        plot_keys = ['te', 'al', 'hu', 'pr', 'alt_speed', 'pi', 'ro']  # Include 'pi' and 'ro' in plot keys
        for ax, key in zip(plot_axes, plot_keys):
            ax.clear()
            if data_store[key]: ax.plot(data_store[key])
            ax.set_title(f"{key.upper()} Over Time")
            ax.set_ylabel(key.upper())
        small_plot.clear()
        if additional_data_store['la'] and additional_data_store['lo']: small_plot.plot(additional_data_store['lo'], additional_data_store['la'], marker='o', linestyle='-', color='b')
        small_plot.set_title("Latitude and Longitude")
        small_plot.set_xlabel("Longitude")
        small_plot.set_ylabel("Latitude")
        small_plot.set_aspect('equal')  # Set aspect ratio to make the plot square
        canvas.draw()
        info_label.config(text=f"Last Update: {timestamp}")
    root.after(100, update_gui)

def select_data_source():
    if var.get() == "UDP":
        udp_thread = threading.Thread(target=udp_server, daemon=True)
        udp_thread.start()
    elif var.get() == "File":
        read_data_from_file()

# GUI setup
root = tk.Tk()
root.title("UDP Data Visualization")
root.protocol("WM_DELETE_WINDOW", root.quit)
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill='both')

# Add radio buttons to select data source
var = tk.StringVar(value="UDP")
udp_radio = tk.Radiobutton(main_frame, text="UDP", variable=var, value="UDP", command=select_data_source)
udp_radio.pack(side=tk.LEFT)
file_radio = tk.Radiobutton(main_frame, text="File", variable=var, value="File", command=select_data_source)
file_radio.pack(side=tk.LEFT)

fig = plt.figure(figsize=(15, 10))
plot_axes = [fig.add_subplot(2, 5, i+1) for i in range(7)]  # Increase the number of subplots to accommodate pitch and roll
small_plot = fig.add_subplot(2, 5, 8)  # Adjust the position for the small plot
canvas = FigureCanvasTkAgg(fig, main_frame)
canvas.get_tk_widget().pack(expand=True, fill='both')
info_label = tk.Label(main_frame, text="No data received yet.")
info_label.pack()

# Start UDP server thread and update GUI
root.after(100, update_gui)

root.mainloop()

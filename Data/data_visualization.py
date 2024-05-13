import socket, threading, tkinter as tk, queue, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


data_queue, data_store, additional_data_store = queue.Queue(), {'te':[],'al':[],'hu':[],'pr':[],'alt_speed':[]}, {'la':[],'lo':[],'pi':[],'ro':[]}
altitude_history, time_history = [], []

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("192.168.126.34", 1337))
        while True:
            data, _ = s.recvfrom(1024)
            if data: data_queue.put(data.decode("utf-8"))

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
    while not data_queue.empty():
        raw_data = data_queue.get()
        timestamp, data_dict = parse_data(raw_data)
        if not data_dict:
            continue
        for key, value in data_dict.items():
            if value is not None:
                if key == 'al':
                    altitude_history.append(value)
                    time_history.append(time.time())
                    data_store['alt_speed'].append(calc_altitude_speed())
                elif key in ['pi', 'ro']:
                    additional_data_store[key] = value  # Update pitch and roll angles

        plot_keys = ['te', 'hu', 'pr', 'al', 'alt_speed']
        for ax, key in zip(plot_axes, plot_keys):
            ax.clear()
            if data_store[key]:
                ax.plot(data_store[key])
            ax.set_title(f"{key.upper()} Over Time")
            ax.set_ylabel(key.upper())

        small_plot.clear()
        if additional_data_store['la'] and additional_data_store['lo']:
            small_plot.plot(additional_data_store['lo'], additional_data_store['la'], marker='o', linestyle='-', color='b')
        small_plot.set_title("Latitude and Longitude")
        small_plot.set_xlabel("Longitude")
        small_plot.set_ylabel("Latitude")

        three_d_plot.clear()
        # Render 3D cuboid
        cuboid_vertices = np.array([[0, 0, 0],
                                    [0, 0, 100],
                                    [0, 50, 0],
                                    [0, 50, 100],
                                    [150, 0, 0],
                                    [150, 0, 100],
                                    [150, 50, 0],
                                    [150, 50, 100]])
        
        # Define rotation matrix based on pitch and roll angles
        pitch = np.radians(additional_data_store['pi'])
        roll = np.radians(additional_data_store['ro'])
        R_pitch = np.array([[1, 0, 0],
                            [0, np.cos(pitch), -np.sin(pitch)],
                            [0, np.sin(pitch), np.cos(pitch)]])
        R_roll = np.array([[np.cos(roll), 0, np.sin(roll)],
                           [0, 1, 0],
                           [-np.sin(roll), 0, np.cos(roll)]])
        R = np.dot(R_pitch, R_roll)
        
        rotated_vertices = np.dot(cuboid_vertices, R.T)
        
        cuboid_edges = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]
        for edge in cuboid_edges:
            three_d_plot.plot3D(rotated_vertices[edge, 0], rotated_vertices[edge, 1], rotated_vertices[edge, 2], 'black')
        # Draw a large 'X' on the bottom face of the cuboid
        bottom_corners = rotated_vertices[[0, 1, 4, 5], :]
        x1, y1, z1 = bottom_corners[0]
        x2, y2, z2 = bottom_corners[3]
        three_d_plot.plot3D([x1, x2], [y1, y2], [z1, z2], color='red')
        x1, y1, z1 = bottom_corners[1]
        x2, y2, z2 = bottom_corners[2]
        three_d_plot.plot3D([x1, x2], [y1, y2], [z1, z2], color='red')
        three_d_plot.set_title("3D Cuboid")
        three_d_plot.set_xlabel("X Axis")
        three_d_plot.set_ylabel("Y Axis")
        three_d_plot.set_zlabel("Z Axis")
        canvas.draw()
        info_label.config(text=f"Last Update: {timestamp}")

    root.after(100, update_gui)





root = tk.Tk()
root.title("UDP Data Visualization")
root.protocol("WM_DELETE_WINDOW", root.quit)
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill='both')
fig = plt.figure(figsize=(15, 10))
plot_axes = [fig.add_subplot(2, 5, i+1) for i in range(5)]
small_plot = fig.add_subplot(2, 5, 6)
three_d_plot = fig.add_subplot(2, 5, (7,10), projection='3d')
canvas = FigureCanvasTkAgg(fig, main_frame)
canvas.get_tk_widget().pack(expand=True, fill='both')
info_label = tk.Label(main_frame, text="No data received yet.")
info_label.pack()
server_thread = threading.Thread(target=udp_server, daemon=True)
server_thread.start()
root.after(100, update_gui)
root.mainloop()
main_frame = tk.Frame(root)
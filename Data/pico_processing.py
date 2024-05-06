import matplotlib.pyplot as plt
import cartopy.crs as ccrs

class HoverDisplay:
    def __init__(self, ax):
        self.ax = ax
        self.annot = ax.annotate("", xy=(0,0), xytext=(-20,20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.ax.figure.canvas.mpl_connect("motion_notify_event", self.hover)

    def hover(self, event):
        if event.inaxes == self.ax:
            vis = self.annot.get_visible()
            if vis:
                self.annot.set_visible(False)
                self.ax.figure.canvas.draw_idle()
                return
            x, y = event.xdata, event.ydata
            text = f"Coordinates: ({x:.2f}, {y:.2f})"
            self.annot.xy = (x, y)
            self.annot.set_text(text)
            self.annot.set_visible(True)
            self.ax.figure.canvas.draw_idle()

def initialize_plot():
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    return fig, ax

def plot_map(ax, latitude, longitude):
    ax.clear()
    ax.scatter(longitude, latitude, color='red', s=10, label='Data Points')
    for i in range(len(latitude)-1):
        ax.plot([longitude[i], longitude[i+1]], [latitude[i], latitude[i+1]], color='blue', linewidth=1)
    ax.set_title('Location Data Visualization')
    ax.legend()
    hover_display = HoverDisplay(ax)
    plt.pause(0.01)

def parse_data(data):
    latitude = []
    longitude = []
    for entry in data:
        parts = entry.split("|")
        if len(parts) == 3 and parts[1] == "d":
            values = parts[2].split(",")
            for value in values:
                key, val = value.split(":")
                if key == "la":
                    latitude.append(float(val))
                elif key == "lo":
                    longitude.append(float(val))
    return latitude, longitude

def main():
    fig, ax = initialize_plot()
    data = []  # Initialize data list
    while True:
        # Input data
        input_data = input("Enter data line (or 'exit' to quit): ")
        if input_data.lower() == "exit":
            break
        
        data.append(input_data)  # Append new data to existing data
        
        # Parse data and plot map
        latitude, longitude = parse_data(data)
        plot_map(ax, latitude, longitude)

if __name__ == "__main__":
    main()

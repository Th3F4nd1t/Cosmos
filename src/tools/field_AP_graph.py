import json
import requests
import threading
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

URL = "http://10.0.100.2/status"
UPDATE_INTERVAL = 0.5  # seconds
HISTORY_LIMIT = 200
PARAMETERS = [
    # "signalDbm", "noiseDbm", "signalNoiseRatio",
    # "rxRateMbps", "txRateMbps", "bandwidthUsedMbps"
    "dataAgeMs", 
    "noiseDbm", 
    "signalNoiseRatio", 
    # "rxRateMbps", 
    # "rxPackets", 
    # "rxBytes", 
    # "txRateMbps", 
    # "txPackets", 
    # "txBytes", 
    "bandwidthUsedMbps"
]
STATIONS = ['red1', 'red2', 'red3', 'blue1', 'blue2', 'blue3']

class StationGraph:
    def __init__(self, parent, station_name):
        self.station_name = station_name
        self.data = {param: deque(maxlen=HISTORY_LIMIT) for param in PARAMETERS}
        self.timestamps = deque(maxlen=HISTORY_LIMIT)

        self.frame = ttk.LabelFrame(parent, text=station_name)
        self.label = ttk.Label(self.frame, text="NULL", foreground="gray")
        self.label.pack()

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.lines = {param: self.ax.plot([], [], label=param)[0] for param in PARAMETERS}
        self.ax.legend(loc='upper left', fontsize="medium")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack()
        self.active = False

    def update(self, snapshot):
        if snapshot is None:
            self.label.config(text="NULL")
            self.canvas.get_tk_widget().pack_forget()
            self.active = False
        else:
            self.active = True
            self.label.config(text="")
            self.canvas.get_tk_widget().pack()
            self.timestamps.append(time.time())
            for param in PARAMETERS:
                self.data[param].append(snapshot.get(param))
            self.redraw()

    def redraw(self):
        times = list(self.timestamps)
        for param in PARAMETERS:
            self.lines[param].set_data(times, list(self.data[param]))
        if times:
            self.ax.relim()
            self.ax.autoscale_view()
        self.canvas.draw()

class StatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Station Status Viewer")
        self.station_graphs = {}

        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(side=tk.TOP)

        for i, name in enumerate(STATIONS):
            graph = StationGraph(self.top_frame, name)
            graph.frame.grid(row=i // 3, column=i % 3)
            self.station_graphs[name] = graph

        self.bottom_frame = ttk.LabelFrame(root, text="Global Status")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_text = tk.Text(self.bottom_frame, height=10)
        self.status_text.pack(fill=tk.X)

        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        while self.running:
            try:
                res = requests.get(URL)
                res.raise_for_status()
                data = res.json()
                stations = data.get("stationStatuses", {})
                global_data = {k: v for k, v in data.items() if k != "stationStatuses"}

                self.status_text.delete("1.0", tk.END)
                self.status_text.insert(tk.END, json.dumps(global_data, indent=2))

                for name in STATIONS:
                    snapshot = stations.get(name)
                    self.root.after(0, self.station_graphs[name].update, snapshot)

            except Exception as e:
                print("Error fetching data:", e)

            time.sleep(UPDATE_INTERVAL)

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = StatusApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

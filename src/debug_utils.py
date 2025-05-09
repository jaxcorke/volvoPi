import psutil
import sys
import os
import time
import uptime
import threading
import customtkinter
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

os_name = sys.platform
initial_time = time.time()

graphing_intervals = 120
graphing_data = [0]*graphing_intervals
graphing_data_time = [0]*graphing_intervals
graphing_elapsed_time = [0]*graphing_intervals
graphing_data_cpu_percent = [None]*graphing_intervals
graphing_data_mem_percent = [None]*graphing_intervals
graphing_data_temp = [None]*graphing_intervals

max_temp = 0.0

def get_performance_stats():
    global max_temp

    current_time = time.time()
    uptime_days=str(int((uptime.uptime()/3600)/24)).zfill(2)
    uptime_hours=str(int((uptime.uptime()/3600)%24)).zfill(2)
    uptime_minutes=str(int((uptime.uptime()%3600)/60)).zfill(2)
    uptime_seconds=str(int((uptime.uptime()%3600)%60)).zfill(2)
    uptime_text=uptime_days+":"+uptime_hours+":"+uptime_minutes+":"+uptime_seconds
    
    cpu_percent = psutil.cpu_percent()
    cpu_freq = (psutil.cpu_freq()[0])/1000

    memory_percent = psutil.virtual_memory().percent 
    memory_fraction_neum = round((psutil.virtual_memory().total - psutil.virtual_memory().available)/(1024**3),1)  
    memory_fraction_denom = round(((psutil.virtual_memory().total)/(1024**3)),1)
    memory_fraction_str = str(memory_fraction_neum)+"/"+str(memory_fraction_denom)

    disk_percent = psutil.disk_usage(os.path.join('/')).percent
    disk_fraction_neum = round((psutil.disk_usage(os.path.join('/')).used / 1024**3),1)
    disk_fraction_denom = int((psutil.disk_usage((os.path.join('/'))).total / 1024**3))
    disk_fraction_str = str(disk_fraction_neum)+"/"+str(disk_fraction_denom)

    if os_name == "linux":
        current_temp = round(psutil.sensors_temperatures()["cpu_thermal"][0].current,1)
        if current_temp > max_temp:
            max_temp = current_temp
    else:
        current_temp = 0.0

    pids_count = len(psutil.pids())

    performance_stats = {
        "current_time": current_time,
        "uptime": (uptime_text, uptime_days, uptime_hours, uptime_minutes, uptime_seconds),
        "cpu_percent": cpu_percent,
        "cpu_freq": cpu_freq,
        "mem_percent": memory_percent,
        "mem_fraction": memory_fraction_str,
        "disk_percent": disk_percent, 
        "disk_fraction": disk_fraction_str,
        "temp_current": current_temp, 
        "temp_max": max_temp,
        "pids": pids_count
    }
    
    return(performance_stats)

def collect_graph_data():
    graphing_data.insert(0, get_performance_stats()) 
    if len(graphing_data) >= graphing_intervals:
        graphing_data.pop()

def split_graphing_data():
    graphing_data_time.insert(0, graphing_data[0]["current_time"])
    graphing_data_cpu_percent.insert(0, graphing_data[0]["cpu_percent"])
    graphing_data_mem_percent.insert(0, graphing_data[0]["mem_percent"])
    graphing_data_temp.insert(0, graphing_data[0]["temp_current"])
    
    if len(graphing_data_time) >= graphing_intervals:
        graphing_data_time.pop()
    if len(graphing_data_cpu_percent) >= graphing_intervals:
        graphing_data_cpu_percent.pop()
    if len(graphing_data_mem_percent) >= graphing_intervals:
        graphing_data_mem_percent.pop()
    if len(graphing_data_temp) >= graphing_intervals:
        graphing_data_temp.pop()

    for i in range(0, len(graphing_data_time)):
        if not graphing_data_time[i] == 0:
            graphing_elapsed_time[i] = graphing_data_time[i] - time.time()
        else:
            graphing_elapsed_time[i] = 0


app = customtkinter.CTk()
app.title("Graphing Test")
app.geometry("1200x600")
app.attributes("-fullscreen", True)
cpu_label = customtkinter.CTkLabel(app, text="",fg_color="gray16",bg_color="black")
cpu_label.pack(fill="both",expand=True,padx=10,pady=10)
mem_label = customtkinter.CTkLabel(app, text="",fg_color="gray16",bg_color="black")
mem_label.pack(fill="both",expand=True,padx=10,pady=10)
temp_label = customtkinter.CTkLabel(app, text="",fg_color="gray16",bg_color="black")
temp_label.pack(fill="both",expand=True,padx=10,pady=10)

def after_loop():       
    app.after(100, after_loop)

def collect():
    while True:
        collect_graph_data()
        split_graphing_data()
        time.sleep(0.1)

def plots():
    while True:
        plt.title("CPU")
        plt.figure(figsize=(5,2))
        plt.ylim(1,100)
        plt.style.use("dark_background")
        plt.grid(axis="y",color="gray",lw=1)     
        plt.plot(graphing_elapsed_time, graphing_data_cpu_percent,color="blue")
        plt.savefig("plotCPU.png")
        ctk_cpu_img = customtkinter.CTkImage(dark_image=Image.open("plotCPU.png"),size=(600,200))
        cpu_label.configure(image=ctk_cpu_img)
        save_ctk_cpu_img = ctk_cpu_img

        plt.title("RAM")
        plt.figure(figsize=(5,2))
        plt.ylim(1,100)
        plt.style.use("dark_background")
        plt.grid(axis="y",color="gray",lw=1)     
        plt.plot(graphing_elapsed_time, graphing_data_mem_percent,color="blue")
        plt.savefig("plotRAM.png")
        ctk_mem_img = customtkinter.CTkImage(dark_image=Image.open("plotRAM.png"),size=(600,200))
        mem_label.configure(image=ctk_mem_img)
        save_ctk_mem_img = ctk_mem_img

        plt.title("TEMP")
        plt.figure(figsize=(5,2))
        plt.ylim(1,100)
        plt.style.use("dark_background")
        plt.grid(axis="y",color="gray",lw=1)     
        plt.plot(graphing_elapsed_time, graphing_data_temp,color="blue")
        plt.savefig("plotTEMP.png")
        ctk_temp_img = customtkinter.CTkImage(dark_image=Image.open("plotTEMP.png"),size=(600,200))
        temp_label.configure(image=ctk_temp_img)
        save_ctk_temp_img = ctk_temp_img

        time.sleep(0.1)
        plt.close("all")

collect_debug_thread = threading.Thread(target=collect, daemon=True)
collect_debug_thread.start()

plot_debug_thread = threading.Thread(target=plots, daemon=True)
plot_debug_thread.start()

#app.after(100, after_loop)
app.mainloop()








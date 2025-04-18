print("Start volvoPi...")
#Imports custom
import gui
import data
#Imports standard
import time
import threading
import sys
import os
import configparser
import requests
import subprocess
#Imports external

#Global variables
mainloop_running = False
ignition = True
reverse = False
os_name = "unknown"

#identify os
os_name = sys.platform
print("Identified OS: " + os_name)

#APP functions
def get_wifi_status(os_name):
    if os_name == "win32":
        output = subprocess.check_output("netsh wlan show interfaces")
        decoded_output = output.decode("utf-8")
        #print(decoded_output)
        lines = decoded_output.splitlines()
        for line in lines:
            if "State" in line:
                return(line.split(":")[1].strip())
    elif os_name == "linux":
        print("os is linux")
    else:
        print("get_wifi_ssid: os not recognized")

def get_wifi_ssid(os_name):
    if os_name == "win32":
        output = subprocess.check_output("netsh wlan show interfaces")
        decoded_output = output.decode("utf-8")
        lines = decoded_output.splitlines()

        for line in lines:
            if "SSID" in line and not "BSSID" in line:
                return(line.split(":")[1].strip())

    elif os_name == "linux":
        print("os is linux")
    else:
        print("get_wifi_ssid: os not recognized")

#GUI updating functions
def update_clock():
    local_time = time.ctime()
    split_local_time = local_time.split()
    clock_time = str(split_local_time[3])[0:5]
    clock_date = split_local_time[0]+ " " + split_local_time[1] + " " + split_local_time[2]
    gui.app.home_frame.set_clock_text(clock_time, clock_date)

def update_wifi_status():
    if get_wifi_status(os_name) == "connected":
        gui.set_wifi_status(True)
    elif get_wifi_status(os_name) == "disconnected":
        gui.set_wifi_status(False)

def update_internet_status():
    try: 
        requests.get("http://www.google.com",timeout=5)
        gui.set_internet_status(True)
    except (requests.ConnectionError, requests.Timeout):
        gui.set_internet_status(False)

#Threads
#GUI
def guiUpdate():
    while mainloop_running == True:
        update_clock()
        update_internet_status()
        update_wifi_status()
        time.sleep(0.5)

thread_gui = threading.Thread(target=guiUpdate)

#Startup tasks
print("Starting app.mainloop...")
mainloop_running = True
thread_gui.start()

#Start GUI mainloop
gui.app.mainloop()

#Exit tasks
print("app.mainloop ended")
mainloop_running = False
time.sleep(1)
thread_gui.join()
print("Exiting program...")
exit(0)

#END
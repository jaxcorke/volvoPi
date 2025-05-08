print("Start volvoPi...")
print("Importing modules...")
#Imports custom
import gui
#Imports standard
import time
import threading
import sys
import os
import subprocess
import serial

print("...Imports complete")
#identify os
os_name = sys.platform
print("Identified OS: " + os_name)

#Global variables
mainloop_running = False
ignition = True
reverse = False

#Startup tasks
print("Starting gui.root.mainloop...")
gui.root.top_bar.set_message("Welcome! Identified OS: " + os_name, "green")

#Start GUI mainloop
mainloop_running = True
gui.root.mainloop()
mainloop_running = False

#Exit tasks
print("root.mainloop ended")
print("Exiting program...")
exit(0)

#END
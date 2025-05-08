#Name: gui.py
#Function: handles gui functionality

#<START>................................................................................................................
#Imports
import customtkinter
from PIL import Image, ImageTk
import sys
import time
import os
import requests
import threading
import subprocess
import psutil
import tkintermapview
import cv2

#GLOBAL VARIABLES <START>........................................................   
versionTagString = "volvoPi"
os_name = sys.platform

#Colors
background_gray = "#292929"
background_gray_2 = "#474747"

#ASSET PATHS <START>........................................................ 

if os.path.basename(os.getcwd()) == "src":
    os.chdir("..")

#Top Bar Icons Paths
internet_symbol_path = os.path.join(os.getcwd(),"assets","webSymbol.png")
wifi_symbol_path = os.path.join(os.getcwd(),"assets","wifiSymbol.png")
bluetooth_symbol_path = os.path.join(os.getcwd(),"assets","bluetoothSymbol.png")
gps_symbol_path = os.path.join(os.getcwd(),"assets","gpsSymbol.png")
#Button Panel Icons Paths
home_icon_path = os.path.join(os.getcwd(),"assets","homeIcon.png")
vehicle_icon_path = os.path.join(os.getcwd(),"assets","vehicleIcon.png")
cam_icon_path = os.path.join(os.getcwd(),"assets","camIcon.png")
menu_icon_path = os.path.join(os.getcwd(),"assets","menuIcon.png")
#Menu Icons Paths
settings_icon_path = os.path.join(os.getcwd(),"assets","settingsIcon.png")
wireless_icon_path = os.path.join(os.getcwd(),"assets","wirelessIcon.png")
debug_icon_path = os.path.join(os.getcwd(),"assets","debugIcon.png")
can_icon_path = os.path.join(os.getcwd(),"assets","canIcon.png")
serial_icon_path = os.path.join(os.getcwd(),"assets","serialIcon.png")
map_icon_path = os.path.join(os.getcwd(),"assets","mapIcon.png")

#Button Panel Icons
home_icon = customtkinter.CTkImage(dark_image=Image.open(home_icon_path),size=(100,100))
vehicle_icon = customtkinter.CTkImage(dark_image=Image.open(vehicle_icon_path),size=(120,100))
cam_icon = customtkinter.CTkImage(dark_image=Image.open(cam_icon_path),size=(100,100))
menu_icon = customtkinter.CTkImage(dark_image=Image.open(menu_icon_path),size=(100,100))
#Menu Icons
settings_icon = customtkinter.CTkImage(dark_image=Image.open(settings_icon_path),size=(60,60))
wireless_icon = customtkinter.CTkImage(dark_image=Image.open(wireless_icon_path),size=(60,60))
debug_icon = customtkinter.CTkImage(dark_image=Image.open(debug_icon_path),size=(60,60))
can_icon = customtkinter.CTkImage(dark_image=Image.open(can_icon_path),size=(70,50))
serial_icon = customtkinter.CTkImage(dark_image=Image.open(serial_icon_path),size=(70,40))
map_icon = customtkinter.CTkImage(dark_image=Image.open(map_icon_path),size=(60,60))

#ASSET PATHS <END>........................................................ 

#GLOBAL VARIABLES <END>........................................................

#GLOBAL FUNCTIONS <START>........................................................ 
#Exit Button

def exitButtonPress():
    root.exit_menu.place(anchor = "center", relx=0.5,rely=0.5,relwidth=1,relheight=0.6)

def exitConfirmExit():
    root.quit()

def exitCancelExit():
    root.exit_menu.place_forget()

#Button Panel

def home_button_press():
    root.main_frame.close_all()
    root.main_frame.home_frame.pack(fill="both",expand=True)
    
def vehicle_button_press():
    root.main_frame.close_all()

def cam_button_press():
    root.main_frame.close_all()
    root.main_frame.cam_frame.pack(fill="both",expand=True)

def menu_button_press():
    root.main_frame.close_all()
    root.main_frame.menu_frame.pack(fill="both",expand=True)

#Connection checks

def get_wifi_status(os_name):

    if os_name == "win32":
        try:
            output = subprocess.check_output("netsh wlan show interfaces")
            decoded_output = output.decode("utf-8")
            #print(decoded_output)
            lines = decoded_output.splitlines()
            for line in lines:
                if "State" in line:
                    if line.split(":")[1].strip() == "connected":
                        return(True)
                    else:
                        return(False)
        except:
            return(False)
        
    elif os_name == "linux":
        try:
            pass
        except:
            return(False)
    else:
        return(False)

def get_internet_status():
    try: 
        requests.get("http://www.google.com",timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

#Camera
camera = cv2.VideoCapture(0)

def camera_loop():
    while(True):
        while(root.main_frame.cam_frame.winfo_ismapped()): 
            if camera.isOpened():
                ret, new_frame = camera.read()
                if ret:
                    flipped_frame = cv2.flip(new_frame, 1)
                    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(rgb_frame) 

                    img_width_real, img_height_real = pil_img.size
                    real_aspect_ratio = img_width_real/img_height_real

                    camera_ctk = customtkinter.CTkImage(dark_image=pil_img,size=(img_width_real,img_height_real))
                    root.main_frame.cam_frame.cam_image_label.configure(image=camera_ctk)
                    root.main_frame.cam_frame.cam_image_label.pack(fill="both",expand=True,padx=10,pady=(0,10))
                    last_frame = camera_ctk
                time.sleep(1/60)
            else:
                camera.open(0)
        time.sleep(0)

#GLOBAL FUNCTIONS <END>........................................................ 

#GUI ELEMENTS <START>........................................................ 
#Main Elements

class BackgroundFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg_color="black",fg_color="black",border_width=2,border_color="blue")

class TopBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(bg_color="black",fg_color="black",border_width=2,border_color="blue",corner_radius=0)

        #Version label
        self.version_tag = customtkinter.CTkLabel(self, fg_color="blue", text_color="white", text=versionTagString, height=34, corner_radius=5,bg_color="transparent")
        self.version_tag.pack(side = "left", padx=5,pady=3)

        #Exit button
        self.exit_button = customtkinter.CTkButton(self,height=34,width=34,command=exitButtonPress,text="X",text_color="red",
                                                   corner_radius=4,fg_color="blue",bg_color="transparent",font=("Arial",28,"bold"),hover=False)
        self.exit_button.pack(side = "right",padx=5,pady=3)

        #Message Bar
        self.message_bar = customtkinter.CTkLabel(self,bg_color="black",fg_color="gray4",text="Messages",text_color="black",font=("Arial",18),corner_radius=8,anchor="e")
        self.message_bar.pack(side="right",pady=3,padx=(30,5),fill="x",expand=True)

        #Status symbols
        #internet
        self.internet_symbol_image = customtkinter.CTkImage(dark_image=Image.open(internet_symbol_path), size=(36,36))
        self.internet_symbol = customtkinter.CTkLabel(self, image=self.internet_symbol_image,text="")
        self.internet_symbol.pack(pady=3,side="left")
        self.internet_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.internet_symbol_status.pack(pady=6,side="left")
        #wifi
        self.wifi_symbol_image = customtkinter.CTkImage(dark_image=Image.open(wifi_symbol_path), size=(36,36))
        self.wifi_symbol = customtkinter.CTkLabel(self, image=self.wifi_symbol_image,text="")
        self.wifi_symbol.pack(pady=3,padx=(10,0),side="left")
        self.wifi_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.wifi_symbol_status.pack(pady=6,padx=2,side="left")
        #bluetooth
        self.bluetooth_symbol_image = customtkinter.CTkImage(dark_image=Image.open(bluetooth_symbol_path), size=(36,36))
        self.bluetooth_symbol = customtkinter.CTkLabel(self, image=self.bluetooth_symbol_image,text="")
        self.bluetooth_symbol.pack(pady=3,padx=(10,0),side="left")
        self.bluetooth_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.bluetooth_symbol_status.pack(pady=6,padx=2,side="left")
        #gps
        self.gps_symbol_image = customtkinter.CTkImage(dark_image=Image.open(gps_symbol_path), size=(36,36))
        self.gps_symbol = customtkinter.CTkLabel(self, image=self.gps_symbol_image,text="")
        self.gps_symbol.pack(pady=3,padx=(10,0),side="left")
        self.gps_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.gps_symbol_status.pack(pady=6,padx=2,side="left")

    def set_internet_state(self, state):
        if state:
            self.internet_symbol_status.configure(fg_color="green")
        else:
            self.internet_symbol_status.configure(fg_color="red")

    def set_wifi_state(self, state):
        if state:
            self.wifi_symbol_status.configure(fg_color="green")
        else:
            self.wifi_symbol_status.configure(fg_color="red")

    def set_gps_state(self, state):
        if state:
            self.gps_symbol_status.configure(fg_color=background_gray_2)
        else:
            self.gps_symbol_status.configure(fg_color="red")

    def set_bluetooth_state(self, state):
        if state:
            self.bluetooth_symbol_status.configure(fg_color=background_gray_2)
        else:
            self.bluetooth_symbol_status.configure(fg_color="red")

    def set_message(self, new_text, new_color):
        local_time = time.ctime()
        split_local_time = local_time.split()
        clock_time = str(split_local_time[3])[0:8]
        message_text = "[" + clock_time + "]: " + new_text
        self.message_bar.configure(text=message_text, text_color=new_color)

    def update_top_bar(self):
        while True:
            self.set_internet_state(get_internet_status())
            self.set_wifi_state(get_wifi_status(os_name))
            time.sleep(1)
        
class ExitMenuFrame(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=20,fg_color="white",bg_color="white")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.exit_menu_prompt = customtkinter.CTkLabel(self,height=200,font=("Arial",34))
        self.exit_menu_prompt.configure(corner_radius=12,fg_color="white",text_color="black")
        self.exit_menu_prompt.configure(text="Are you sure you want to exit?\n(Warning: A keyboard is required upon exiting)")
        self.exit_menu_prompt.grid(column=0,row=0,columnspan=2,padx=40,pady=10,sticky="nsew")

        self.exit_menu_cancel_button = customtkinter.CTkButton(self, width=110, height=120, text="Cancel",command=exitCancelExit,fg_color="blue",hover=False)
        self.exit_menu_cancel_button.configure(font=("Arial",34))
        self.exit_menu_cancel_button.grid(column=0,row=1,padx=40,pady=40,sticky="ew")

        self.exit_menu_exit_button = customtkinter.CTkButton(self, width=110,height=120,text="Exit",command=exitConfirmExit,fg_color="dark red",hover=False)
        self.exit_menu_exit_button.configure(font=("Arial",34))
        self.exit_menu_exit_button.grid(column=1,row=1,padx=40,pady=40,sticky="ew")

class ButtonPanelFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=background_gray,bg_color="black",corner_radius=10,width=250)

        self.home_button = customtkinter.CTkButton(self, width=210,fg_color="blue",text="",bg_color=background_gray,command=home_button_press, image=home_icon,hover=False)
        self.home_button.pack(pady=(20,10),padx=20,fill="y",expand=True)

        self.vehicle_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="",command=vehicle_button_press, image=vehicle_icon,hover=False)
        self.vehicle_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

        self.cam_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="",command=cam_button_press, image=cam_icon,hover=False)
        self.cam_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

        self.menu_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="",command=menu_button_press, image=menu_icon,hover=False)
        self.menu_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

class MainFrame(customtkinter.CTkFrame):

    class HomeFrame(customtkinter.CTkFrame):

        class ClimatePanel(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.configure(fg_color=background_gray,bg_color="black",corner_radius=10,width=450)
                self.grid_columnconfigure(0, weight=1)
                self.grid_columnconfigure(1,weight=1)
                self.grid_rowconfigure(0,weight=0)

                #Climate
                self.climate_label_frame = customtkinter.CTkFrame(self,border_width=2,border_color="blue",bg_color=background_gray,corner_radius=6,fg_color=background_gray)
                self.climate_label_frame.configure(width=313)
                self.climate_label_frame.rowconfigure(0, weight=1)
                self.climate_label_frame.grid(column=0,row=0,columnspan=2,sticky="ew",padx=0,pady=0)
                

                self.climate_label = customtkinter.CTkLabel(self.climate_label_frame, fg_color=background_gray,bg_color=background_gray,
                                                            text_color="white",text="Climate:",anchor="w",font=("Arial",42),width=250)
                self.climate_label.pack(pady=4,padx=8,side="left")

                #Fan
                self.fan_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Fan:"
                                                        ,text_color="white",font=("Arial",28),anchor="w")
                self.fan_label.grid(column=0,row=1,sticky="ew",padx=(8,0),pady=(8,0))

                self.fan_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("Arial",28),anchor="e")
                self.fan_value.grid(column=1,row=1,sticky="ew",padx=(0,5),pady=(8,0))

                #Temperature
                self.temp_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Temp:"
                                                        ,text_color="white",font=("Arial",28),anchor="w")
                self.temp_label.grid(column=0,row=2,sticky="ew",padx=(8,0),pady=(4,0))

                self.temp_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("Arial",28),anchor="e")
                self.temp_value.grid(column=1,row=2,sticky="ew",padx=(0,5),pady=(4,0))

                #AC status
                self.ac_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="A/C:"
                                                        ,text_color="white",font=("Arial",28),anchor="w")
                self.ac_label.grid(column=0,row=3,sticky="ew",padx=(8,0),pady=(4,0))

                self.ac_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("Arial",28),anchor="e")
                self.ac_value.grid(column=1,row=3,sticky="ew",padx=(0,5),pady=(4,0))

                #Compressor status
                self.compressor_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Compressor:"
                                                                ,text_color="white",font=("Arial",28),anchor="w")
                self.compressor_label.grid(column=0,row=4,sticky="ew",padx=(8,0),pady=(4,0))

                self.compressor_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("Arial",28),anchor="e")
                self.compressor_value.grid(column=1,row=4,sticky="ew",padx=(0,5),pady=(4,0))

        class Clock(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                #Clock
                self.configure(bg_color="black",fg_color="black")
                #clock time
                self.clock_time = customtkinter.CTkLabel(self, height=40,width=100,text="__:__",bg_color="black",fg_color="black",text_color="white",font=("Comfortaa",72,"bold"))
                self.clock_time.place(y=0,relx=0.5,anchor="n")
                #clock date
                self.clock_date = customtkinter.CTkLabel(self,text="date",font=("Arial",32),fg_color="black",bg_color="black",text_color="gray40")
                self.clock_date.place(anchor="n",relx=0.5,y=70)

            def set_clock(self, time, date):
                self.clock_time.configure(text=time)
                self.clock_date.configure(text=date)

            def update_clock(self):
                local_time = time.ctime()
                split_local_time = local_time.split()
                clock_time = str(split_local_time[3])[0:5]
                clock_date = split_local_time[0]+ " " + split_local_time[1] + " " + split_local_time[2]
                self.set_clock(clock_time, clock_date)

        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.configure(fg_color="black",bg_color="black")
            self.grid_columnconfigure(0,weight=1)
            self.grid_columnconfigure(1,weight=0)
            self.grid_rowconfigure(0,weight=1)

            #Clock
            self.clock = self.Clock(self)
            self.clock.grid(column=0,row=0,sticky="ewn",padx=(0,10))
            #Climate Panel
            self.climate_panel = self.ClimatePanel(self)
            self.climate_panel.grid(column=1,row=0,sticky="nse")

    class VehicleFrame(customtkinter.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

    class CamFrame(customtkinter.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.configure(bg_color="black",fg_color=background_gray)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

            self.cam_label = customtkinter.CTkLabel(self, text="Camera", font=("Arial",28),text_color="white",fg_color=background_gray_2,bg_color=background_gray)
            self.cam_label.configure(corner_radius=6)
            self.cam_label.pack(side="top",padx=10,pady=10,fill="x")

            self.cam_image_label = customtkinter.CTkLabel(self, text="", image=None, bg_color=background_gray,fg_color="green")

    class MenuFrame(customtkinter.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.configure(bg_color="black",fg_color=background_gray)

            for i in range(0,4):
                self.grid_columnconfigure(i,weight=1,uniform="grid_group")
            for i in range(0,4):
                self.grid_rowconfigure(i,weight=1,uniform="grid_group")

            self.menu_settings = customtkinter.CTkButton(self,text="Settings",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_settings,hover=False)
            self.menu_settings.configure(image=settings_icon,compound="top")
            self.menu_settings.grid(column=0,row=0,padx=(20,10),pady=10,sticky="nsew")

            self.menu_wireless = customtkinter.CTkButton(self,text="Wireless",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_connections,hover=False)
            self.menu_wireless.configure(image=wireless_icon,compound="top")
            self.menu_wireless.grid(column=1,row=0,padx=10,pady=10,sticky="nsew")

            self.menu_debug = customtkinter.CTkButton(self,text="Debug",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_debug,hover=False)
            self.menu_debug.configure(image=debug_icon,compound="top")
            self.menu_debug.grid(column=2,row=0,padx=10,pady=10,sticky="nsew")

            self.menu_map = customtkinter.CTkButton(self,text="Map",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_map,hover=False)
            self.menu_map.configure(image=map_icon,compound="top")
            self.menu_map.grid(column=2,row=1,padx=10,pady=10,sticky="nsew")

            self.menu_can = customtkinter.CTkButton(self,text="CAN View",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_can,hover=False)
            self.menu_can.configure(image=can_icon,compound="top")
            self.menu_can.grid(column=0,row=1,padx=(20,10),pady=10,sticky="nsew")

            self.menu_serial = customtkinter.CTkButton(self,text="Serial",bg_color="transparent",fg_color="blue",font=("Arial",24),command=self.master.open_serial,hover=False)
            self.menu_serial.configure(image=serial_icon,compound="top")
            self.menu_serial.grid(column=1,row=1,padx=10,pady=10,sticky="nsew")

            self.menu_show_screen = customtkinter.CTkButton(self, text="Screens",bg_color="transparent",fg_color="blue",font=("Arial",24),command=None,hover=False)
            self.menu_show_screen.grid(column=0,row=2,padx=(20,10),pady=10,sticky="nsew")

            self.menu_quick_settings_frame = customtkinter.CTkFrame(self,bg_color=background_gray,fg_color=background_gray_2)
            self.menu_quick_settings_frame.grid(column=3,row=0,rowspan=4,pady=10,padx=10,sticky="nsew")

    class SubmenusFrame(customtkinter.CTkFrame):

        class SettingsFrame(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.settings_label = customtkinter.CTkLabel(self, text="settings")
                self.settings_label.pack()

        class ConnectionsFrame(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.connections_label = customtkinter.CTkLabel(self, text="connections")
                self.connections_label.pack()

        class DebugFrame(customtkinter.CTkFrame):

            class PerformanceFrame(customtkinter.CTkFrame):
                def __init__(self, master, **kwargs):
                    super().__init__(master, **kwargs)
                    self.configure(fg_color=background_gray_2,bg_color=background_gray_2,corner_radius=10)
                    self.columnconfigure(1,weight=1)

                    self.performance_label = customtkinter.CTkLabel(self,bg_color=background_gray_2,fg_color=background_gray_2,text="Performance:",anchor="w",text_color="white")
                    self.performance_label.configure(font=("Arial",24,"bold"))
                    self.performance_label.grid(column=0,row=0,sticky="new",columnspan=3,pady=(0,6))

                    self.cpu_usage_label = customtkinter.CTkLabel(self, text="CPU:",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.cpu_usage_label.configure(font=("Arial",18))
                    self.cpu_usage_label.grid(column=0, row=1,sticky="w",padx=(10,20))

                    self.cpu_percent_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.cpu_percent_value.configure(font=("Arial",18))
                    self.cpu_percent_value.grid(column=1, row=1,sticky="w")

                    self.cpu_freq_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.cpu_freq_value.configure(font=("Arial",18))
                    self.cpu_freq_value.grid(column=2, row=1,sticky="e")

                    self.memory_usage_label = customtkinter.CTkLabel(self, text="RAM:",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.memory_usage_label.configure(font=("Arial",18))
                    self.memory_usage_label.grid(column=0, row=2,sticky="w",padx=(10,20))

                    self.memory_percent_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.memory_percent_value.configure(font=("Arial",18))
                    self.memory_percent_value.grid(column=1, row=2,sticky="w")

                    self.memory_fraction_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.memory_fraction_value.configure(font=("Arial",18))
                    self.memory_fraction_value.grid(column=2, row=2,sticky="e")

                    self.disk_usage_label = customtkinter.CTkLabel(self, text="Disk:",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.disk_usage_label.configure(font=("Arial",18))
                    self.disk_usage_label.grid(column=0, row=3,sticky="w",padx=(10,20))

                    self.disk_percent_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.disk_percent_value.configure(font=("Arial",18))
                    self.disk_percent_value.grid(column=1, row=3,sticky="w")

                    self.disk_fraction_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.disk_fraction_value.configure(font=("Arial",18))
                    self.disk_fraction_value.grid(column=2, row=3,sticky="e")

                    self.temp_label = customtkinter.CTkLabel(self, text="Temp:",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.temp_label.configure(font=("Arial",18))
                    self.temp_label.grid(column=0, row=4,sticky="w",padx=(10,20))

                    self.temp_value = customtkinter.CTkLabel(self, text="??",fg_color=background_gray_2,bg_color=background_gray_2,anchor="w",text_color="white")
                    self.temp_value.configure(font=("Arial",18))
                    self.temp_value.grid(column=1, row=4,sticky="w")

                    self.update_performance()

                def update_cpu(self):
                    self.cpu_percent_value.configure(text=str((psutil.cpu_percent(1))) + "%")
                    self.cpu_freq_value.configure(text= "(" + (str(int(psutil.cpu_freq()[0])/1000) + "GHz)"))

                def update_memory(self):
                    self.memory_percent_value.configure(text=str(psutil.virtual_memory().percent) + "%")  
                    self.memory_fraction_value.configure(text= "(" + str(round((psutil.virtual_memory().total - psutil.virtual_memory().available)/(1024**3),1)) + "/" + str(round(((psutil.virtual_memory().total)/(1024**3)),1)) + " GB)")

                def update_disk(self):
                    disk_value_percent = str(psutil.disk_usage(os.path.join('/')).percent) + "%"
                    disk_value_fraction = "(" + str(round((psutil.disk_usage(os.path.join('/')).used / 1024**3),1)) + "/" + str(int((psutil.disk_usage((os.path.join('/'))).total / 1024**3))) + "GB)"
                    self.disk_percent_value.configure(text=disk_value_percent)
                    self.disk_fraction_value.configure(text=disk_value_fraction)

                def upddate_temp(self):
                    if os_name == "linux":
                        self.temp_value.configure(text= str(round(psutil.sensors_temperatures()["cpu_thermal"][0].current,1)) + " C")
                    else:
                        self.temp_value.configure(text="N/A")

                def update_performance(self):
                    self.update_cpu()
                    self.update_memory()
                    self.update_disk()
                    self.upddate_temp()

            class ThreadingFrame(customtkinter.CTkFrame):
                def __init__(self, master, **kwargs):
                    super().__init__(master, **kwargs)
                    self.configure(fg_color=background_gray_2,bg_color=background_gray_2)
                    self.columnconfigure(0, weight=1)

                    self.threading_label = customtkinter.CTkLabel(self,bg_color=background_gray_2,fg_color=background_gray_2,text="Active Threads:",anchor="w",text_color="white")
                    self.threading_label.configure(font=("Arial",24,"bold"))
                    self.threading_label.grid(column=0,row=0,sticky="new")

                    self.threading_count = customtkinter.CTkLabel(self,bg_color=background_gray_2,fg_color=background_gray_2,text="?",anchor="w",text_color="white")
                    self.threading_count.configure(font=("Arial",20))
                    self.threading_count.grid(column=1,row=0,sticky="nw",padx=(0,5))

                    self.threading_list = customtkinter.CTkTextbox(self, bg_color=background_gray_2, fg_color=background_gray,activate_scrollbars=True,text_color="white",height=150)
                    self.threading_list.grid(column=0,row=1,sticky="new",columnspan=2)

                    self.show_threads()

                def show_threads(self):
                    self.threading_count.configure(text= "(" + str(threading.active_count()) + ")")
                    self.threading_list.configure(state="normal")
                    self.threading_list.delete(0.0, 'end')

                    for thread in threading.enumerate():
                        thread_entry = str(thread.native_id) + ": " + str(thread.name)
                        self.threading_list.insert('end', thread_entry + "\n")
                    
                    self.threading_list.insert('end', "\n")
                    self.threading_list.configure(state="disabled")

            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self.configure(bg_color="black",fg_color=background_gray,corner_radius=10)
                self.columnconfigure(0, weight=1, uniform="equal")
                self.columnconfigure(1, weight=1,uniform="equal")
                self.rowconfigure(1, weight=1)

                self.debug_label = customtkinter.CTkLabel(self, text="Debug & Sys Info:",bg_color=background_gray,fg_color=background_gray_2,font=("Arial",30,"bold"),text_color="white",anchor="w")
                self.debug_label.configure(corner_radius=6)
                self.debug_label.grid(column=0,row=0,sticky="nsew",columnspan=2,padx=10,pady=(10,0))

                #Left Panel
                self.left_frame = customtkinter.CTkFrame(self, bg_color=background_gray,fg_color=background_gray_2,corner_radius=6)
                self.performance_frame = self.PerformanceFrame(self.left_frame)
                self.performance_frame.pack(side="top",fill="x",padx=10,pady=(10,0))
                self.threading_frame = self.ThreadingFrame(self.left_frame)
                self.threading_frame.pack(side="top",fill="x",padx=10,pady=(10,0))

                self.left_frame.grid(column=0,row=1,pady=10,padx=10,sticky="nsew")

                #Right Panel
                self.right_frame = customtkinter.CTkFrame(self, bg_color=background_gray,fg_color=background_gray_2,corner_radius=6)

                self.right_frame.grid(column=1,row=1,pady=10,padx=10,sticky="nsew")

            def update_debug(self):
                while(True):
                    if root.main_frame.submenus_frame.debug_frame.winfo_ismapped():
                        self.threading_frame.show_threads()
                        self.performance_frame.update_performance()
                        time.sleep(0.2)
                    else:
                        time.sleep(0.5)

        class CANFrame(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.can_label = customtkinter.CTkLabel(self, text="CAN")
                self.can_label.pack()

        class SerialFrame(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.serial_label = customtkinter.CTkLabel(self, text="serial")
                self.serial_label.pack()

        class MapFrame(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self.configure(bg_color="black",fg_color=background_gray,corner_radius=10)
                self.rowconfigure(0, weight=0)
                self.rowconfigure(1, weight=1)
                self.columnconfigure(0, weight=1)

                self.map_label = customtkinter.CTkLabel(self, text="Map & Locations",font=("Arial",30), fg_color=background_gray_2,bg_color=background_gray)
                self.map_label.configure(text_color="white",corner_radius=10)
                self.map_label.grid(column=0,row=0,sticky="ew",padx=6,pady=(6,0))

            def create_map(self):
                self.map_widget = tkintermapview.TkinterMapView(self,corner_radius=10,bg_color=background_gray)
                #Default Postition (LSU, Baton Rouge, LA)
                self.map_widget.set_position(30.41, -91.18)
                self.map_widget.grid(column=0,row=1,sticky="nsew",padx=10,pady=10)

            def destroy_map(self):
                try:
                    self.map_widget.destroy()
                except:
                    pass

        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.settings_frame = self.SettingsFrame(self)
            self.connections_frame = self.ConnectionsFrame(self)
            self.debug_frame = self.DebugFrame(self)
            self.can_frame = self.CANFrame(self)
            self.serial_frame = self.SerialFrame(self)
            self.map_frame = self.MapFrame(self)

        def close_all(self):
            self.settings_frame.pack_forget()
            self.connections_frame.pack_forget()
            self.debug_frame.pack_forget()
            self.can_frame.pack_forget()
            self.serial_frame.pack_forget()
            self.map_frame.pack_forget()
            self.map_frame.destroy_map()

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg_color="black",fg_color=background_gray)

        self.home_frame = self.HomeFrame(self)
        self.vehicle_frame = self.VehicleFrame(self)
        self.cam_frame = self.CamFrame(self)
        self.menu_frame = self.MenuFrame(self)
        self.submenus_frame = self.SubmenusFrame(self)

        self.home_frame.pack(fill="both",expand=True)

    def close_all(self):
        self.home_frame.pack_forget()
        self.vehicle_frame.pack_forget()
        self.cam_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.submenus_frame.close_all()
        self.submenus_frame.pack_forget()

    #Open submenus

    def open_settings(self):
        self.close_all()
        self.submenus_frame.pack(fill="both",expand=True)
        self.submenus_frame.settings_frame.pack()

    def open_connections(self):
        self.close_all()
        self.submenus_frame.pack()
        self.submenus_frame.connections_frame.pack()

    def open_debug(self):
        self.close_all()
        self.submenus_frame.pack(fill="both",expand=True)
        self.submenus_frame.debug_frame.pack(fill="both",expand=True)

    def open_can(self):
        self.close_all()
        self.submenus_frame.pack()
        self.submenus_frame.can_frame.pack()

    def open_serial(self):
        self.close_all()
        self.submenus_frame.pack()
        self.submenus_frame.serial_frame.pack()

    def open_map(self):
        self.close_all()
        self.submenus_frame.map_frame.create_map()
        self.submenus_frame.pack(fill="both",expand=True)
        self.submenus_frame.map_frame.pack(fill="both",expand=True)

#Show Screens

#GUI ELEMENTS <END>........................................................ 

#WINDOW <START>........................................................ 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("volvoPi")
        self.geometry("1024x600")
        #self.maxsize(width=1920,height=1080)
        #self.minsize(width=1024,height=600)
        self.attributes("-fullscreen", True)

        self.top_bar = TopBarFrame(self)
        self.top_bar.pack(fill = "x")

        self.background = BackgroundFrame(self)
        self.background.pack(fill = "both", expand=True)

        self.exit_menu = ExitMenuFrame(self)

        self.button_panel = ButtonPanelFrame(self.background)
        self.button_panel.pack(padx=(10,0),pady=10,fill="y",anchor="w",side="left")

        self.main_frame = MainFrame(self.background)
        self.main_frame.pack(padx=(10,10),pady=10,fill="both",expand=True,anchor="center",side="left")

        self.top_bar.set_message("Welcome!",background_gray_2)

root = App()
#WINDOW <END>........................................................

#root.main_frame.submenus_frame.debug_frame.threading_frame.show_threads()
#root.main_frame.submenus_frame.debug_frame.performance_frame.update_performance()


#Threads
top_bar_thread = threading.Thread(target=root.top_bar.update_top_bar, daemon=True, name="top_bar_thread")
top_bar_thread.start()

debug_thread = threading.Thread(target=root.main_frame.submenus_frame.debug_frame.update_debug, daemon=True, name="update_debug")
debug_thread.start()

camera_thread = threading.Thread(target=camera_loop, daemon=True, name="camera")
camera_thread.start()

#mainloop tasks

def main_loop():
    #Home>Clock
    if root.main_frame.home_frame.winfo_ismapped():
        root.main_frame.home_frame.clock.update_clock()

    root.after(20, main_loop)

root.after(20, main_loop)

#<END>................................................................................................................
import customtkinter
from PIL import Image
import sys
import time
import os
import requests
import threading
import subprocess

#Global Variables
versionTagString = "volvoPi"
os_name = sys.platform
background_gray = "gray8"

#assets paths
if os.path.basename(os.getcwd()) == "src":
    os.chdir("..")

internet_symbol_path = os.path.join(os.getcwd(),"assets","webSymbol.png")
wifi_symbol_path = os.path.join(os.getcwd(),"assets","wifiSymbol.jpg")
bluetooth_symbol_path = os.path.join(os.getcwd(),"assets","bluetoothSymbol.jpg")
gps_symbol_path = os.path.join(os.getcwd(),"assets","gpsSymbol.jpg")

#GLOBAL FUNCTIONS <START>
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
        return(False)
    
    else:
        return(False)

def get_internet_status():
    try: 
        requests.get("http://www.google.com",timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

#GLOBAL FUNCTIONS <END>

#GUI ELEMENTS <START>
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
                                                   corner_radius=4,fg_color="blue",bg_color="transparent",font=("CTkFont",28,"bold"))
        self.exit_button.pack(side = "right",padx=5,pady=3)

        #Message Bar
        self.message_bar = customtkinter.CTkLabel(self,bg_color="black",fg_color="gray4",text="Messages",text_color="black",font=("CTkFont",18),corner_radius=8,anchor="e")
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
            self.gps_symbol_status.configure(fg_color="green")
        else:
            self.gps_symbol_status.configure(fg_color="red")

    def set_bluetooth_state(self, state):
        if state:
            self.bluetooth_symbol_status.configure(fg_color="green")
        else:
            self.bluetooth_symbol_status.configure(fg_color="red")

    def set_message(self, new_text, new_color):
        local_time = time.ctime()
        split_local_time = local_time.split()
        clock_time = str(split_local_time[3])[0:8]
        message_text = "[" + clock_time + "]: " + new_text
        self.message_bar.configure(text=message_text, text_color=new_color)

    def update_top_bar_loop(self):
        while True:
            #print("internet:",get_internet_status())
            self.set_internet_state(get_internet_status())
            #print("wifi:",get_wifi_status(os_name))
            self.set_wifi_state(get_wifi_status(os_name))
            time.sleep(2)
        
class ExitMenuFrame(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=20,fg_color="gray16",bg_color="gray16")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.exit_menu_prompt = customtkinter.CTkTextbox(self,height=200,font=("CTkFont",34),wrap="word",activate_scrollbars=False)
        self.exit_menu_prompt.configure(corner_radius=12,fg_color="gray16",text_color="white")
        self.exit_menu_prompt.insert(0.0,"Are you sure you want to exit?\nYou will be sent to terminal, a keyboard is needed.")
        self.exit_menu_prompt.configure(state="disabled")
        self.exit_menu_prompt.grid(column=0,row=0,columnspan=2,padx=40,pady=10,sticky="nsew")

        self.exit_menu_cancel_button = customtkinter.CTkButton(self, width=110, height=120, text="Cancel",command=exitCancelExit,fg_color="blue")
        self.exit_menu_cancel_button.configure(font=("CTkFont",34))
        self.exit_menu_cancel_button.grid(column=0,row=1,padx=40,pady=40,sticky="ew")

        self.exit_menu_exit_button = customtkinter.CTkButton(self, width=110,height=120,text="Exit",command=exitConfirmExit,fg_color="dark red")
        self.exit_menu_exit_button.configure(font=("CTkFont",34))
        self.exit_menu_exit_button.grid(column=1,row=1,padx=40,pady=40,sticky="ew")

class ButtonPanelFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=background_gray,bg_color="black",corner_radius=12,width=250)

        self.home_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="Home",
                                                   font=("CTkFont",32),text_color="White",command=home_button_press)
        self.home_button.pack(pady=(20,10),padx=20,fill="y",expand=True)

        self.vehicle_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="Vehicle",
                                                      font=("CTkFont",32),text_color="White",command=vehicle_button_press)
        self.vehicle_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

        self.cam_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="Cam",
                                                  font=("CTkFont",32),text_color="White",command=cam_button_press)
        self.cam_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

        self.menu_button = customtkinter.CTkButton(self, width=210,fg_color="blue",bg_color=background_gray,text="Menu",
                                                   font=("CTkFont",32),text_color="White",command=menu_button_press)
        self.menu_button.pack(pady=(10,10),padx=20,fill="y",expand=True)

class MainFrame(customtkinter.CTkFrame):

    class HomeFrame(customtkinter.CTkFrame):

        class ClimatePanel(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)

                self.configure(fg_color=background_gray,bg_color="black",corner_radius=12)
                self.grid_columnconfigure(0, weight=1)
                self.grid_columnconfigure(1,weight=0)

                #Climate
                self.climate_label_frame = customtkinter.CTkFrame(self,border_width=2,border_color="blue",bg_color=background_gray,corner_radius=6,fg_color=background_gray)
                self.climate_label_frame.grid(column=0,row=0,columnspan=2,sticky="ew",padx=0,pady=0)

                self.climate_label = customtkinter.CTkLabel(self.climate_label_frame, fg_color=background_gray,bg_color=background_gray,
                                                            text_color="white",text="Climate:",anchor="w",font=("CTkFont",42))
                self.climate_label.pack(pady=4,padx=8,side="left")

                #Fan
                self.fan_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Fan:"
                                                        ,text_color="white",font=("CTkFont",28),anchor="w")
                self.fan_label.grid(column=0,row=1,sticky="ew",padx=(8,0),pady=(8,0))

                self.fan_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="000%"
                                                        ,text_color="white",font=("CTkFont",28),anchor="e")
                self.fan_value.grid(column=1,row=1,sticky="ew",padx=(0,5),pady=(8,0))

                #Temperature
                self.temp_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Temp:"
                                                        ,text_color="white",font=("CTkFont",28),anchor="w")
                self.temp_label.grid(column=0,row=2,sticky="ew",padx=(8,0),pady=(4,0))

                self.temp_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="-000%"
                                                        ,text_color="white",font=("CTkFont",28),anchor="e")
                self.temp_value.grid(column=1,row=2,sticky="ew",padx=(0,5),pady=(4,0))

                #AC status
                self.ac_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="A/C:"
                                                        ,text_color="white",font=("CTkFont",28),anchor="w")
                self.ac_label.grid(column=0,row=3,sticky="ew",padx=(8,0),pady=(4,0))

                self.ac_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("CTkFont",28),anchor="e")
                self.ac_value.grid(column=1,row=3,sticky="ew",padx=(0,5),pady=(4,0))

                #Compressor status
                self.compressor_label = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="Compressor:"
                                                                ,text_color="white",font=("CTkFont",28),anchor="w")
                self.compressor_label.grid(column=0,row=4,sticky="ew",padx=(8,0),pady=(4,0))

                self.compressor_value = customtkinter.CTkLabel(self,fg_color=background_gray,bg_color=background_gray,text="???"
                                                        ,text_color="white",font=("CTkFont",28),anchor="e")
                self.compressor_value.grid(column=1,row=4,sticky="ew",padx=(0,5),pady=(4,0))

        class Clock(customtkinter.CTkFrame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                #Clock
                self.configure(bg_color="black",fg_color="black")
                #clock time
                self.clock_time = customtkinter.CTkLabel(self, height=40,width=100,text="__:__",bg_color="black",fg_color="black",text_color="white",font=("CTkFont",72))
                self.clock_time.place(y=0,relx=0.5,anchor="n")
                #clock date
                self.clock_date = customtkinter.CTkLabel(self,text="date",font=("CTkFont",32),fg_color="black",bg_color="black",text_color="gray40")
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

        def update_home_frame_loop(self):
            self.clock.update_clock()
            time.sleep(0.5)

    class MenuFrame(customtkinter.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            self.configure(bg_color="black",fg_color=background_gray)

            for i in range(0,4):
                self.grid_columnconfigure(i,weight=1)
            for i in range(0,4):
                self.grid_rowconfigure(i,weight=1)

            self.menu_settings = customtkinter.CTkButton(self,text="Settings",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_settings.grid(column=0,row=0,padx=(20,10),pady=10,sticky="nsew")

            self.menu_connections = customtkinter.CTkButton(self,text="Connections",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_connections.grid(column=1,row=0,padx=10,pady=10,sticky="nsew")

            self.menu_debug = customtkinter.CTkButton(self,text="Debug/\nSys Info",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_debug.grid(column=2,row=0,padx=10,pady=10,sticky="nsew")

            self.menu_map = customtkinter.CTkButton(self,text="Map\nand Locations",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_map.grid(column=2,row=1,padx=10,pady=10,sticky="nsew")

            self.menu_can = customtkinter.CTkButton(self,text="CAN\nView",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_can.grid(column=0,row=1,padx=(20,10),pady=10,sticky="nsew")

            self.menu_serial = customtkinter.CTkButton(self,text="Serial",bg_color="transparent",fg_color="blue",font=("CTkFont",24))
            self.menu_serial.grid(column=1,row=1,padx=10,pady=10,sticky="nsew")

            #self.menu_show_screen = customtkinter.CTkButton(self, text="Show Screens",bg_color="transparent",fg_color="blue",font=("CTkFont",24),command=show_screen)
            #self.menu_show_screen.grid(column=0,row=2,padx=(20,10),pady=10,sticky="nsew")

            self.menu_quick_settings_frame = customtkinter.CTkFrame(self,bg_color=background_gray,fg_color="black")
            self.menu_quick_settings_frame.grid(column=3,row=0,rowspan=4,pady=10,padx=10,sticky="nsew")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg_color="black",fg_color=background_gray)

        self.home_frame = self.HomeFrame(self)
        self.home_frame.pack(fill="both",expand=True)

        self.menu_frame = self.MenuFrame(self)

    def close_all(self):
        self.home_frame.pack_forget()
        self.menu_frame.pack_forget()

#Submenus

#Show Screens

#GUI ELEMENTS <END>

#WINDOW
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("volvoPi")
        self.geometry("1024x600")
        self.maxsize(width=1920,height=1080)
        self.minsize(width=1024,height=600)

        self.top_bar = TopBarFrame(self)
        self.top_bar.pack(fill = "x")

        self.background = BackgroundFrame(self)
        self.background.pack(fill = "both", expand=True)

        self.exit_menu = ExitMenuFrame(self)

        self.button_panel = ButtonPanelFrame(self.background)
        self.button_panel.pack(padx=(10,0),pady=10,fill="y",anchor="w",side="left")

        self.main_frame = MainFrame(self.background)
        self.main_frame.pack(padx=(10,10),pady=10,fill="both",expand=True,anchor="center",side="left")

        self.top_bar.set_message("Welcome!","green")

root = App()

#Threads

#Top Bar
top_bar_thread = threading.Thread(target=root.top_bar.update_top_bar_loop, daemon=True)
top_bar_thread.start()
#Home
home_thread = threading.Thread(target=root.main_frame.home_frame.update_home_frame_loop, daemon=True)
home_thread.start()

#mainloop tasks
def update_loop():
    
    root.after(100, update_loop)

root.after(100, update_loop)

#root.mainloop()
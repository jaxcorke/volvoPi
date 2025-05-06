import customtkinter
from PIL import Image
import sys
import time
import os
import requests
import threading
import subprocess

versionTagString = "volvoPi v0.0.0a"
os_name = sys.platform
background_gray = "gray8"
cam_open = False
static_screen_on = False

#assets paths
internet_symbol_path = os.path.join("assets","webSymbol.png")
wifi_symbol_path = os.path.join(os.getcwd(),"assets","wifiSymbol.jpg")
bluetooth_symbol_path = os.path.join(os.getcwd(),"assets","bluetoothSymbol.jpg")
gps_symbol_path = os.path.join(os.getcwd(),"assets","gpsSymbol.jpg")

def show_screen_click(event):
    root.buckle_up_1_frame.place_forget()
    root.buckle_up_2_frame.place_forget()
    root.black_screen_frame.place_forget()

#Exit button functions
def exitButtonPress():
    root.exit_menu.place(anchor = "center", relx=0.5,rely=0.5,relwidth=1,relheight=0.6)

def exitConfirmExit():
    root.quit()

def exitCancelExit():
    root.exit_menu.place_forget()

#Button Panel Functions
def home_button_press():

    #close others
    global cam_open
    cam_open = False
    root.menu_frame.pack_forget()

    root.show_screen_selection.pack_forget()
    #open home
    root.home_frame.pack(pady=2,padx=2,side="left",fill="both",expand=True)
    
def vehicle_button_press():
    global cam_open
    cam_open = False
    root.home_frame.pack_forget()
    root.menu_frame.pack_forget()

def cam_button_press():
     global cam_open
     cam_open = True
     root.home_frame.pack_forget()
     root.menu_frame.pack_forget()

def menu_button_press():
     global cam_open
     cam_open = False
     root.home_frame.pack_forget()
     root.show_screen_selection.pack_forget()
     root.menu_frame.pack(pady=10,padx=(0,10),side="left",fill="both",expand=True)

#TopBar functions
def set_message_text(new_text,new_color):
    local_time = time.ctime()
    split_local_time = local_time.split()
    clock_time = str(split_local_time[3])[0:8]
    message_text = "[" + clock_time + "]: " + new_text
    root.top_bar_frame.message_bar.configure(text=message_text,text_color=new_color)

def set_wifi_status(status):
            if status:
                root.top_bar_frame.wifi_symbol_status.configure(fg_color="green")
            else:
                root.top_bar_frame.wifi_symbol_status.configure(fg_color="red")

def set_internet_status(status):
            if status:
                root.top_bar_frame.internet_symbol_status.configure(fg_color="green")
            else:
                root.top_bar_frame.internet_symbol_status.configure(fg_color="red")

def get_internet_status():
    try: 
        requests.get("http://www.google.com",timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

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

#######################################################################
#GUI ELEMENTS
#Main
class TopBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=1030,height=40,bg_color="black",fg_color="black",border_width=2,border_color="blue",corner_radius=0)

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

class BackgroundFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=1024,height=573,bg_color="black",fg_color="transparent",border_width=2,border_color="blue")
         
class ExitMenuFrame(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=20,fg_color=background_gray,bg_color=background_gray)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.exit_menu_prompt = customtkinter.CTkTextbox(self,height=200,font=("CTkFont",34),wrap="word",activate_scrollbars=False)
        self.exit_menu_prompt.configure(corner_radius=12,fg_color=background_gray,text_color="white")
        self.exit_menu_prompt.insert(0.0,"Are you sure you want to exit?\nYou will be sent to terminal, a keyboard is needed.")
        self.exit_menu_prompt.configure(state="disabled")
        self.exit_menu_prompt.grid(column=0,row=0,columnspan=2,padx=40,pady=10,sticky="nsew")

        self.exit_menu_cancel_button = customtkinter.CTkButton(self, width=110, height=120, text="Cancel",command=exitCancelExit,fg_color="blue")
        self.exit_menu_cancel_button.configure(font=("CTkFont",34))
        self.exit_menu_cancel_button.grid(column=0,row=1,padx=40,pady=40,sticky="ew")

        self.exit_menu_exit_button = customtkinter.CTkButton(self, width=110,height=120,text="Exit",command=exitConfirmExit,fg_color="dark red")
        self.exit_menu_exit_button.configure(font=("CTkFont",34))
        self.exit_menu_exit_button.grid(column=1,row=1,padx=40,pady=40,sticky="ew")


class ButtonPanel(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=background_gray,bg_color="black",corner_radius=20,width=250)

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

#Home
class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="black",bg_color="black")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        #Clock
        #clock frame
        self.clock_frame = customtkinter.CTkFrame(self,bg_color="black",fg_color="black",height=120,width=200)
        self.clock_frame.grid(column=0,row=0,sticky="ewn")
        #clock time
        self.clock_frame.clock = customtkinter.CTkLabel(master=self.clock_frame, height=40,width=100,
        text="__:__",bg_color="transparent",fg_color="transparent",text_color="white",font=("CTkFont",72),anchor="s")
        self.clock_frame.clock.place(y=0,relx=0.5,anchor="n")
        #clock date
        self.clock_frame.clock_date = customtkinter.CTkLabel(master=self.clock_frame,text="date",font=("CTkFont",32),
        fg_color="black",bg_color="black",text_color="gray40")
        self.clock_frame.clock_date.place(anchor="n",relx=0.5,y=70)

        #Climate Panel
        self.climate_panel = ClimatePanel(master=self)
        self.climate_panel.grid(column=1,row=0,sticky="nse",pady=10,padx=10)

    def set_clock_text(self, clock_time, clock_date):
        self.clock_frame.clock.configure(text=clock_time)
        self.clock_frame.clock_date.configure(text=clock_date)

class ClimatePanel(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=background_gray,bg_color="black",corner_radius=20,width=250)
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

#Vehicle

#Cam

#Menu
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

        self.menu_show_screen = customtkinter.CTkButton(self, text="Show Screens",bg_color="transparent",fg_color="blue",font=("CTkFont",24),command=show_screen)
        self.menu_show_screen.grid(column=0,row=2,padx=(20,10),pady=10,sticky="nsew")

        self.menu_quick_settings_frame = customtkinter.CTkFrame(self,bg_color=background_gray,fg_color="black")
        self.menu_quick_settings_frame.grid(column=3,row=0,rowspan=4,pady=10,padx=10,sticky="nsew")

def show_screen():
    root.menu_frame.pack_forget()
    root.show_screen_selection.pack(pady=10,padx=(0,10),side="left",fill="both",expand=True)

#Settings

#Connections

#Map and location

#Debug/sys info

#Terminal

#CAN

#Show Screens
class ShowScreenSelection(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(bg_color="black",fg_color=background_gray)
        for i in range(0,2):
            self.columnconfigure(i,weight=1)
            self.rowconfigure(i,weight=1)

        self.buckle_up_button_1 = customtkinter.CTkButton(self, text="Buckle Up 1", font=("CTkFont",24),command=place_screen_buckle_up_1)
        self.buckle_up_button_1.grid(column=0,row=0,padx=(20,10),pady=(20,10),sticky="nsew")

        self.buckle_up_button_2 = customtkinter.CTkButton(self, text="Buckle Up 2", font=("CTkFont",24),command=place_screen_buckle_up_2)
        self.buckle_up_button_2.grid(column=1,row=0,padx=(20,10),pady=(20,10),sticky="nsew")

        self.black_screen_button = customtkinter.CTkButton(self, text="Black Screen", font=("CTkFont",24),command=place_black_screen)
        self.black_screen_button.grid(column=0,row=1,padx=(20,10),pady=(20,10),sticky="nsew")

class BuckleUp1Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Button-1>", show_screen_click)
        self.configure(bg_color="black",fg_color="black")

        self.top_text = customtkinter.CTkLabel(self, text="BUCKLE UP",font=("CTkFont",124),anchor="center",text_color="white")
        self.top_text.pack(pady=40,side="top")

def place_screen_buckle_up_1():
    root.buckle_up_1_frame.place(anchor="center",relx=0.5,rely=0.5,relheight=1,relwidth=1)

class BuckleUp2Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Button-1>", show_screen_click)
        self.configure(bg_color="black",fg_color="black")

        self.top_text = customtkinter.CTkLabel(self, text="BUCKLE UP",font=("CTkFont",124),anchor="center",text_color="white")
        self.top_text.pack(pady=40,side="top")

        self.bottom_text = customtkinter.CTkLabel(self, text="PRINCESS",font=("CTkFont",124),anchor="center",text_color="white")
        self.bottom_text.pack(pady=40,side="bottom")

def place_screen_buckle_up_2():
    root.buckle_up_2_frame.place(anchor="center",relx=0.5,rely=0.5,relheight=1,relwidth=1)

class BlackFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Button-1>", show_screen_click)
        self.configure(bg_color="black",fg_color="black")

        self.top_text = customtkinter.CTkLabel(self, text="",font=("CTkFont",124),anchor="center",text_color="white")
        self.top_text.pack(pady=40,side="top")

def place_black_screen():
    root.black_screen_frame.place(anchor="center",relx=0.5,rely=0.5,relheight=1,relwidth=1)

###################################################################
#WINDOW        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("volvoPi")
        self.geometry("1024x600")
        self.maxsize(width=1920,height=1080)
        self.minsize(width=1024,height=600)

        self.create_gui_elements()

        self.exit_menu = ExitMenuFrame(master=self)

    def create_gui_elements(self):
        #Main GUI Elements
        #Top bar
        self.top_bar_frame = TopBarFrame(master=self)
        self.top_bar_frame.pack(fill = "x")
        #Background
        self.background_frame = BackgroundFrame(master=self)
        self.background_frame.pack(pady=0, fill = "both",expand=True)
        #Button Panel
        self.button_panel = ButtonPanel(master=self.background_frame)
        self.button_panel.pack(padx=10,pady=(10,10),side="left",fill="y")

        #Home
        self.home_frame = HomeFrame(master=self.background_frame)
        self.home_frame.pack(pady=2,padx=2,side="left",fill="both",expand=True)
        #Menu
        self.menu_frame = MenuFrame(master=self.background_frame)

        #Show Screens
        self.show_screen_selection = ShowScreenSelection(master=self.background_frame)
        self.buckle_up_1_frame = BuckleUp1Frame(master=self)
        self.buckle_up_2_frame = BuckleUp2Frame(master=self)
        self.black_screen_frame = BlackFrame(master=self)

    def update_clock(self):
        local_time = time.ctime()
        split_local_time = local_time.split()
        clock_time = str(split_local_time[3])[0:5]
        clock_date = split_local_time[0]+ " " + split_local_time[1] + " " + split_local_time[2]
        root.home_frame.set_clock_text(clock_time, clock_date)

root = App()

#UPDATE GUI

#Threaded functions
def update_statusbar():
    while True:
        set_internet_status(get_internet_status())  
        if get_wifi_status(os_name) == "connected":
            set_wifi_status(True)
        else:
            set_wifi_status(False)
        time.sleep(2)

#Threads   
gui_statusbar_thead = threading.Thread(target=update_statusbar, daemon=True)
gui_statusbar_thead.start()

#mainloop function
def gui_update():
    root.update_clock()

    root.after(20, gui_update)

root.after(20, gui_update)
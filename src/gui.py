import customtkinter
from PIL import Image

versionTagString = "volvoPi v0.0.0a"

#Exit button functions
def exitButtonPress():
    app.exit_menu.place(anchor = "center", relx=0.5,rely=0.5,relwidth=0.5,relheight=0.5)

def exitConfirmExit():
    app.quit()

def exitCancelExit():
    app.exit_menu.place_forget()

#Status symbol functions
def set_wifi_status(status):
            if status:
                app.top_bar_frame.wifi_symbol_status.configure(fg_color="green")
            else:
                app.top_bar_frame.wifi_symbol_status.configure(fg_color="red")

def set_internet_status(status):
            if status:
                app.top_bar_frame.internet_symbol_status.configure(fg_color="green")
            else:
                app.top_bar_frame.internet_symbol_status.configure(fg_color="red")

#Define GUI elements
class TopBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=1030,height=40,bg_color="black",fg_color="black",border_width=2,border_color="blue",corner_radius=0)

        self.version_tag = customtkinter.CTkLabel(self, fg_color="blue", text_color="white", text=versionTagString, height=34, corner_radius=5,bg_color="transparent")
        self.version_tag.pack(side = "left", padx=5,pady=3)

        self.exit_button = customtkinter.CTkButton(self,height=34,width=34,command=exitButtonPress,text="X",text_color="red",corner_radius=4,fg_color="blue",bg_color="transparent")
        self.exit_button.pack(side = "right",padx=5,pady=3)

        self.internet_symbol_image = customtkinter.CTkImage(dark_image=Image.open(".\\assets\\webSymbol.png"), size=(36,36))
        self.internet_symbol = customtkinter.CTkLabel(self, image=self.internet_symbol_image,text="")
        self.internet_symbol.pack(pady=3,side="left")
        self.internet_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.internet_symbol_status.pack(pady=6,side="left")

        self.wifi_symbol_image = customtkinter.CTkImage(dark_image=Image.open(".\\assets\\wifiSymbol.jpg"), size=(36,36))
        self.wifi_symbol = customtkinter.CTkLabel(self, image=self.wifi_symbol_image,text="")
        self.wifi_symbol.pack(pady=3,padx=(10,0),side="left")
        self.wifi_symbol_status = customtkinter.CTkLabel(self,fg_color="gray",height=34,width=10,corner_radius=4,text="")
        self.wifi_symbol_status.pack(pady=6,padx=2,side="left")
                  
class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=1024,height=573,bg_color="black",fg_color="transparent",border_width=2,border_color="blue")

        self.clock_frame = customtkinter.CTkFrame(self,bg_color="black",fg_color="black",height=120,width=200)
        self.clock_frame.pack(side="top",pady=10) 

        self.clock_frame.clock = customtkinter.CTkLabel(master=self.clock_frame, height=40,width=100,
        text="__:__",bg_color="transparent",fg_color="transparent",text_color="white",font=("CTkFont",72),anchor="s")
        self.clock_frame.clock.place(y=0,relx=0.5,anchor="n")

        self.clock_frame.clock_date = customtkinter.CTkLabel(master=self.clock_frame,text="date",font=("CTkFont",32),
        fg_color="black",bg_color="black",text_color="gray40")
        self.clock_frame.clock_date.place(anchor="n",relx=0.5,y=66)

        

    def set_clock_text(self, clock_time, clock_date):
         self.clock_frame.clock.configure(text=clock_time)
         self.clock_frame.clock_date.configure(text=clock_date)
         
class ExitMenuFrame(customtkinter.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(corner_radius=20,fg_color="gray10",bg_color="black")

        self.exit_menu_prompt = customtkinter.CTkLabel(self, width=580,height=100,text="Are you sure you want to exit?",font=("CTkFont",34))
        self.exit_menu_prompt.configure(corner_radius=12,fg_color="gray10",text_color="white")
        self.exit_menu_prompt.place(anchor = "n", relx=0.5,y=10)

        self.exit_menu_cancel_button = customtkinter.CTkButton(self, width=110, height=120, text="Cancel",command=exitCancelExit,fg_color="blue")
        self.exit_menu_cancel_button.configure(font=("CTkFont",34))
        self.exit_menu_cancel_button.pack(padx=20,pady=30,fill="x",side="left",expand=True,anchor="s")

        self.exit_menu_exit_button = customtkinter.CTkButton(self, width=110,height=120,text="Exit",command=exitConfirmExit,fg_color="dark red")
        self.exit_menu_exit_button.configure(font=("CTkFont",34))
        self.exit_menu_exit_button.pack(padx=20,pady=30,fill="x",side="right",expand=True,anchor="s")

#WINDOW        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("volvoPi")
        self.geometry("1024x600+300+150")
        self.maxsize(width=1920,height=1080)
        self.minsize(width=600,height=600)
        #self._set_appearance_mode("dark")
        #self.overrideredirect(True)

        self.top_bar_frame = TopBarFrame(master=self)
        self.top_bar_frame.pack(fill = "x")
        
        self.home_frame = HomeFrame(master=self)
        self.home_frame.pack(pady=0, fill = "both",expand=True)

        self.exit_menu = ExitMenuFrame(master=self)


app = App()

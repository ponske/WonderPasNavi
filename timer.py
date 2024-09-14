import customtkinter
import datetime
import subprocess

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('timer app')
        self.geometry('400x500')

        time_now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.label_time=customtkinter.CTkLabel(self, text=time_now)
        self.label_time.grid(row=1,column=0,padx=20,pady=20)

        self.label_operation=customtkinter.CTkLabel(self, text="")
        self.label_operation.grid(row=1, column=1, padx=20, pady=20)

        self.button=customtkinter.CTkButton(self, text="OFF", command=self.button_pressed)
        self.button.grid(row=0,columnspan=2,padx=20,pady=20, sticky = "ew")
        self.flag_timer = 0

        self.update_current_time()
        print('test')

    def button_pressed(self):
        # 0: OFF / 1: ON
        if self.button.cget("text") == "ON":
            self.button.configure(text="OFF")
        else:
            self.button.configure(text="ON")
        
        
    def update_current_time(self):
        
        self.label_time.configure(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.check_opening()
        self.after(1000,self.update_current_time)

    def check_opening(self):
        opening_time=datetime.time(hour=8, minute=45, second=0)
        now_time=datetime.datetime.now().time().replace(microsecond=0)
        if now_time == opening_time:
            self.label_operation.configure(text = "It's opening hour!!!!!!!!!!")
            self.execute_collectiongjob()
        elif now_time < opening_time:
            self.label_operation.configure(text = "It's not open yet...")
        else:
            self.label_operation.configure(text = "It's already Open!")

    def execute_collectingjob(self):
        cmd='/home/ubuntu/origin_collectwaitingtime/WonderPasNavi/collectdata.sh'
        subprocess.run(['gnome-terminal', '--', cmd])
        
    
app = App()
app.mainloop()

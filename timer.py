import customtkinter
import datetime
import subprocess
import requests
import os
from dotenv import load_dotenv

load_dotenv()

LINE_NOTIFY_TOKEN = os.getenv('line_notify_token')

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("themes/cherry.json")

class App(customtkinter.CTk):
    def __init__(self):

        super().__init__()

        self.title('Mini Scheduler')
        self.geometry('800x300')

        time_now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.label_time=customtkinter.CTkLabel(self, text=time_now)
        self.label_time.grid(row=1,column=0,padx=20,pady=20)

        self.label_operation=customtkinter.CTkLabel(self, text="")
        self.label_operation.grid(row=1, column=1, padx=20, pady=20)

        self.label_app=customtkinter.CTkLabel(self,text="おはようございます。タイマーを起動してください")
        self.label_app.grid(row=2, column=1, padx=20, pady=20)

        self.button=customtkinter.CTkButton(self, text="OFF クリックでON", command=self.button_pressed)
        self.button.grid(row=0,columnspan=2,padx=20,pady=20, sticky = "ew")
        self.flag_timer = 0
        self.time_off = {'hour': 0,
                         'minute': 0,
                         'second': 0,
                         'microsecond': 9}
        self.time_open = {'hour': 9,
                         'minute': 00,
                         'second': 00}
        self.opening_time = datetime.time(hour=self.time_off['hour'], minute=self.time_off['minute'], 
                                          second=self.time_off['second'], microsecond=self.time_off['microsecond'])

        hours=[]
        for i in range(24):
            hours.append(str(i))
        combobox_hour = customtkinter.CTkComboBox(self, values=hours, command=self.combobox_hour_callback)
        combobox_hour.set("9")
        combobox_hour.grid(row=1,column=2, padx=20, pady=20)

        minutes=[]
        for i in range(60):
            minutes.append(str(i))
        combobox_minute = customtkinter.CTkComboBox(self, values=minutes, command=self.combobox_minute_callback)
        combobox_minute.set("0")
        combobox_minute.grid(row=1,column=3, padx=20, pady=20)

        self.update_current_time()

    def button_pressed(self):
        # 0: OFF / 1: ON
        if self.button.cget("text") == "ON クリックでOFF":
            self.button.configure(text="OFF クリックでON")
            self.opening_time = datetime.time(hour=self.time_off['hour'], minute=self.time_off['minute'], 
                                              second=self.time_off['second'], microsecond=self.time_off['microsecond'])
            self.label_app.configure(text="")
        else:
            self.button.configure(text="ON クリックでOFF")
            self.opening_time = datetime.time(hour=self.time_open['hour'], minute=self.time_open['minute'], second=self.time_open['second'])
            
    def update_current_time(self):
        
        self.label_time.configure(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.check_opening()
        self.after(1000,self.update_current_time)

    def check_opening(self):
        current_time = datetime.datetime.now().time().replace(microsecond=0)
        if current_time == self.opening_time:
            self.label_operation.configure(text = "It's opening hour!!!!!!!!!!")
            self.label_app.configure(text="データ収集中")
            try:
                self.execute_collectingjob()
            except:
                self.label_app.configure(text="ジョブ実行中に問題が発生")
            else:
                self.label_app.configure(text="データ収集ジョブ停止中")

        elif self.opening_time == datetime.time(hour=0, minute=0, second=0, microsecond=9):
            self.label_operation.configure(text = "Timer is OFF.")
        elif current_time < self.opening_time:
            self.label_operation.configure(text = "It's not open yet...")
        else:
            self.label_operation.configure(text = "It's already Open!")

    def execute_collectingjob(self):
        notification_message = 'ジョブ実行開始'
        line_notify_api='https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
        data = {'message': f'message: {notification_message}'}
        requests.post(line_notify_api, headers = headers, data = data)
        cmd='/home/ubuntu/origin_collectwaitingtime/WonderPasNavi/collectdata.sh'
        
        ret = subprocess.run(['gnome-terminal', '--', cmd], capture_output=True, text=True)

        if ret.returncode == 0:
            return 0
        else:
            return ret.returncode


    def combobox_hour_callback(self, choice):
        
        self.time_open["hour"] = int(choice)
        self.opening_time = datetime.time(hour=self.time_open['hour'], minute=self.time_open['minute'], second=self.time_open['second'])

    def combobox_minute_callback(self, choice):
        self.time_open["minute"] = int(choice)
        self.opening_time = datetime.time(hour=self.time_open['hour'], minute=self.time_open['minute'], second=self.time_open['second'])

    
app = App()
app.mainloop()

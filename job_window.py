#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk
from tkinter import messagebox

import time
import datetime

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('待ち時間収集バッチ')
        self.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):
        self.lb_title=tk.Label(self)
        self.lb_title["text"]="待ち時間収集ジョブ実行画面"
        self.lb_result=tk.Label(self)
        self.lb_result["text"]="待ち時間収集ジョブ実行結果："

        self.button_onetimejob=tk.Button(text="スポット実行",command=self.cmd_onetimejob)

        self.lb_title.grid()
        self.lb_result.grid()
        self.button_onetimejob.grid()

    def cmd_onetimejob(self):
        rt=collectwaitingtime()
        self.lb_result["text"]='待ち時間収集ジョブ実行結果：{}'.format(rt)

def collectwaitingtime():
    # WebDriverのセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # ページにアクセス
        driver.get('https://www.tokyodisneyresort.jp/tds/realtime/attraction.html')
        time.sleep(5)  # JavaScriptがロードされるのを待つ

        # 要素を探す
        elements_waiting_time = driver.find_elements(By.CLASS_NAME, 'time')
        operation=driver.find_elements(By.CLASS_NAME, 'operation')
        attr_name=[]
        for i in range(34):
            attr_name.append(driver.find_elements(By.CSS_SELECTOR, '#pbBlock5805924 > div > ul > li:nth-child('+str(i+1)+') > a > div > div.headingArea > h3'))

        for element in elements_waiting_time:
            print(element.text)  
        for op in operation:
            print(op.text)
        for atnm in attr_name:
            print(atnm[0].text)

        #aタグを検出
        t_id=(227,219,244,230,245,246,243,232,228,218,233,234,231,247,222,229,242,255,256,257,258,236,220,235,226,202,239,238,237,240,221,241,224,223,)
        for t in t_id:
            link = driver.find_element(By.CSS_SELECTOR, 'a[href="/tds/attraction/detail/'+str(t)+'/"]')
            if link:
                realtime_info_elements = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'a[href="/tds/attraction/detail/{t}/"] .realtimeInformation'))
                )
                if realtime_info_elements:
                    waiting_time_element = realtime_info_elements.find_elements(By.CLASS_NAME, 'waitingtime')
                    if waiting_time_element:
                        print('ID{}:存在する'.format(t))
                        waiting_time=realtime_info_elements.find_elements(By.CLASS_NAME, 'time')
                        print('{}分待ち'.format(waiting_time))
                    else:
                        print('ID{}:存在しない'.format(t))
                
            else:
                print('指定したIDのアトラクションが見つからない')
    finally:
        driver.quit()  # ブラウザを閉じる

#root=tk.Tk()
#app=Application(master=root)
root=Application()
root.mainloop()
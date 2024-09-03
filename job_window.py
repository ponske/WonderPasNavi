#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tkinter as tk
from tkinter import messagebox

import psycopg2

import time
import datetime

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('待ち時間収集バッチ')
        self.geometry("700x500")

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        self.lb_title=tk.Label(self)
        self.lb_title["text"]="待ち時間収集ジョブ実行画面"
        self.lb_title["font"]=("Helvetica",20)

        current=datetime.datetime.now()
        self.lb_time=tk.Label(self)
        self.lb_time["text"]=current
        self.lb_time["fg"]="green"
        self.lb_time["bg"]="black"
        self.lb_time["font"]=("Helvetica",12)
        self.lb_result=tk.Label(self)
        self.lb_result["text"]="両パーク待ち時間収集ジョブスポット実行"
        self.lb_result_1hour=tk.Label(self)
        self.lb_result_1hour["text"]="両パーク待ち時間収集ジョブ実行"

        self.button_onetimejob=tk.Button(text="実行",command=self.cmd_onetimejob)
        self.button_job=tk.Button(text="実行",command=self.cmd_onehourjob)

        self.lb_title.grid(column=0,columnspan=2,row=0,padx=20,pady=20)
        self.lb_time.grid(row=0,column=4,sticky="e",padx=10,pady=10)
        self.lb_result.grid(column=0,row=1,padx=10,pady=10)
        self.button_onetimejob.grid(column=1,row=1,padx=10,pady=10)
        self.lb_result_1hour.grid(column=0,row=2,padx=10,pady=10)
        self.button_job.grid(column=1,row=2,padx=10,pady=10)

    def update_time(self):
        # 現在の時刻を取得してラベルを更新
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.lb_time["text"] = current_time
        # 1000ミリ秒後に自身を呼び出し、時刻更新を繰り返す
        self.after(1000, self.update_time)

    def cmd_onetimejob(self):
        rt_sea=collectwaitingtime_sea()
        rt_land=collectwaitingtime_land()
        self.lb_result["text"]='待ち時間収集ジョブスポット実行：{} {}'.format(rt_sea,rt_land)
    
    def cmd_onehourjob(self):
        for r in range(120):
            rt_sea=collectwaitingtime_sea()
            rt_land=collectwaitingtime_land()
            self.lb_result_1hour["text"]='待ち時間収集ジョブ実行{}回目：{} {}'.format(r, rt_sea, rt_land)
            time.sleep(30)

def collectwaitingtime_sea():
    # WebDriverのセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # ページにアクセス
        driver.get('https://www.tokyodisneyresort.jp/tds/realtime/attraction.html')
        time.sleep(5)  # JavaScriptがロードされるのを待つ

        # 要素を探す
        attr_name=[]
        for i in range(34):
            attr_name.append(driver.find_elements(By.CSS_SELECTOR, '#pbBlock5805924 > div > ul > li:nth-child('+str(i+1)+') > a > div > div.headingArea > h3'))
        index_atrnm=0

        #aタグを検出
        t_id=(227,219,244,230,245,246,243,232,228,218,233,234,231,247,222,229,242,255,256,257,258,236,220,235,226,202,239,238,237,240,221,241,224,223,)
        wait_time=[]
        ope_cond=[]
        for t in t_id:
            link = driver.find_element(By.CSS_SELECTOR, 'a[href="/tds/attraction/detail/'+str(t)+'/"]')
            if link:
                realtime_info_elements = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'a[href="/tds/attraction/detail/{t}/"] .realtimeInformation'))
                )
                if realtime_info_elements:
                    waiting_time_element = realtime_info_elements.find_elements(By.CLASS_NAME, 'waitingtime')
                    if waiting_time_element:
                        waiting_time=realtime_info_elements.find_elements(By.CLASS_NAME, 'time')
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if len(operation) > 0:
                            ope_cond.append(operation[0].text)
                        else:
                            ope_cond.append("★運営中") #謎 なぜかタグが見つからない --> issueに挙げる
                        if len(waiting_time) != 0:
                            wait_time.append(waiting_time[0].text)
                        else:
                            wait_time.append("999") #施設にて確認
                    else:
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if operation:
                            ope_cond.append(operation[0].text)
                        else:
                            ope_cond.append("★運営状態不明")
                        wait_time.append("999")

            else:
                print('指定したIDのアトラクションが見つからない')
            index_atrnm=index_atrnm+1

        ins_waittime(t_id,wait_time,ope_cond)
        return 0
    except Exception as e:
        print(f'エラーが発生しました: {e}')
        return 999
    finally:
        driver.quit()  # ブラウザを閉じる

def ins_waittime(t_id,wait_time,ope_cond):
    try:
        conn=psycopg2.connect(
            host="localhost",
            database="wonderpasnavi",
            user="wpnuser",
            password="wpnuser"
        )

        current=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur=conn.cursor()
        for i in range(34):
            cur.execute("""
                        INSERT INTO trk_waitingtime (attr_id,waitingperiod,at_t)
                        VALUES(%s,%s,%s);
                        """,(t_id[i],wait_time[i],current,))
            cur.execute("""
                        INSERT INTO trk_operation (attr_id,condition,at_t)
                        VALUES(%s,%s,%s);
                        """,(t_id[i],ope_cond[i],current,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f'DBでエラーが発生しました: {e}')

def collectwaitingtime_land():
    # WebDriverのセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        # ページにアクセス
        driver.get('https://www.tokyodisneyresort.jp/tdl/realtime/attraction.html')
        time.sleep(5)  # JavaScriptがロードされるのを待つ

        html_content = driver.page_source

        # HTMLコンテンツをファイルに書き出す
        with open('samplehtml_land.txt', 'w', encoding="utf-8") as f:
            f.write(html_content)

        # 要素を探す
        attr_name=[]
        for i in range(38):
            attr_name.append(driver.find_elements(By.CSS_SELECTOR, '#pbBlock5805786 > div > ul > li:nth-child('+str(i+1)+') > a > div > div.headingArea > h3'))
        
        index_atrnm=0

        #aタグを検出
        t_id=(151,191,154,152,153,155,156,157,158,159,161,160,162,163,173,172,170,165,166,169,197,164,168,174,171,167,179,181,178,194,180,176,175,183,195,185,196,189,)
        wait_time=[]
        ope_cond=[]
        for t in t_id:
            link = driver.find_element(By.CSS_SELECTOR, 'a[href="/tdl/attraction/detail/'+str(t)+'/"]')
            if link:
                realtime_info_elements = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, f'a[href="/tdl/attraction/detail/{t}/"] .realtimeInformation'))
                )
                if realtime_info_elements:
                    waiting_time_element = realtime_info_elements.find_elements(By.CLASS_NAME, 'waitingtime')
                    if waiting_time_element:
                        #print('ID{}  {}  :存在する'.format(t, attr_name[index_atrnm][0].text),end='\t')
                        waiting_time=realtime_info_elements.find_elements(By.CLASS_NAME, 'time')
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if len(operation) > 0:
                            ope_cond.append(operation[0].text)
                        else:
                            ope_cond.append("★運営中") #謎 なぜかタグが見つからない --> issueに挙げる
                        if len(waiting_time) != 0:
                            #print('{}分待ち'.format(waiting_time[0].text))
                            wait_time.append(waiting_time[0].text)
                        else:
                            wait_time.append("999") #施設にて確認
                            #print('現地にて確認')
                    else:
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if operation:
                            ope_cond.append(operation[0].text)
                            #print('ID{}  {}  :存在しない  {}'.format(t, attr_name[index_atrnm][0].text, operation[0].text))
                        else:
                            #print('ID{}  {}  :存在しない  ★運営状態不明'.format(t, attr_name[index_atrnm][0].text))
                            ope_cond.append("★運営状態不明")
                        wait_time.append("999")

            else:
                print('指定したIDのアトラクションが見つからない')
            index_atrnm=index_atrnm+1
        ins_waittime(t_id,wait_time,ope_cond)
        return 0
    except Exception as e:
        print(f'エラーが発生しました: {e}')
        return 999
    finally:
        driver.quit()  # ブラウザを閉じる

root=Application()
root.mainloop()
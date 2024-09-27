from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import time 
import datetime

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
                            write_log('ID: ' + str(t) + '[1]: operation 情報あり')
                        else:
                            ope_cond.append("★運営中") #謎 なぜかタグが見つからない --> issueに挙げる
                            write_log('ID: ' + str(t) + '[2]: operation タグが見つからない')
                        if len(waiting_time) != 0:
                            wait_time.append(waiting_time[0].text)
                            write_log('ID: ' + str(t) + '[3]: 待ち時間あり')
                        else:
                            wait_time.append("999") #施設にて確認
                    else:
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if operation:
                            ope_cond.append(operation[0].text)
                            write_log('ID: ' + str(t) + '[5]: 別階層で探索 operation 情報あり')
                        else:
                            ope_cond.append("★運営状態不明")
                            write_log('ID: ' + str(t) + '[6]: 運営状態が不明')
                        wait_time.append("999")

            else:
                print('指定したIDのアトラクションが見つからない')
                write_log('ID: ' + str(t) + '指定したIDのアトラクションが見つからない')
            index_atrnm=index_atrnm+1

        ins_waittime(t_id,wait_time,ope_cond)
        return 0
    except Exception as e:
        error_msg = f'エラーが発生しました: {e}'
        write_log('エラーが発生した')
        write_log(error_msg)
        return 999
    finally:
        driver.quit()  # ブラウザを閉じる

def write_log(content):
    log_name="log/" + str(datetime.date.today()) + ".log"
    file = open(log_name, "a")
    file.write(datetime.datetime.now().strftime("%Y/%M/%D %H:%M") +"   ")
    file.write(content)
    file.write("\r")
    file.close()

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
        for i in range(len(t_id)):
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
        error_msg = f'DBでエラーが発生しました: {e}'
        write_log('エラーが発生した')
        write_log(error_msg)

def collectwaitingtime_land():
    # WebDriverのセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        # ページにアクセス
        driver.get('https://www.tokyodisneyresort.jp/tdl/realtime/attraction.html')
        time.sleep(5)  # JavaScriptがロードされるのを待つ

        html_content = driver.page_source

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
                        waiting_time=realtime_info_elements.find_elements(By.CLASS_NAME, 'time')
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if len(operation) > 0:
                            ope_cond.append(operation[0].text)
                            write_log('ID: ' + str(t) + '[1]: operation 情報あり')
                        else:
                            ope_cond.append("★運営中")
                            write_log('ID: ' + str(t) + '[2]: operation タグが見つからない')
                        if len(waiting_time) != 0:
                            wait_time.append(waiting_time[0].text)
                            write_log('ID: ' + str(t) + '[3]: 待ち時間あり')
                        else:
                            wait_time.append("999")
                            write_log('ID: ' + str(t) + '[4]: 施設にて確認')
                    else:
                        operation=link.find_elements(By.CLASS_NAME, 'operation')
                        if operation:
                            ope_cond.append(operation[0].text)
                            write_log('ID: ' + str(t) + '[5]: 別階層で探索 operation 情報あり')
                        else:
                            ope_cond.append("★運営状態不明")
                            write_log('ID: ' + str(t) + '[6]: 運営状態が不明')
                        wait_time.append("999")

            else:
                print('指定したIDのアトラクションが見つからない')
            index_atrnm=index_atrnm+1
        ins_waittime(t_id,wait_time,ope_cond)
        return 0
    except Exception as e:
        error_msg = f'エラーが発生しました: {e}'
        write_log('エラーが発生した')
        write_log(error_msg)
        return 999
    finally:
        driver.quit()  # ブラウザを閉じる
r=1
while True:
    write_log(str(r + 1) + '回目の実行開始--------------------------------------------' 
              + '\r' + '[Sea] データ収集開始')
    rt_sea=collectwaitingtime_sea()
    if rt_sea == 0:
        write_log('[Sea] データ収集完了')
    elif rt_sea == 999:
        write_log('[Sea] Error Occurred')
    write_log('[Land] データ収集開始')
    rt_land=collectwaitingtime_land()
    write_log('[Land] データ収集完了')
    time.sleep(5)
    if datetime.datetime.now().strftime("%H%M%S") > datetime.time(hour=21,minute=5).strftime("%H%M%S"):
        break 
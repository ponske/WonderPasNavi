from django.core.management.base import BaseCommand
from graphviewer.models import Image
import os.path
import pandas as pd
import psycopg2 as pg
import matplotlib.pyplot as plt
import japanize_matplotlib
import io
import dotenv
import cloudinary
from cloudinary.uploader import upload
import datetime


class Command(BaseCommand):
    help = 'Generates and updates attraction images in the database'
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    today_filename = datetime.datetime.now().strftime('%Y%m%d')
    day = datetime.datetime.now().strftime('%d')
    #date_end = str(int(day) + 1)
    today ='2024-09-21'
    today_filename = '20240921'
    day = '21'
    

    def handle(self, *args, **options):
        dotenv.load_dotenv()

        # Cloudinaryの設定
        cloudinary.config(
            cloud_name=os.getenv('CLOUD_NAME'),
            api_key=os.getenv('API_KEY'),
            api_secret=os.getenv('API_SECRET')
        )
        
        attraction = {
            '227': 'ディズニーシー・トランジットスチーマーライン',
            '219': 'ソアリン：ファンタスティック・フライト',
            '244': 'フォートレス・エクスプロレーション',
            '230': 'ヴェネツィアン・ゴンドラ',
            '245': 'フォートレス・エクスプロレーション"ザ・レオナルドチャレンジ"',
            '246': 'タートル・トーク',
            '243': 'タワー・オブ・テラー',
            '232': 'ディズニーシー・エレクトリックレールウェイ',
            '228': 'ディズニーシー・トランジットスチーマーライン',
            '218': 'トイ・ストーリー・マニア！',
            '233': 'ビッグシティ・ヴィークル',
            '234': 'アクアトピア',
            '231': 'ディズニーシー・エレクトリックレールウェイ',
            '247': 'ニモ＆フレンズ・シーライダー',
            '222': 'インディ・ジョーンズ®・アドベンチャー： クリスタルスカルの魔宮',
            '229': 'ディズニーシー・トランジットスチーマーライン',
            '242': 'レイジングスピリッツ',
            '255': 'アナとエルサのフローズンジャーニー NEW',
            '256': 'ラプンツェルのランタンフェスティバル NEW',
            '257': 'ピーターパンのネバーランドアドベンチャー NEW',
            '258': 'フェアリー・ティンカーベルのビジーバギー NEW',
            '236': 'キャラバンカルーセル',
            '220': 'ジャスミンのフライングカーペット',
            '235': 'シンドバッド・ストーリーブック・ヴォヤッジ',
            '226': 'マジックランプシアター',
            '202': 'アリエルのプレイグラウンド',
            '239': 'ジャンピン・ジェリーフィッシュ',
            '238': 'スカットルのスクーター',
            '237': 'フランダーのフライングフィッシュコースター',
            '240': 'ブローフィッシュ・バルーンレース',
            '221': 'マーメイドラグーンシアター',
            '241': 'ワールプール',
            '224': '海底2万マイル',
            '223': 'センター・オブ・ジ・アース',
            '151': 'オムニバス',
            '191': 'ペニーアーケード',
            '154': 'ウエスタンリバー鉄道',
            '152': 'カリブの海賊',
            '153': 'ジャングルクルーズ：ワイルドライフ・エクスペディション',
            '155': 'スイスファミリー・ツリーハウス',
            '156': '魅惑のチキルーム：スティッチ・プレゼンツ“アロハ・エ・コモ・マイ！”',
            '157': 'ウエスタンランド・シューティングギャラリー',
            '158': 'カントリーベア・シアター',
            '159': '蒸気船マークトウェイン号',
            '161': 'トムソーヤ島いかだ',
            '160': 'ビッグサンダー・マウンテン',
            '162': 'スプラッシュ・マウンテン',
            '163': 'ビーバーブラザーズのカヌー探険',
            '173': 'アリスのティーパーティー',
            '172': 'イッツ・ア・スモールワールド',
            '170': 'キャッスルカルーセル',
            '165': '白雪姫と七人のこびと',
            '166': 'シンデレラのフェアリーテイル・ホール',
            '169': '空飛ぶダンボ',
            '197': '美女と野獣“魔法のものがたり”',
            '164': 'ピーターパン空の旅',
            '168': 'ピノキオの冒険旅行',
            '174': 'プーさんのハニーハント',
            '171': 'ホーンテッドマンション',
            '167': 'ミッキーのフィルハーマジック',
            '179': 'ガジェットのゴーコースター',
            '181': 'グーフィーのペイント＆プレイハウス',
            '178': 'チップとデールのツリーハウス',
            '194': 'トゥーンパーク',
            '180': 'ドナルドのボート',
            '176': 'ミニーの家',
            '175': 'ロジャーラビットのカートゥーンスピン',
            '183': 'スター・ツアーズ：ザ・アドベンチャーズ・コンティニュー',
            '195': 'スティッチ・エンカウンター',
            '185': 'バズ・ライトイヤーのアストロブラスター',
            '196': 'ベイマックスのハッピーライド',
            '189': 'モンスターズ・インク“ライド＆ゴーシーク！”'
        }
        try:
            conn = pg.connect(
                host = os.getenv('HOST'),
                database = os.getenv('DATABASE'),
                user = os.getenv('USER'),
                password = os.getenv('PASSWORD')
            )
            
            cursor = conn.cursor()
            data=[]
            for attr_id in attraction:    
                cursor.execute("""
                            SELECT at_t, waitingperiod FROM trk_waitingtime
                            WHERE at_t >= '2024-09-21' AND
                            at_t < '2024-09-22' AND
                            attr_id = %s
                            
                            ORDER BY at_t;
                            """, (attr_id,))
                data.append(cursor.fetchall())
            cursor.close()
            conn.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
        
        
        for i, (attr_id, attr_name) in enumerate(attraction.items()):
            df = pd.DataFrame(data[i], columns =['at_t','waitingperiod'])
            df = df[df['waitingperiod'] != 999]
            if not df.empty:
                fig, ax = plt.subplots()
                df.plot(ax=ax, x='at_t',y='waitingperiod')

                ax.set_xlabel('時刻')
                ax.set_ylabel('待ち時間')
                ax.set_title(attr_name)
                plt.xticks(rotation=45)
                plt.tight_layout()
                image_url = upload_image_to_cloudinary(fig, f'graph_{self.today_filename}_{attr_id}')
                Image.objects.create(
                    attraction_id=attr_id,
                    image = image_url
                )
                plt.close(fig)

        self.stdout.write(self.style.SUCCESS('Succcessfully updated images'))

def upload_image_to_cloudinary(fig, public_id):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    response = upload(buf, folder='attraction_graphs', public_id=public_id)
    buf.close()
    return response['url']
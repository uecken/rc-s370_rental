import binascii
import nfc
import os

class MyCardReader(object):
    def on_connect(self, tag):
        print("【 Touched 】")

        #タグ情報を全て表示
        print(tag)

        #IDmのみ取得して表示
        self.idm = binascii.hexlify(tag._nfcid)
        print("IDm : " + str(self.idm))


        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb')
        try:
            clf.connect(rdwr={'on-connect': self.on_connect})
        finally:
            clf.close()
            return self.idm

import gspread
import json
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
import datetime
class GS_Rentaller(object):
    Kaiin_sheet = "Kaiin_DB"
    Buppin_sheet = "Buppin_DB"
    Kashidashi_sheet = "Kashidashi_DB"

    def __init__(self):
        #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        #認証情報設定
        #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('rental-kasasagi-58fe527d03b9.json', self.scope)

        #OAuth2の資格情報を使用してGoogle APIにログインします。
        self.gc = gspread.authorize(self.credentials)

        #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
        self.SPREADSHEET_KEY = '1NE4CNVoSq8iumlyjiDO6xYrsgPifgmVNrhnZG69z8Zg'


    
    def regist_thing(self,thing_id,thing_name=False,price=False,regist_place=False,regist_date=False):
        self.worksheet = self.gc.open_by_key(self.SPREADSHEET_KEY).worksheet("Buppin_DB") #sheet1
        ws = self.worksheet
        
        check = ws.find(thing_id) # in case ID collision
        if(check): # in case ID collision
            print("==This has been already registered")
            print("Skip registration. If regist it, please delete the ID on DB==")
        else:
            col = 2 #Row of Buppin_ID
            worksheet.update_cell(self.get_last_row_idx(ws,col)+1,col, thing_id) #Row,Col,ID

    def get_last_row_idx(self,ws,col):
        #A列のデータを配列として取得
        A_COL_ARRAY = ws.col_values(col)
        print("len(A_COL_ARRAY); " + str(len(A_COL_ARRAY)))

        #最下行インデックスを取得
        LAST_ROW_IDX = len(A_COL_ARRAY)
        return LAST_ROW_IDX



    def regist_card(self,card_id,name=False,charge_money=False,phone_num=False,regist_place=False,regist_date=False):
        self.worksheet = self.gc.open_by_key(self.SPREADSHEET_KEY).worksheet("Kaiin_DB") #sheet1
        ws = self.worksheet
        
        check = ws.find(card_id) # in case ID collision
        if(check): # in case ID collision
            print("==This has been already registered")
            print("Skip registration. If regist it, please delete the ID on DB==")
            return
        else:
            col = 2 #Row of Kaiinn_ID
            ws.update_cell(self.get_last_row_idx(ws,col)+1,col, card_id) #Row,Col,ID

    def rent_thing(self,cr,card_id=False,thing_id=False,rent_date=False,rent_place=False,return_date=False,return_check=False,return_place=False): 
        now = datetime.datetime.now()
        rent_date = now.strftime('%Y-%m-%d %H:%M:%S')
        rent_place = "MiraiKyoshitu"
        return_date = (now + datetime.timedelta(days=14)).strftime('%Y-%m-%d %H:%M:%S') 
        return_check = ""
        return_place = ""

        # === Check card if registerd ===
        card_id = cr.read_id().decode() # Wait for NFC touch

        self.worksheet = self.gc.open_by_key(self.SPREADSHEET_KEY).worksheet("Kaiin_DB")
        if(self.worksheet.find(card_id)): # ID existance check
            print("===You are member of Kasasagi ICT Sharing Economy===")
        else:
            print("===You are not member")
            return

        # === Regist things ====
        self.worksheet = self.gc.open_by_key(self.SPREADSHEET_KEY).worksheet("Kashidashi_DB")    
        ws = self.worksheet
        while True:
            thing_id = cr.read_id().decode() # Wait for NFC touch
        
            check = ws.find(thing_id) # in case ID collision
            if(check): # in case ID collision
                print("== This has been already renterd. Check the ID on kashidashi_DB ==")
            else:
                col = 2
                ws.append_row(['',card_id,thing_id,rent_date,rent_place,return_date,return_check,return_place])
                #row = self.get_last_row_idx(ws,col)+1
                #ws.update_cell(row,2, card_id) #Row,Col,ID
                #ws.update_cell(row,3, thing_id) #Row,Col,ID
                #ws.update_cell(row,4, rent_date) #Row,Col,ID
                #ws.update_cell(row,5, rent_place) #Row,Col,ID
                #ws.update_cell(row,6, return_date) #Row,Col,ID
                #ws.update_cell(row,7, return_check) #Row,Col,ID
                #ws.update_cell(row,8, return_place) #Row,Col,ID

        # === End registration by re-congnition the ID card ===
        if(card_id == cr.read_id().decode()): # Wait for NFC touch
            print("Same ID card. Thing register is finishied.")


if __name__ == '__main__':
    cr = MyCardReader()
    rl = GS_Rentaller()

    print("Input 1(rental), 2(return), 3(regist card), 4(regist thing)")
    mode_num = input()
    if mode_num == "1":
        print("Start rental. Please touch your card)")
        #read_id = cr.read_id().decode() #Wait for NFC touch
        rl.rent_thing(cr)
    elif mode_num =="2":
        pass
        #cr.return_thing()
    elif mode_num =="3":
        read_id = cr.read_id().decode() #Wait for NFC touch
        rl.regist_card(read_id)
    elif mode_num =="4": 
        while True:
            print("Please Touch")
            read_id = cr.read_id().decode() #Wait for NFC touch
            rl.regist_thing(read_id)
            print("【 Released 】")


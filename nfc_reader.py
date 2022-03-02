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
        #print("IDm : " + str(self.idm))


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

    
    def regist_thing(self,thing_id,thing_name=False,price=False,place=False):
        worksheet = self.gc.open_by_key(self.SPREADSHEET_KEY).worksheet(self.Buppin_sheet) #sheet1
        ws = worksheet

        
        check = ws.find(thing_id) # in case ID collision
        if(check): # in case ID collision
            print("This is has been already registered")
            print("If continue, input 1.")
            msg = input()
            if(msg != "1"):
                print("Stop registration")
                return false

        col = 2 #Row of Buppin_ID
        worksheet.update_cell(self.get_last_row_idx(ws,col)+1,col, thing_id) #Row,Col,ID

    def get_last_row_idx(self,ws,col):
        #A列のデータを配列として取得
        A_COL_ARRAY = ws.col_values(col)
        print("len(A_COL_ARRAY); " + str(len(A_COL_ARRAY)))

        #最下行インデックスを取得
        LAST_ROW_IDX = len(A_COL_ARRAY)
        return LAST_ROW_IDX
        



if __name__ == '__main__':
    cr = MyCardReader()
    rl = GS_Rentaller()

    print("Input 1(rental), 2(return), 3(regist card), 4(regist thing)")
    mode_num = input()
    if mode_num == "1":
        print("Start rental. Please touch your card)")
        #cr.rental_thing()
    elif mode_num =="2":
        pass
        #cr.return_thing()
    elif mode_num =="3":
        pass
        #cr.regist_card()
    elif mode_num =="4": 
        while True:
            print("Please Touch")
            read_id_byte = cr.read_id() #Wait for NFC touch
            rl.regist_thing(read_id_byte.decode())
            print("【 Released 】")


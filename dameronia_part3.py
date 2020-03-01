# 「逆転オセロニア」を画像解析して自動ダメージ計算 part3 (キャラ識別編)
# https://qiita.com/toyotoyo_/items/2ecbe7205b828db74bcb

# 抽出処理実行


from PIL import ImageGrab

#キャラ駒の大きさ
CHARACTER_SIZE_X=50
CHARACTER_SIZE_Y=50
#左上キャラの開始座標
CHARACTER_START_X=760
CHARACTER_START_Y=310
#キャラ駒の間隔
CHARACTER_SPACE_X=116
CHARACTER_SPACE_Y=108

#デッキ編成画面
for row in range(4):
    for col in range(4):
        url_img = "img\\character\\hensei" + str(col) + "_" + str(row) + ".png"
        print(url_img)
        ImageGrab.grab(bbox=(CHARACTER_START_X+CHARACTER_SPACE_X*row, CHARACTER_START_Y+CHARACTER_SPACE_Y*col, CHARACTER_START_X+CHARACTER_SIZE_X+CHARACTER_SPACE_X*row, CHARACTER_START_Y+CHARACTER_SIZE_Y+CHARACTER_SPACE_Y*col)).save(url_img)




# 戦闘画面からのデータ抽出

from PIL import ImageGrab

#キャラ駒の大きさ
CHARACTER_SIZE_X=50
CHARACTER_SIZE_Y=50
#左キャラの開始座標
TEGOMA_START_X=737
TEGOMA_START_Y=870
#キャラ駒の間隔
TEGOMA_SPACE_X=132

#戦闘画面の手駒
for row in range(4):
    url_img = "img\\tegoma\\tegoma" + str(row) + ".png"
    print(url_img)
    ImageGrab.grab(bbox=(TEGOMA_START_X+TEGOMA_SPACE_X*row, TEGOMA_START_Y, TEGOMA_START_X+CHARACTER_SIZE_X+TEGOMA_SPACE_X*row, TEGOMA_START_Y+CHARACTER_SIZE_Y)).save(url_img)




# 類似度判断処理

import cv2
import os
IMG_DIR = 'img\\character\\'
TEGOMA_IMG_PATH = "img\\tegoma\\tegoma1.png"
# 手駒画像を読み込みヒストグラム作成
target_img = cv2.imread(TEGOMA_IMG_PATH)
target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])

# characterフォルダの中にあるデッキ編成画像と類似度を比較していく
files = os.listdir(IMG_DIR)
for file in files:
    comparing_img_path = IMG_DIR + file
    # デッキ編成画像を読み込みヒストグラム作成
    comparing_img = cv2.imread(comparing_img_path)
    comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])
    # 手駒とデッキ編成画像のヒストグラム比較を行う
    ret = cv2.compareHist(target_hist, comparing_hist, 0)
    print(file, ret)



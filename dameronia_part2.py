# 「逆転オセロニア」を画像解析して自動ダメージ計算 part2 (文字識別編)
# https://qiita.com/toyotoyo_/items/161496e1bcf685e6ecb3

# ATK部分の画像抽出

from PIL import Image, ImageTk, ImageGrab
url_img = 'othellonia_atk2.png'
ImageGrab.grab(bbox=(881, 978, 950, 999)).save(url_img)



# pytesseractを実行

from PIL import Image, ImageTk, ImageGrab
import pytesseract
url_img = 'othellonia_atk2.png'

img = Image.open(url_img)
number = pytesseract.image_to_string(img, config = "--psm 7 nobatch digits")
print(number)



# おまけ
# 画像変換後にOCR実行

from PIL import Image, ImageTk, ImageGrab
import pytesseract
import cv2
url_img = 'othellonia_atk2.png'
ImageGrab.grab(bbox=(881, 978, 950, 999)).save(url_img)



# 入力画像の読み込み
img = cv2.imread(url_img)

#色の反転
img = cv2.bitwise_not(img)
# 結果をファイルに出力
cv2.imwrite("bitwise_not_" + url_img, img)



# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# 結果をファイルに出力
cv2.imwrite("gray_" + url_img, gray)



#しきいち処理
t = 100  # 閾値
ret, th2 = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
# 結果をファイルに出力
cv2.imwrite("threshold_" + url_img, th2)



# OCR実行
number = pytesseract.image_to_string(th2, config = "--psm 7 nobatch digits")
print(number)
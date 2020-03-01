# 「逆転オセロニア」を画像解析して自動ダメージ計算 part1 (iPhone PC表示編)
# https://qiita.com/toyotoyo_/items/eb1198074eafabcc8a67

from PIL import Image, ImageTk, ImageGrab
url_img = 'othellonia.png'
ImageGrab.grab(bbox=(600, 0, 1920, 1030)).save(url_img)
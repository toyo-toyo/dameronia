# 「逆転オセロニア」を画像解析して自動ダメージ計算 part4 (ダメージ計算編)
# https://qiita.com/toyotoyo_/items/59ad4cc24cfd78ddc700


# オセロニアのダメージ計算用クラス


from decimal import Decimal

# スキル(コンボ)定義用クラス
class Skill:
    def __init__(self, _type, **mapping):
        self.type = _type
        if "one" in mapping: self.one = Decimal(mapping['one'])
        if "max" in mapping: self.max = Decimal(mapping['max'])
        if "premise" in mapping: self.premise = mapping['premise']

BLANK = 0
BLACK = 1
WHITE = -1
BOARD_SIZE = 6
XS = ['A', 'B', 'C', 'D', 'E', 'F']
YS = ['1', '2', '3', '4', '5', '6']
OFFSET = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
DECK = {'0751': {'name': 'デネブ', 'skill': Skill('aura'), 'combo': Skill('whisper', one='1.3', max='2')},
        '1926': {'name': '竜フェリヤ', 'skill': Skill('fixed', max='2'), 'combo': Skill('fixed', max='2.2')},
        '1719': {'name': 'ジェンイー', 'skill': Skill('my_board', premise=12, max='1.9'), 'combo': Skill('whisper', one='1.3', max='2.2')},
        '3414': {'name': 'ルーシュ', 'skill': Skill('whisper', one='1.3', max='2'), 'combo': Skill('whisper', one='1.3', max='1.8')},
        '3133': {'name': 'ランメリー', 'skill': Skill('fixed', max='1.9'), 'combo': Skill('whisper', one='1.3', max='1.8')},
        '3001': {'name': '京極', 'skill':Skill('fixed', max='1.8'), 'combo': Skill('whisper', one='1.3', max='1.6')},
        '2968': {'name': 'イモ', 'skill': Skill('aura'), 'combo': Skill('mai', premise=2, max='1.6')},
        '2250': {'name': '雛クロリス', 'skill': Skill('fixed', max='2.1'), 'combo': Skill('mai', premise=2, max='1.6')},
        '2206': {'name': 'ラウラ', 'skill': Skill('whisper', one='1.3', max='1.9'), 'combo': Skill('whisper', one='1.3', max='1.8')},
        '1933': {'name': '竜守護者', 'skill': Skill('fixed', max='1.7'), 'combo': Skill('whisper', one='1.3', max='2')},
        '1892': {'name': 'エルツドラッヘ', 'skill': Skill('my_board', premise=8, max='1.7'), 'combo': Skill('whisper', one='1.3', max='2')},
        '1646': {'name': '呂蒙', 'skill': Skill('previous', premise=1, max='1.3'), 'combo': Skill('whisper', one='1.3', max='1.8')},
        '1436': {'name': 'グレリオ', 'skill': Skill('fixed', max='1.5'), 'combo': Skill('fixed', max='1.6')},
        '0848': {'name': 'ファイドレ', 'skill': Skill('mai', premise=2, max='1.8'), 'combo': Skill('whisper', one='1.3', max='2')},
        '0847': {'name': 'ランタイ', 'skill': Skill('aura'), 'combo': Skill('fixed', max='1.4')},
        '0755': {'name': 'クロリス', 'skill': Skill('fixed', max='1.8'), 'combo': Skill('fixed', max='1.6')}}

# オセロニア ダメージ計算用クラス
class Damellonia:
    def __init__(self, my_stone=BLACK):
        self.cells = [[0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0,-1, 1, 0, 0],
                     [0, 0, 1,-1, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]] # 現在の盤面の状況
        self.current = BLACK # 現在の順番
        self.player = my_stone # 自分の石の色
        self.boardPiece = [] # 盤面の自分の駒
        self.puts = []   # 現在置ける位置
        self.putInfo = []   # 置いた場合の情報
        self.previousCnt = 0   # 直前に返された枚数
        self.atks = [None,None,None,None] # 画面から識別したATKの値
        self.tegomas = [None,None,None,None] # 画面から識別した手駒番号
        for i in range(BOARD_SIZE):
            self.boardPiece.append([None for i in range(BOARD_SIZE)])
            self.putInfo.append([None for i in range(BOARD_SIZE)])
        self.allCheckStone()
        self.boardPrint()

    # 置ける石をチェック
    def checkStone(self, x, y):
        if self.cells[x][y] != BLANK:
            return
        flippable = []
        cmbs = []
        for dx, dy in OFFSET:
            tmp = []
            depth = 0
            while(True):
                depth += 1
                rx = x + (dx * depth)
                ry = y + (dy * depth)
                if 0 <= rx < BOARD_SIZE and 0 <= ry < BOARD_SIZE:
                    request = self.cells[rx][ry]
                    if request == BLANK:
                        break
                    if request == self.current:
                        if tmp != []:
                            flippable.extend(tmp)
                            if self.boardPiece[rx][ry] != None:
                                cmbs.append(self.boardPiece[rx][ry])
                        break
                    else:
                        tmp.append((rx, ry))
                else:
                    break  
        if flippable != []:
            # 駒の置ける位置や置いた場合の情報を退避
            self.puts.append((x, y))
            self.putInfo[x][y]={'flippable': flippable, 'cnt': len(flippable) , 'combos': cmbs}

    # 盤面全ての置ける石をチェック
    def allCheckStone(self):
        self.puts = []
        self.putInfo = []
        for i in range(BOARD_SIZE):
            self.putInfo.append([None for i in range(BOARD_SIZE)])
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.checkStone(x, y)

    # 石を置く
    def putStone(self, x, y, pieceNo):
        if self.cells[x][y] != BLANK:
            print(XS[x] + YS[y] + 'はすでに置かれています')
            return False
        if self.putInfo[x][y] == None:
            print(XS[x] + YS[y] + 'は置けません')
            return False
        flippable = self.putInfo[x][y]['flippable']
        # 実際に石を置く処理
        self.cells[x][y] = self.current
        self.previousCnt = self.putInfo[x][y]['cnt'] 
        if self.current == self.player:
            self.boardPiece[x][y] = pieceNo # 置いた駒を覚えておく
        for xf, yf in flippable:
            self.cells[xf][yf] = self.current
            self.boardPiece[xf][yf] = None # 返したら駒を消す
        self.current *= -1
        self.allCheckStone()
        return True

    # 盤面確認用（自動計算には必要なし）
    def boardPrint(self):
        if self.current == BLACK:
            print('黒番')
        else:
            print('白番')
        stone = ['〇', '＊', '●']
        bord =['', '', '', '', '', '']
        for cell in self.cells:
            for y, i in enumerate(cell):
                bord[y] += stone[i+1]
        for s in bord:
            print(s)
        for x, y in self.puts:
            info = self.putInfo[x][y]
            comb = ''
            if len(self.putInfo[x][y]['combos']) > 0:
                for no in self.putInfo[x][y]['combos']:
                    comb += DECK[no]['name'] + ' '
                comb += 'とコンボ！！'
            print(XS[x] + YS[y] + 'は' + str(info['cnt']) + '枚返し ' + comb)

    # スキル(コンボ含)の倍率計算
    def getSkillMultiply(self, info, skill):
        type = skill.type
        if type == "aura":
            return 0
        elif type == "fixed":
            return  skill.max
        elif type == "whisper":
            one = Decimal(skill.one) ** (len([i for j in self.boardPiece for i in j if i]) + 1)
            if skill.max <= one:
                return skill.max 
            return one
        elif type == "my_board":
            if len([i for j in self.cells for i in j if i == self.player]) <= skill.premise:
                return skill.max 
        elif type == "mai":
            if info['cnt'] >= skill.premise:
                return skill.max 
        elif type == 'previous':
            if self.previousCnt == skill.premise:
                return skill.max 
        return 0

    # 指定駒での倍率計算
    def getMultiply(self, info, pieceNo):
        multiply = Decimal('1')
        if info['cnt'] != 1:
            multiply = Decimal('1.2') ** (info['cnt'] - 1)
        skillMultiply = self.getSkillMultiply(info, DECK[pieceNo]['skill'])
        if skillMultiply == 0:
            return multiply
        comboMultiply = 1
        for no in info['combos']:
            cm = self.getSkillMultiply(info, DECK[no]['combo'])
            if cm != 0:
                comboMultiply *= cm
        return multiply * skillMultiply * comboMultiply

    # 各駒を置いた時の情報を表示
    def infoDisplay(self):
        for i, no in enumerate(self.tegomas):
            print(DECK[no]['name'] + ' ATK: ' + str(self.atks[i]))
            for x, y in self.puts:
                print(XS[x] + YS[y] + '  ' + str(self.atks[i] * self.getMultiply(self.putInfo[x][y], no)))

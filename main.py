import os, keyboard, random, time, sys

ROWS = 27
COLS = 160
TOWERSIZE = 8

textureArray = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
GAMEOVER = False
SCORE = 0
DIFFICULTY = 1
HIGHSCORE = 0
FPS_CAP = 20
FPS = 0

def gotoxy(x, y):
    print("\033[%d;%dH" % (y, x), end='')


def printGameIntro():
    gotoxy(0, 0)
    print('''
|-----------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                     |
|                                                                                                                                                     |
|                                  FFFFFFFFF  LL                  A            PPPPPPP      PPPPPPP     YY      YY                                    |
|                                  FF         LL                AA AA          PP     P     PP     P     YY    YY                                     |
|                                  FFFFFFFF   LL               AA   AA         PPPPPPP      PPPPPPP       YY  YY                                      |
|                                  FF         LL              AAAAAAAAA        PP           PP              YY                                        |
|                                  FF         LL             AA       AA       PP           PP              YY                                        |
|                                  FF         LLLLLLLLL     AAA       AAA      PP           PP              YY                                        |
|                                                                                                                                                     |
|                                                                                                                                                     |
|                                                     BBBBBB     II   RRRRRR       DDDD                                                               |
|                                                     BB   BB    II   RR    RR     DD   DD                                                            |
|                                                     BBBBBBB    II   RR    RR     DD     D                                                           |
|                                                     BB    BB   II   RR RR        DD     D                                                           |
|                                                     BB     B   II   RR   RR      DD    DD                                                           |
|                                                     BBBBBBB    II   RR     RR    DDDDDD                                                             |
|                                                                                                                                                     |
|                                                              V 2.1 By TheStef                                                                       |
|                                                                                                                                                     |
|                                             COMMANDS:                                                                                               |
|                                                      JUMP: ARROW-UP                                                                                 |
|                                                      EXIT: CTRL+C                                                                                   |
|                                                      START/NEW-GAME (when game is over): ENTER                                                      |
|                                                                                                                                                     |
|                                                                                                                                                     |
|                                                                                                                                                     |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|
                                                                                                                                                       
                                                                                                                                                       
                                                                                                                                                       
''')

def printGameOver():
    gotoxy(0, 8)
    print('''
|                                               GGGG              A         MM          MM   EEEEEEEEEEE
|                                           GGG      GG         AA AA       MMMM      MMMM   EE
|                                           GG                 AA   AA      MM  MM  MM  MM   EEEEEEEEEEE
|                                           GG   GGGGGGG      AAAAAAAAA     MM    MM    MM   EE
|                                            GGG   GG        AA       AA    MM          MM   EE
|                                               GGGGG       AAA       AAA   MM          MM   EEEEEEEEEEE
|
|                                               OOOO       VV           VV   EEEEEEEEEEE     RRRRRR
|                                            OO      OO     VV         VV    EE              RR    RR
|                                           O          O     VV       VV     EEEEEEEEEEE     RR    RR
|                                           O          O      VV     VV      EE              RR RR
|                                            OO      OO         VV VV        EE              RR   RR
|                                               OOOO              V          EEEEEEEEEEE     RR     RR''')

def initArray(a):
    for row in range(ROWS):
        for x in range(COLS):
            if x == COLS - 1:
                a[row][x] = '\n'
            elif x >= COLS - TOWERSIZE - 1:
                a[row][x] = ' '
            elif x == 0 or x == (COLS - TOWERSIZE - 2):
                a[row][x] = '|'
            elif row == 0 or row == (ROWS - 1):
                a[row][x] = '-'
            elif row == ROWS // 3 or row == ROWS // 3 + 1:
                if x == 8 or x == 9 or x == 10:
                    a[row][x] = 'G'
                else:
                    a[row][x] = ' '
            else:
                a[row][x] = ' '

def insertTower(a, height):
    if height == 0:
        return
    if height > 0:
        for row in range(ROWS - height, ROWS - 1):
            for x in range(151, COLS - 1):
                a[row][x] = '0'
    else:
        for row in range(1, -height):
            for x in range(151, COLS - 1):
                a[row][x] = '0'

def shiftArrayTick(a, jump_size):
    global GAMEOVER, SCORE
    for row in range(1, ROWS - 1):
        for x in range(COLS):
            if a[row][x] == '0':
                if a[row][x - jump_size] == 'G':
                    GAMEOVER = True
                if x <= jump_size:
                    a[row][x] = ' '
                    SCORE += 0.1
                else:
                    check = 0
                    for m in range(jump_size):
                        if a[row][x - jump_size + m] == '|':
                            check = 1
                    if check:
                        a[row][x - jump_size - 1] = '0'
                        a[row][x] = ' '
                    else:
                        a[row][x - jump_size] = '0'
                        a[row][x] = ' '

def printMat(a):
    global DIFFICULTY, HIGHSCORE, FPS
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(ROWS):
        for j in range(COLS):
            if j >= COLS - 9:
                if j == COLS - 1:
                    print()
                    continue
                print(' ', end='')
            else:
                print(a[i][j], end='')
    print(f"                  STAGE (1-4): {DIFFICULTY}{' '*20}SCORE: {int(SCORE)}{' '*25}HIGH SCORE: {int(HIGHSCORE)}{' '*23}FPS: {FPS:.2f}\n")

def shiftPlayer(a, y):
    global GAMEOVER
    if y < 0:
        for row in range(1, ROWS):
            for x in range(8, 11):
                if a[row][x] == 'G':
                    if row <= 1:
                        GAMEOVER = True
                        return

                    a[row + y][x] = 'G'
                    a[row][x] = ' '
    else:
        for row in range(ROWS - 1, 0, -1):
            for x in range(8, 11):
                if a[row][x] == 'G':
                    if row + y >= ROWS:
                        GAMEOVER = True
                        return
                    a[row + y][x] = 'G'
                    a[row][x] = ' '

def hideCursor():
    os.system('cls' if os.name == 'nt' else 'clear')

def startGame():
    global GAMEOVER, SCORE, DIFFICULTY, HIGHSCORE, FPS, FPS_CAP
    count = 0
    top = 0
    delim = TOWERSIZE * 2
    time.sleep(0.5)
    printGameIntro()
    while True:
        try:
            if keyboard.is_pressed('enter'):
                hideCursor()
                initArray(textureArray)
                break
        except KeyboardInterrupt:
            sys.exit()

    while True:
        try:
            t1 = time.time()
            for _ in range(DIFFICULTY):
                if GAMEOVER:
                    printGameOver()
                    while True:
                        time.sleep(0.1)
                        if keyboard.is_pressed('enter'):
                            hideCursor()
                            count = 0
                            top = 0
                            GAMEOVER = False
                            HIGHSCORE = SCORE
                            SCORE = 0
                            DIFFICULTY = 1
                            initArray(textureArray)
                            t1 = time.time()
                            break

                shiftArrayTick(textureArray, 2)
                if keyboard.is_pressed('up'):
                    shiftPlayer(textureArray, -1)
                else:
                    shiftPlayer(textureArray, 1)

                if SCORE >= 100:
                    if DIFFICULTY == 1:
                        DIFFICULTY = 2
                    if SCORE >= 300:
                        if DIFFICULTY == 2:
                            DIFFICULTY = 3
                        if SCORE >= 500:
                            if DIFFICULTY == 3:
                                DIFFICULTY = 4

                if count >= delim:
                    r = random.randint(0, 2)
                    if r == 2:
                        height = 10 + random.randint(0, 4)
                        if top:
                            insertTower(textureArray, -height)
                            top = 0
                        else:
                            insertTower(textureArray, height)
                            top = 1
                        count = 0
                count += 1
            time.sleep(1/FPS_CAP - (time.time() - t1))
            t2 = time.time()
            FPS = 1 / (t2 - t1)
            printMat(textureArray)
            
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    hideCursor()
    startGame()

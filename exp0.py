import curses as cs
from wins import *
from obj import *

cs.noecho()
cs.cbreak()
stdscr.keypad(True)
stdscr.clear()
# 色彩参考
# https://www.sojson.com/rgb.html
cs.start_color()
cs.init_pair(1, cs.COLOR_WHITE, cs.COLOR_BLACK)
cs.init_pair(2, cs.COLOR_GREEN, cs.COLOR_BLACK)
cs.init_pair(3, cs.COLOR_YELLOW, cs.COLOR_BLACK)
cs.init_pair(4, cs.COLOR_RED, cs.COLOR_BLACK)
cs.init_pair(5, cs.COLOR_BLUE, cs.COLOR_BLACK)
# 1-8为cs内置颜色
COLOR_LightGray = 9
cs.init_color(COLOR_LightGray, 240, 240, 240)
cs.init_pair(6, COLOR_LightGray, cs.COLOR_BLACK)
# 坐标系
room_cord = [[Floor() for i in range(room_width-2)] for j in range(room_height-2)]
room_cord[2][5] = Board()
room_cord[3][3] = Door()
room_cord[3][4] = Password_Door('123')
room_cord[5][5] = Box()
room_cord[5][5].cont = [OBJ(), OBJ()]

# 界面初始化
win_init(room_win, room_cord)
lalala = Warning_Win(3, 50)
lalala.show(2, 'Welcome to the world of Arda!')
def Global_Win_Update():
    main_win.box()
    status_win.box()
    main_win.refresh()
    status_win.refresh()
    stdscr.refresh()
ch = main_win.getch()
Global_Win_Update()

# 玩家初始化
my_x = 0
my_y = main_begin_y // 2

while ch != ord('q') and ch != ord("Q"):
    ch = room_win.getch()
    # 物品交互
    if ch == ord('c') or ch == ord('C'):
        # 方向向量
        d_y = 0
        d_x = 0
        d = lalala.show(1, 'Where to operate?')
        if (d == ord('w') or d == ord("W")) and my_y > 0:
            d_y = -1
        elif (d == ord('s') or d ==ord("S")) and my_y < room_height - 3:
            d_y = 1
        elif (d == ord('a') or d==ord("A")) and my_x > 0:
            d_x = -1
        elif (d == ord('d') or d==ord("D")) and my_x < room_width - 3:
            d_x = 1
        room_cord[my_y+d_y][my_x+d_x].interact()
        win_init(room_win, room_cord)
        Global_Win_Update()
    else:
        d_y = 0
        d_x = 0
        # 简单移动
        if (ch == ord('w') or ch==ord("W")) and my_y > 0:
            d_y = -1
        elif (ch == ord('s') or ch==ord("S")) and my_y < room_height - 3:
            d_y = 1
        elif (ch == ord('a') or ch==ord("A")) and my_x > 0:
            d_x = -1
        elif (ch == ord('d') or ch==ord("D")) and my_x < room_width - 3:
            d_x = 1
        if room_cord[my_y+d_y][my_x+d_x].passable:
            room_win.addch(my_y+1, my_x+1, room_cord[my_y][my_x].sym, cs.color_pair(room_cord[my_y][my_x].n_color))
            my_y += d_y
            my_x += d_x
            
    room_win.addch(my_y+1, my_x+1, '@')
    room_win.refresh()
    

# end
cs.nocbreak()
stdscr.keypad(False)
cs.echo()
cs.endwin()
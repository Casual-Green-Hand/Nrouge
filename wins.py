import curses as cs
from obj import *

stdscr = cs.initscr()

def win_init(win: cs.window, cord):
    h = win.getmaxyx()[0]
    w = win.getmaxyx()[1]
    for y in range(1, h-1):
        for x in range(1, w-1):
            # print(cord[y-1][x-1])
            win.addch(y, x, cord[y-1][x-1].sym, cs.color_pair(cord[y-1][x-1].n_color))
    win.refresh()

main_begin_x = 0
main_begin_y = 0
main_height = cs.LINES
main_width = cs.COLS // 2
main_win = cs.newwin(main_height, main_width, main_begin_y, main_begin_x)
main_win.box()
stdscr.refresh()

# 子窗口试验
room_height = 10
room_width = 20
room_win = main_win.subwin(room_height, room_width, main_height//2-room_height//2, main_width//2-room_width//2)
room_win.box()
main_win.refresh()

# status_win
status_begin_x = main_width
status_begin_y = 0
status_height = cs.LINES // 2
status_width = cs.COLS - main_width
status_win = cs.newwin(status_height, status_width, status_begin_y, status_begin_x)
status_win.box()
stdscr.refresh()

# 弹窗
class Warning_Win:
    def __init__(self, height, width) -> None:
        self.h = height
        self.w = width
        self.win = cs.newwin(self.h, self.w, cs.LINES // 2 - self.h // 2, cs.COLS // 2 - self.w // 2)
    def show(self, n_color, meg):
        self.win.box()
        self.win.overwrite(stdscr)
        stdscr.refresh()
        self.win.addstr(1, self.w // 2 - len(meg) // 2, meg, cs.color_pair(n_color))
        self.win.refresh()
        ch = self.win.getch()
        self.win.erase()
        self.win.refresh()
        stdscr.refresh()
        return ch

# 确认框
class Check_Win(Warning_Win):
    def show(self, n_color, meg):
        self.win.box()
        self.win.overwrite(stdscr)
        stdscr.refresh()
        self.win.addstr(1, 1, meg, cs.color_pair(n_color))
        self.win.addstr(self.h - 1, 1, 'Yes[Y]', cs.color_pair(2))
        self.win.refresh()
        key = self.win.getch()
        self.win.erase()
        self.win.refresh()
        stdscr.refresh()
        if key == ord('y') or key==ord("Y"):
            return 1
        else:
            return 0
        
# 文本输入框
class Text_Win(Warning_Win):
    meg = 'Type the text:'
    text = 'Submmit[Y]'
    def show(self):
        self.win.box()
        self.win.overwrite(stdscr)
        stdscr.refresh()
        self.win.addstr(1, 1, self.meg, cs.color_pair(1))
        self.win.addstr(self.h - 1, 1, self.text, cs.color_pair(2))
        self.win.refresh()
        # 密码输入及检测
        self.win.move(2,1)
        a = self.win.getch()
        s = ''
        while a != ord('y') and a!=ord("Y"):
            s += chr(a)
            self.win.addch(a)
            self.win.refresh()
            a = self.win.getch()
        self.win.erase()
        self.win.refresh()
        stdscr.refresh()
        return s
# 密码输入框
class Password_Win(Warning_Win):
    meg = 'Type the password:'
    text = 'Submmit[Y]'
    def show(self):
        self.win.box()
        self.win.overwrite(stdscr)
        stdscr.refresh()
        self.win.addstr(1, 1, self.meg, cs.color_pair(1))
        self.win.addstr(self.h - 1, 1, self.text, cs.color_pair(2))
        self.win.refresh()
        # 密码输入及检测
        self.win.move(2,1)
        a = self.win.getch()
        s = ''
        while a != ord('y') and a!=ord("Y"):
            s += chr(a)
            self.win.addch('*')
            self.win.refresh()
            a = self.win.getch()
        self.win.erase()
        self.win.refresh()
        stdscr.refresh()
        return s
    
# 单选框
class Single_Choose_Box(Warning_Win):
    title = 'Choose:'
    def show(self, options: list):
        self.win.erase()
        self.win.box()
        self.win.overwrite(stdscr)
        stdscr.refresh()
        # 对options分组，每页9项
        opt = []
        # 无需翻页的情况
        if len(options) < 10:
            opt = options
            self.win.addstr(1,1, self.title)
            for i in range(len(opt)):
                self.win.addstr(i+2, 1, '[%d]:' % (i+1), cs.color_pair(2))
                self.win.addstr(opt[i], cs.color_pair(1))
            self.win.refresh()    
            key = self.win.getch()
            while key > ord('9') or key < ord('1'):
                key = self.win.getch()
            return key - ord('0')
        # 需要翻页的情况
        else:
            for i in range(len(options) // 9):
                opt.append(options[i*9:(i+1)*9])
            opt.append(options[(i+1)*9:])
            key = self.win.getch()
            sum_page = len(options) // 9 + 1
            page = 0
            while key != ord('Y'):
                if key == cs.KEY_RIGHT and page < sum_page:
                    page += 1
                if key == cs.KEY_LEFT and page > 0:
                    page -= 1
                if key <= ord('9') and key >= ord('1'):
                    break
                self.win.addstr(1,1, self.title)
                for i in range(9):
                    self.win.addstr(i+2, 1, '[%d]:' % (i+1), cs.color_pair(2))
                    self.win.addstr(opt[page][i], cs.color_pair(1))
                self.win.refresh()
            return page * 9 + ord(key) - ord('0')
    
# 多选框
# class Multiple_Choose_Box(Warning_Win):
#     meg = 'Choose:'
#     def show(self, options: list):
#         self.win.box()
#         self.win.overwrite(stdscr)
#         stdscr.refresh()

#         page = len(options) // 9
#         c_page = 0
#         ch_list = [False for i in range(len(options))]
#         while True:
#             self.win.erase()
#             for i in range(9):
#                 self.win.addstr(1,1, self.meg)
#                 self.win.addstr(i+1, 1, '[%d]:-' % (i+1), cs.color_pair(2))
#                 self.win.addstr(options[c_page * 9 + i])
#                 self.win.refresh()
#             key = self.win.getch()
#             if key == cs.KEY_RIGHT and c_page < page:
#                 c_page += 1
#                 continue
#             if key == cs.KEY_LEFT and c_page > 0:
#                 c_page -= 1
#                 continue
#             if ord('1') <= key <= ord('9'):
#                 choice = c_page * 9 + key - 1
#                 if ch_list[choice]:
#                     self.win.addch(choice+2, 5, '-', cs.color_pair(2))
#                     ch_list[choice] = 1-ch_list[choice]
#                 else:
#                     self.win.addch(choice+2, 5, '+', cs.color_pair(2))
#                     ch_list[choice] = 1-ch_list[choice]
#                 self.win.refresh()
#             if key == ord('y'):
#                 return ch_list
        
# 物品管理框
class Obj_Manage_Box(Warning_Win):
    def show(self, my_pack: Container, other_pack: Container):
        pass
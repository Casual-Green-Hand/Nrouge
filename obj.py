import curses as cs
import wins

# 所有物体的父类（空物体）
class OBJ:
    sym = ''            #
    n_color = 1         #
    passable = True     # 是否允许被穿过
    endur = 0           # 耐久度
    cur_st = 'ABLE'     #
    def __init__(self):
        pass
    def interact(self):
        return 0

class Floor(OBJ):
    sym = '.'
    passable = True
    endur = 20

class Board(OBJ):
    sym = '#'
    passable = False
    endur = 10

'''
==========
Containers
==========
'''
# 容器父类
class Container(OBJ):
    capacity = 0
    cont = []
    cur_st = 'NOT_FULL'
    def interact(self):
        h = len(self.cont)
        t_win = wins.Multiple_Choose_Box(cs.LINES // 2, cs.COLS // 2)
        op = []
        for i in range(len(self.cont)):
            op.append(str(type(self.cont[i])))
        opt = t_win.show(op)
        return opt
    def in_out(self):
        pass

# 可开关容器（单选框测试）  
class Box(Container):
    sym = 'u'
    n_color = 3
    endur = 2
    #
    capacity = 5 # 容量
    cont = []
    cur_st = ['CLOSE', 'NOT_FULL']
    def interact(self):
        if self.cur_st[0] == 'CLOSE':
            options = ['Open the box']
        else:
            options = ['Close the box', 'Manage Objects']
        c_win = wins.Single_Choose_Box(len(options) + 3, 30)    
        ch = c_win.show(options)
        print(ch)
        # 开关盒子
        if ch == 1:
            if self.cur_st[0] == 'CLOSE':
                self.cur_st[0] = 'OPEN'
                self.n_color = 1
            else:
                self.cur_st[0] = "CLOSE"
                self.n_color = 3
        # 物品管理
        if ch == 2:
            self.in_out()
'''
=====
Doors
=====
'''
# 无需密码即可开启的门
class Door(OBJ):
    sym = '+'
    placable = False
    passable = False
    endur = 0
    cur_st = 'CLOSE'
    def interact(self):
        if self.cur_st == 'CLOSE':
            self.cur_st = 'OPEN'
            self.sym = '-'
            self.passable = True
        else:
            self.cur_st = "CLOSE"
            self.sym = '+'
            self.passable = False
        return 1

# 密码门
class Password_Door(Door):
    def __init__(self, password: str):
        self.pw = password
    def interact(self):
        if self.cur_st == 'CLOSE':
            pw_win = wins.Password_Win(5, 30)
            w_win = wins.Warning_Win(3, 30)
            inp = pw_win.show()
            if inp == self.pw:
                self.cur_st = 'OPEN'
                self.sym = '-'
                self.passable = not self.passable
                w_win.show(2, 'Correct')
            else:
                w_win.show(4, 'Error')
            del pw_win
            del w_win
        else:
            self.cur_st = 'CLOSE'
            self.sym = '+'
            self.passable = False
        return 1

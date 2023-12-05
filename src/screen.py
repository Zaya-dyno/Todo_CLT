import os,logging,curses
from enum import Enum
from helper import printf

class Mode(Enum):
    Scr = 1
    Cmd = 2

class Screen:
    COL = None
    ROW = None
    list_scr = None
    cmd_scr = None
    Data = None
    config = None
    mode = Mode.Cmd
    Functions = {}
    F_macro = {"a":"add",
               "d":"done",
               "s":"start",
               "ar":"addr",
               "e":"end",
               "r":"remove"}

    def __init__(self, data, scr):
        self.scr = scr
        self.Data = data
        (self.COL,self.ROW) = os.get_terminal_size() 
        self.config = self.Data.get_config()["Screen"]
        Scr_h = int(self.config["ratio_scr_cmd"] *
                    self.ROW)
        Cmd_h = self.ROW - Scr_h
        self.list_scr = List_scr(Scr_h,self.COL,
                                 self.Data)
        self.cmd_scr = Cmd_scr(Cmd_h,self.COL,
                               (Scr_h,0))
        self.set_functions()

    def clean_screen(self):
        self.scr.clear()

    def render(self):
        self.clean_screen()
        self.list_scr.render()
        self.cmd_scr.render()

    def set_functions(self):
        self.Functions["add"] = self.add_task
        self.Functions["done"] = self.done_task
        self.Functions["start"] = self.start_task
        self.Functions["addr"] = self.add_repeated_task
        self.Functions["end"] = self.end_task
        self.Functions["remove"] = self.remove_task
        self.Functions["save"] = self.save_data

    def save_data(self):
        self.Data.save()

    def done_task(self,args):
        try:
            ID = int(args[0])
        except:
            return -1
        done = True
        if len(args) > 1:
            done = not (args[1] == "r")
        return self.Data.done_task(ID,done)

    def start_task(self,args):
        pass

    def add_repeated_task(self,args):
        pass

    def end_task(self,args):
        pass

    def add_task(self,args):
        try:
            title = args[0]
        except:
            return -1

        try:
            tags = args[1:]
        except:
            tags = []
        self.Data.add_task(args[0],[])
        pass
    
    def remove_task(self,args):
        pass

    def done_task(self,args):
        pass

    def edit_task(self,args):
        pass

    def execute_line(self,cmd):
        if cmd.isspace() or cmd == "":
            return -1
        tokens = cmd.split()
        if not tokens:
            return -1

        cmd = tokens[0]
        if cmd in self.F_macro.keys():
            cmd = self.F_macro[cmd]

        logging.debug(cmd)

        if cmd not in self.Functions.keys():
            return -1

        logging.debug("execute")
        func = self.Functions[cmd]
        if len(tokens) == 1:
            return func()
        else:
            return func(tokens[1:])


    def execute_cmd(self,cmd):
        if (type(cmd) == int):
            if (cmd == 6):
                self.mode = Mode.Scr
            return 1
        else:
            self.execute_line(cmd)
            return 0
    
    def get_input(self):
        command = ""
        if self.mode == Mode.Scr:
            command = self.list_scr.get_input()
        else:
            command = self.cmd_scr.get_input()
        ret = self.execute_cmd(command)
        return ret

class Frame:
    R_D = "\u250F"
    U_R = "\u2517"
    D_L = "\u2513"
    U_L = "\u251B"
    R_L = "\u2501"
    U_D = "\u2503"
    U_R_D = "\u2523"
    U_D_L = "\u252B"
    HEAD_SEP = " \u25C6 "


class CMDS:
    NEW_LINE = 10
    SCR_MODE = 6

class List_scr:
    ROW = None
    COL = None
    Data = None
    Start = None
    Chosen_tag = 0
    Start_head = (1,1)
    Start_list = (2,1)

    def __init__(self,row,col,data,start=(0,0)):
        self.ROW = row
        self.COL = col
        self.Data = data
        self.Start = start
        self.scr = curses.newwin(row,col,start[0],start[1])
        self.render_frame()

    def render_frame(self):
        frame = Frame.R_D
        frame += Frame.R_L * (self.COL - 2)
        frame += Frame.D_L
        self.scr.insstr(0,0,frame)
        for i in range(1,self.ROW-1):
            self.scr.insstr(i,0,Frame.U_D)
            self.scr.insstr(i,self.COL-1,Frame.U_D)
        frame = Frame.U_R
        frame += Frame.R_L * (self.COL - 2)
        frame += Frame.U_L
        self.scr.insstr(self.ROW-1,0,frame)

    def get_input(self):
        self.scr.getch()

    def render_header(self):
        headers = self.Data.get_tags_header()
        self.scr.move(self.Start_head[0],
                      self.Start_head[1])
        for i in range(len(headers)):
            flag = 0
            if i != 0:
                self.scr.addstr(Frame.HEAD_SEP)
            if i == self.Chosen_tag:
                flag = curses.A_UNDERLINE
            self.scr.addstr(headers[i],flag)
        y,x = self.scr.getyx()
        self.scr.move(y+1,
                      0)

    def render_list(self):
        self.scr.move(self.Start_list[0],
                      self.Start_list[1])
        for task in self.Data.tasks:
            self.scr.addstr(str(task))
            y,x = self.scr.getyx()
            self.scr.move(y+1,1)

    def render(self):
        self.render_header()
        self.render_list()
        self.scr.refresh()


class Cmd_scr:
    ROW = None
    COL = None
    Start = None

    def __init__(self,row,col,start):
        self.ROW = row
        self.COL = col
        self.Start = start
        self.scr = curses.newwin(row,col,start[0],start[1])
        self.screen_set()
        self.y_m, self.x_m = self.scr.getmaxyx()

    def screen_set(self):
        self.scr.keypad(True)
    
    def set_buf(self):
        (y,x) = self.scr.getyx()
        self.cur_loc = y*self.x_m+x 
        self.cur_buf_sta = y*self.x_m+x
        self.cur_buf_end = self.cur_buf_sta + 1
        self.cur_buf_max = self.y_m*self.x_m 
        self.cur_cmd_buf = ""

    def move(self,am):
        loc = self.cur_loc
        dest = loc + am
        if (dest < self.cur_buf_sta or dest >= self.cur_buf_end):
            return
        self.cur_loc = dest
        self.scr.move(dest//self.x_m,dest%self.x_m)

    def cur_loc_buf(self):
        return self.cur_loc - self.cur_buf_sta

    def move_cursor(self):
        self.scr.move(self.cur_loc//self.x_m,self.cur_loc%self.x_m)
    
    def addch(self,char):
        cur = self.cur_loc_buf()
        self.cur_buf_end += 1
        self.cur_cmd_buf = self.cur_cmd_buf[:cur] + \
                       char + self.cur_cmd_buf[cur:]
        self.move(+1)

    def remch(self):
        cur = self.cur_loc_buf()
        self.cur_buf_end -= 1
        self.cur_cmd_buf = self.cur_cmd_buf[:cur-1] + \
                           self.cur_cmd_buf[cur:]
        self.move(-1)


    def loc_to_yx(self,loc):
        return (loc//self.x_m,loc%self.x_m)

    def write_buf(self):
        self.render()
        y,x = self.loc_to_yx(self.cur_buf_sta)
        length = len(self.cur_cmd_buf)
        i = 0
        while i < length:
            cur_len = min(length-i,self.x_m-x)
            self.scr.addstr(y,x,self.cur_cmd_buf[i:i+cur_len])
            i += cur_len
            y += 1
            x = 0


    def get_input(self):
        command = None
        self.set_buf()
        while True:
            ch = self.scr.getch()
            key = chr(ch)
            if (ch == CMDS.SCR_MODE): # go screen mode
                command = ch
                break
            elif (ch == CMDS.NEW_LINE):
                break 
            elif (ch == curses.KEY_LEFT):
                self.move(-1)
            elif (ch == curses.KEY_RIGHT):
                self.move(+1)
            elif (ch == curses.KEY_BACKSPACE):
                self.remch()
                self.write_buf()
            else:
                self.addch(key)
                self.write_buf()
            self.move_cursor()
            self.scr.refresh()
        if command == None:
            command =  self.cur_cmd_buf
        return command

    def render(self):
        self.scr.clear()
        self.scr.addstr(0,0,"Enter cmd:")
        self.scr.refresh()

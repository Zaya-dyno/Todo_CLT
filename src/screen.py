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

    def clean_screen(self):
        self.scr.clear()

    def render(self):
        self.clean_screen()
        self.list_scr.render()
        self.cmd_scr.render()

    def add_task(self,args):
        self.Data.add_task(args[0],[])
        pass

    def execute_line(self,cmd):
        tokens = cmd.split()
        if tokens[0] == 'a' or tokens[0] == 'add':
            self.add_task(tokens[1:])
        else:
            logging.debug('invalid cmd')

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

    def set_catch_signal(self):
        pass

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

    def get_input(self):
        curses.echo()
        command = ""
        while True:
            key = self.scr.getch()
            if (key == CMDS.SCR_MODE): # go screen mode
                command = key
                break
            if (key == CMDS.NEW_LINE):
                break 
            command += chr(key)
        curses.noecho()
        return command

    def render(self):
        self.scr.clear()
        self.scr.addstr(0,0,"Enter cmd:")
        self.scr.refresh()

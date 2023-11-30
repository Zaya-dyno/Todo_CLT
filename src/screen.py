import os,logging
from helper import printf
import curses
import time

class Screen:
    COL = None
    ROW = None
    list_scr = None
    cmd_scr = None
    Data = None
    config = None

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
        time.sleep(1)
    
    def get_input(self):
        pass

    def set_catch_signal(self):
        pass

class Frame:
    LEFT_UP = "\u250F"
    LEFT_DOWN = "\u2517"
    RIGHT_UP = "\u2513"
    RIGHT_DOWN = "\u251B"
    HOR = "\u2501"
    VER = "\u2503"

class List_scr:
    ROW = None
    COL = None
    Data = None
    Start = None
    Chosen_tag = 0
    Color = {"high":"39;46"}

    def __init__(self,row,col,data,start=(0,0)):
        self.ROW = row
        self.COL = col
        self.Data = data
        self.Start = start
        self.scr = curses.newwin(row,col,start[0],start[1])

    def render_frame(self):
        frame = Frame.LEFT_UP
        frame += Frame.HOR * (self.COL - 2)
        frame += Frame.RIGHT_UP
        self.scr.insstr(0,0,frame)
        logging.debug(self.COL)
        logging.debug(self.scr.getmaxyx())
        for i in range(1,self.ROW-1):
            logging.debug(i)
            self.scr.insstr(i,0,Frame.VER)
            self.scr.insstr(i,self.COL-1,Frame.VER)
        frame = Frame.LEFT_DOWN
        frame += Frame.HOR * (self.COL - 2)
        frame += Frame.RIGHT_DOWN
        self.scr.insstr(self.ROW-1,0,frame)

    def add_color(self, text, key):
        return text 

    def render_header(self):
        headers = self.Data.get_tags_header()
        headers[self.Chosen_tag] = self.add_color(headers[self.Chosen_tag], "high")
        top = " \u25C6 ".join(headers)
        self.scr.addstr(1,1,top)

    def render(self):
        self.render_frame()
        self.render_header()
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

    def render(self):
        self.scr.addstr(0,0,"Enter cmd:")
        self.scr.refresh()

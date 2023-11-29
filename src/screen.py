import os
from helper import printf
import logging

class Screen:
    COL = None
    ROW = None
    list_scr = None
    cmd_scr = None
    Data = None
    config = None

    def __init__(self, data):
        self.Data = data
        (self.COL,self.ROW) = os.get_terminal_size() 
        self.config = self.Data.get_config()["Screen"]
        Scr_h = int(self.config["ratio_scr_cmd"] *
                    self.ROW)
        Cmd_h = self.ROW - Scr_h
        self.list_scr = List_scr(Scr_h,self.COL,
                                 self.Data)
        self.cmd_scr = Cmd_scr(Cmd_h,self.COL,
                               (Scr_h + 1,1))

    def clean_screen(self):
        printf("\033[2J")

    def render(self):
        self.clean_screen()
        self.list_scr.render()
        self.cmd_scr.render()

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

    def __init__(self,row,col,data,start=(1,1)):
        self.ROW = row
        self.COL = col
        self.Data = data
        self.Start = start

    def ml_cur(self,row=0,col=0): # move locally cursor
        row += self.Start[0]
        col += self.Start[1]
        printf("\033[{};{}H".format(row,col))

    def render_frame(self):
        self.ml_cur()
        frame = Frame.LEFT_UP
        frame += Frame.HOR * (self.COL - 2) + Frame.RIGHT_UP
        frame += "\n"
        temp = Frame.VER + " " * (self.COL - 2) + Frame.VER
        temp += "\n"
        temp = temp * (self.ROW - 2)
        frame += temp
        frame += Frame.LEFT_DOWN
        frame += Frame.HOR * (self.COL - 2) + Frame.RIGHT_DOWN
        frame += "\n"
        printf(frame)

    def render_header(self):
        self.ml_cur(1,1)
        headers = self.Data.get_tags_header()
        top = " \u25C6 ".join(headers)
        printf(top)

    def render(self):
        self.render_frame()
        self.render_header()

class Cmd_scr:
    ROW = None
    COL = None
    Start = None

    def __init__(self,row,col,start):
        self.ROW = row
        self.COL = col
        self.Start = start

    def ml_cur(self,row=0,col=0): # move locally cursor
        row += self.Start[0]
        col += self.Start[1]
        printf("\033[{};{}H".format(row,col))

    def render(self):
        self.ml_cur()
        printf("Enter_cmd:")

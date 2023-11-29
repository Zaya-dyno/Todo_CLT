import os
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
        Scr_h = int(self.config["ratio_scr_cmd"] * self.ROW)
        Cmd_h = self.ROW - Scr_h
        self.list_scr = List_scr(Scr_h,self.COL,self.Data)
        self.cmd_scr = Cmd_scr(Cmd_h,self.COL)


    def render(self):
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

    def __init__(self,row,col,data):
        self.ROW = row
        self.COL = col
        self.Data = data

    def render_frame(self):
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
        print(frame, end="")
        print("\033[{}A".format(self.ROW), end="")

    def to_new_section(self):
        print("\033[{}B".format(self.ROW), end="")

    def render_header(self):
        headers = self.Data.get_tags_header()
        top = " \u25C6 ".join(headers)
        print("\033[B\033[C",end="")
        print(top,end="")
        print("\033[{}B".format(self.ROW-1), end="")

    def render(self):
        self.render_frame()
        self.render_header()
        self.to_new_section()

class Cmd_scr:
    ROW = None
    COL = None

    def __init__(self,row,col):
        self.ROW = row
        self.COL = col
    def render(self):
        print("\n"*(self.ROW - 1),end="")
        print("\033[%dA"%(self.ROW - 1), end="")
        print("Enter_cmd:",end="")

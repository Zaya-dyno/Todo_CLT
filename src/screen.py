import os
class Screen:
    COL = None
    ROW = None
    Scr_h = None
    Cmd_h = None

    def __init__(self, config):
        (self.COL,self.ROW) = os.get_terminal_size() 
        self.Scr_h = int(config["ratio_scr_cmd"] * self.ROW)
        self.Cmd_h = self.ROW - self.Scr_h

    def render_scr(self):
        print("-\n"*self.Scr_h,end="")

    def render_cmd(self):
        print("\n"*(self.Cmd_h - 1),end="")
        print("\033[%dA"%(self.Cmd_h - 1), end="")
        print("Enter_cmd:",end="")

    def render(self):
        self.render_scr()
        self.render_cmd()

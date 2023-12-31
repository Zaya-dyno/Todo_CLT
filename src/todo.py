import data, screen

class Todo:
    Data = None   # Instance of Data class
    Screen = None # Instance of Screen class
    Config = None # Dict that contains configurations
    def __init__(self,scr):
        self.Data = data.Data()
        self.Config = self.Data.get_config()
        self.Screen = screen.Screen(self.Data, scr)

    def run(self):
        ret = 0
        while ret == 0:
            self.Screen.render()
            ret = self.Screen.get_input()
            self.Screen.save()


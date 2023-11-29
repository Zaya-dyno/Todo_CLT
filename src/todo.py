import data, screen

class Todo:
    Data = None   # Instance of Data class
    Screen = None # Instance of Screen class
    Config = None # Dict that contains configurations
    def __init__(self):
        self.Data = data.Data()
        self.Config = self.Data.get_config()
        self.Screen = screen.Screen(self.Data)

    def run(self):
        self.Screen.render()
        #self.Screen.get_command()
        input("")


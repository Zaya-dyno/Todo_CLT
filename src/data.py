import os,json
class Data:
    config = None
    data_dir = None 

    def __init__(self):
        self.find_data_dir()
        self.config = self.load_json("config.json")
        raw_data = self.load_json("data.json")

    def get_config(self):
        return self.config

    def find_data_dir(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.abspath(os.path.join(script_dir,"../data"))

    def load_json(self,file):
        if (self.data_dir == None):
            self.find_data_dir()

        config_file = os.path.join(self.data_dir,file)
        with open(config_file,"r") as file:
            return json.load(file)

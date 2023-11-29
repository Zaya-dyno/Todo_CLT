import os,json
from task import Task

class Data:
    config = None
    data_dir = None 
    tasks = []
    repTasks = []
    i = 0 # temp solution for id

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
        raw = None
        with open(config_file,"r") as file:
            raw = json.load(file)
        return raw

    def get_new_id(self):
        self.i += 1
        return self.i

    def add_task(self,title,tags,done=False,iden=None):
        if (iden == None):
            iden = self.get_new_id()
        self.tasks.append(Task(iden,title,done,tags))

    def get_tags_header(self):
        return ["today","urgent"]
    def print_tasks_naive(self):
        for task in self.tasks:
            print(task)

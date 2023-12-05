import os,json,logging
from task import Task, Tags
class Data:
    config = None
    data_dir = None 
    tasks = []
    repTasks = []
    reuseID = set()
    max_ID = -1 
    tags = []
    tagsH = []
    tag_today = Tags("today",header=True,importance=10)

    def __init__(self):
        self.find_data_dir()
        self.config = self.load_json("config.json")
        self.load_data()

    def load_data(self):
        self.load_tasks()
        self.load_reTasks()
        self.load_tags()

    def load_tasks(self):
        raw = self.load_json("tasks.json")
        for task in raw:
            self.tasks.append(Task.init__dic(task))
        
        ids = [task.ID for task in self.tasks]
        if len(ids) != 0:
            high = max(ids)
            self.max_ID = high
            self.reuseID = set([i for i in range(ids[-1] + 1)]) - set(ids)


    def load_reTasks(self):
        pass

    def load_tags(self):
        raw = self.load_json("tags.json")
        for tag in raw:
            self.tags.append(Tags.init__dict(tag))
        for tag in self.tags:
            if tag.Header:
                self.tagsH.append(tag)

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

    def write_json(self,file,data):
        if (self.data_dir == None):
            self.find_data_dir()

        config_file = os.path.join(self.data_dir,file)
        with open(config_file,"w") as file:
            json.dump(data,file,
                      default=lambda o:o.__dict__,
                      indent=4)

    def get_new_id(self):
        if len(self.reuseID) == 0:
            self.max_ID += 1
            return self.max_ID
        return self.reuseID.pop()

    def add_tagH(self,tag):
        self.tagsH.append(tag)
        self.tagsH.sort(key=lambda x: x.Im,
                        reverse=True)

    def add_tag(self,tag,sort=True):
        if not isinstance(tag,Tags):
            tag = Tags(tag)
        if tag not in self.tags:
            self.tags.append(tag)
            if tag.header:
                self.add_tagH(tag)
            if sort:
                self.tags.sort(key=lambda x: x.Im,
                               reverse=True)

    def add_task(self,title,tags,done=False,iden=None,sort=True):
        if (iden == None):
            iden = self.get_new_id()
        for tag in tags:
            self.add_tag(tag)
        if not tags:
            tags = [self.tag_today]
        self.tasks.append(Task(iden,title,done,tags))
        if sort:
            self.tasks.sort(key=lambda x:x.ID)

    def find_task(self,ID):
        low = 0
        high = 0
        while low<=high:
            mid = (low + high)//2
            if (self.tags[mid].iden == ID):
                return self.tags[mid]
            elif (self.tags[mid].iden < ID):
                high = mid - 1
            else:
                low = mid + 1
        return None
    
    def done_task(self,ID,done=True):
        task = self.find_task(ID)
        if not task:
            return -1
        task.Done = done 
        return 0


    def start_task(self,ID):
        pass

    def add_repeated_task(self):
        pass
    
    def end_task(self,ID):
        pass

    def remove_task(self,ID):
        task = self.find_task(ID)
        if task != None:
            self.tasks.remove(task)
        return 0

    def get_tags_header(self):
        return [t.Title for t in self.tagsH] 

    def print_tasks_naive(self):
        for task in self.tasks:
            print(task)

    def write_tasks(self):
        self.write_json("tasks.json",self.tasks)

    def save(self):
        self.write_tasks()

class RepTask:
    Title:str
    Repeated:str
    Tags:[str]

    def __init__(title,repeated,tags):
        self.Title = title
        self.Repeated = repeated
        self.Tags = tags

class Task:
    ID:int
    Title:str
    Done:bool
    Tags:[str]

    def __init__(self,iden,title,done,tags):
        self.ID = iden 
        self.Title = title
        self.Done = done
        self.Tags = tags
    
    def __str__(self):
        ret = "{"
        ret += "ID:{},Title:\"{}\",done:{},tags:".format(self.ID,self.Title,self.Done)
        ret += self.Tags.__str__()
        ret += "}"
        return ret

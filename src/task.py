class RepTask:
    def __init__(self,title,repeated,tags):
        self.Title = title
        self.Repeated = repeated
        self.Tags = tags

class Tags:
    def __init__(self,title,header=False,importance=0):
        self.Title = title.lower()
        self.Header = header
        self.Im = importance

    def __eq__(self,other):
        if isinstance(other,Tags):
            return self.Title == other.Title
        return other == self.Title

    def __str__(self):
        return self.Title

    def __repr__(self):
        return self.Title

class Task:
    def __init__(self,iden,title,done,tags):
        self.ID = iden 
        self.Title = title
        self.Done = done
        self.Tags = tags
    
    def __str__(self):
        ret = "{"
        ret += "ID:{},Title:\"{}\",done:{},tags:".format(self.ID,self.Title,self.Done)
        ret += str(self.Tags)
        ret += "}"
        return ret

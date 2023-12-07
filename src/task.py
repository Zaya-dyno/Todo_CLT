import logging
class RepTask:
    def __init__(self,title,repeated,tags):
        self.Title = title
        self.Repeated = repeated
        self.Tags = tags

class Tags:
    @staticmethod
    def init__dict(dic):
        Title = dic["Title"]
        Header = dic["Header"]
        Im = dic["Im"]
        return Tags(Title,Header,Im)

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

    @staticmethod
    def from_list(lis):
        ret = []
        for tag in lis:
            ret.append(Tags(tag["Title"],
                            tag["Header"],
                            tag["Im"]))
        return ret

class Task:
    
    @staticmethod
    def init__dic(dic):
        ID = dic["ID"]
        title = dic["Title"]
        done = dic["Done"]
        tags = Tags.from_list(dic["Tags"])
        return Task(ID,title,done,tags)

    def toJson(self):
        pass

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

    def nice_str(self):
        ret = ""
        if self.Done:
            ret += "\u2611"
        else:
            ret += "\u2610"

        ret += " "
        ret += str(self.ID)
        ret += " "
        ret += self.Title
        ret += " --"
        ret += ",".join([str(t) for t in self.Tags])
        return ret

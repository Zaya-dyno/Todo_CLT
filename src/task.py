class RepTask:
    Title:str
    Repeated
    Tags:[str]

    def __init__(title,repeated,tags):
        self.Title = title
        self.Repeated = repeated
        self.Tags = tags

class Task:
    Title:str
    Done:bool
    Tags:[str]

    def __init__(title,done,tags):
        self.Title = title
        self.Done = done
        self.Tags = tags

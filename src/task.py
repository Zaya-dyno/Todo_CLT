class Task:
    Title:str
    Done:bool
    Tags:[str]

    def __init__(title,done,tags):
        self.Title = title
        self.Done = done
        self.Tags = tags

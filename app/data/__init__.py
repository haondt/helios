import uuid
import json

class Mark:
    def __init__(self):
        self.id  = ""
        self.group_id  = ""
        self.url  = ""
        self.name  = ""
        self.highlight  = ""
        self.icon = ""
class Group:
    def __init__(self):
        self.mark_ids = []
        self.id = ""
        self.name = ""
class Colors:
    def __init__(self):
        self.background  = ""
        self.foreground  = ""
class Settings:
    def __init__(self):
        self.colors = Colors()
        self.search_delay_ms = 100
class State:
    def __init__(self):
        self.groups = {}
        self.marks = {}
        self.group_ids = []
        self.settings = Settings()

class Data:
    def __init__(self, config):
        self.state = State()
        pass 
    def get_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    def save(self):
        pass
    def load(self):
        pass
    def add_group(self, name):
        g = Group()
        g.id = str(uuid.uuid4())
        g.name = name
        self.state.group_ids.append(g.id)
        self.state.groups[g.id] = g
        return g
    def add_mark(self, group_id, name, url):
        m = Mark()
        m.id = str(uuid.uuid4())
        m.icon = 'fa-regular fa-bookmark'
        m.name = name
        m.url = url
        m.group_id = group_id
        self.state.groups[group_id].mark_ids.append(m.id)
        self.state.marks[m.id] = m
        return m
    def pop_group(self, id):
        for mark_id in self.state.groups[id].mark_ids:
            self.state.marks.pop(mark_id)
        self.state.group_ids.remove(id)
        return self.state.groups.pop(id)
    def pop_mark(self, id):
        mark = self.state.marks[id]
        self.state.groups[mark.group_id].mark_ids.remove(id)
        return  self.state.marks.pop(id)


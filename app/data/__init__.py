import uuid
import json
import os

class Mark:
    def __init__(self):
        self.id  = ""
        self.group_id  = ""
        self.url  = ""
        self.name  = ""
        self.highlight  = ""
        self.icon = ""
    def __str__(self):
        s = ''
        s += f'id: {self.id}\n'
        s += f'group_id: {self.group_id}\n'
        s += f'url: {self.url}\n'
        s += f'name: {self.name}\n'
        s += f'highlight: {self.highlight}\n'
        s += f'icon: {self.icon}'
        return s
    def from_json(self, d):
        self.id = d['id'] if 'id' in d else self.id
        self.group_id = d['group_id'] if 'group_id' in d else self.group_id
        self.url = d['url'] if 'url' in d else self.url
        self.name = d['name'] if 'name' in d else self.name
        self.highlight = d['highlight'] if 'highlight' in d else self.highlight
        self.icon = d['icon'] if 'icon' in d else self.icon

class Group:
    def __init__(self):
        self.mark_ids = []
        self.id = ""
        self.name = ""
    def __str__(self):
        s = f'id: {self.id}\n'
        s = f'name: {self.name}\n'
        s = f'mark_ids:\n'
        s += '\n'.join([f'  {i}' for i in self.mark_ids])
        return s
    def from_json(self, d):
        self.mark_ids = [str(i) for i in d['mark_ids']] if 'mark_ids' in d else self.mark_ids
        self.id = d['id'] if 'id' in d else self.id
        self.name = d['name'] if 'name' in d else self.name

class Settings:
    def __init__(self):
        self.search_delay_ms = 100
        self.mark_width = 60
        self.data_file = './data.json'
    def __str__(self):
        s = 'colors:\n'
        s += '\n'.join([f'  {i}' for i in str(self.colors).split('\n')]) + '\n'
        s += f'search_delay: {self.search_delay_ms}'
        return s
    def from_json(self, d):
        self.search_delay_ms = int(d['search_delay_ms']) if 'search_delay_ms' in d else self.search_delay_ms
        self.mark_width = int(d['mark_width']) if 'mark_width' in d else self.mark_width
        self.data_file = d['data_file'] if 'data_file' in d else self.data_file

class State:
    def __init__(self):
        self.groups = {}
        self.marks = {}
        self.group_ids = []
    def __str__(self):
        s = 'settings:\n'
        s += '\n'.join([f'  {i}' for i in str(self.settings).split('\n')]) + '\n'
        s += 'group_ids:\n'
        s += '\n'.join([f'  {i}' for i in self.group_ids]) + '\n'
        s += 'groups:\n'
        for gid in self.groups:
            s += f'{gid}:\n'
            s += '\n'.join([f'  {i}' for i in str(self.groups[gid]).split('\n')]) + '\n'
        s += 'marks:\n'
        for mid in self.marks:
            s += f'{mid}:\n'
            s += '\n'.join([f'  {i}' for i in str(self.marks[mid]).split('\n')]) + '\n'
        return s
    def from_json(self, d):
        if 'groups' in d:
            self.groups = {}
            for gid in d['groups']:
                g = Group()
                g.from_json(d['groups'][gid])
                self.groups[gid] = g
        if 'marks' in d:
            self.marks = {}
            for mid in d['marks']:
                m = Mark()
                m.from_json(d['marks'][mid])
                self.marks[mid] = m
        if 'group_ids' in d:
            self.group_ids = [str(i) for i in d['group_ids']]

class Data:
    def __init__(self, config):
        self.state = State()
        self.settings = Settings()
        self.settings.from_json(config)
    def get_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    def save(self):
        with open(self.settings.data_file, 'w') as f:
            j = json.dumps(self.state, default=lambda o: o.__dict__)
            f.write(j)
    def load(self):
        self.state = State()
        if os.path.isfile(self.settings.data_file):
            with open(self.settings.data_file, 'r') as f:
                self.state.from_json(json.loads(f.read()))
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


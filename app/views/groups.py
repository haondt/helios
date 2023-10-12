from flask import Flask, jsonify, render_template, request

class ViewGroup:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.marks = []
class ViewMark:
    def __init__(self):
        self.id  = ""
        self.group_id  = ""
        self.url  = ""
        self.link = ""
        self.name  = ""
        self.highlight  = ""
        self.icon = ""

def create_view_marks(state, mark_ids):
    marks = []
    for mid in mark_ids:
        sm = state.marks[mid]
        vm = ViewMark()
        vm.id = sm.id
        vm.group_id = sm.group_id
        if sm.url.startswith('http'):
            vm.link = sm.url
        else:
            vm.link = "//" + sm.url
        vm.url = sm.url
        vm.name = sm.name
        vm.icon = sm.icon
        vm.highlight = sm.highlight
        marks.append(vm)
    return marks

def create_view_groups(state):
    return [create_view_group(state, gid) for gid in state.group_ids]

def create_view_group(state, group_id):
    sg = state.groups[group_id]
    vg = ViewGroup()
    vg.id = sg.id
    vg.name = sg.name
    vg.marks += create_view_marks(state, sg.mark_ids)
    return vg

def apply(helios, data):
    @helios.route('/hx/groups', methods=['GET', 'POST'])
    def get_groups():
        if request.method == 'GET':
            return render_template('groups.html', groups=create_view_groups(data.state))
        elif request.method == 'POST':
            groups = [data.state.groups[i] for i in data.state.group_ids]
            ids = request.form.getlist('ids')
            assert len(set(ids)) == len(set(data.state.group_ids))
            assert all([i in data.state.group_ids for i in ids])
            data.state.group_ids = ids
            return render_template('groups.html', groups=create_view_groups(data.state))

    @helios.route('/hx/groups/readonly', methods=['GET'])
    def get_groups_readonly():
        return render_template('groups-readonly.html', groups=create_view_groups(data.state))

    @helios.route('/hx/group/<id>', methods=['POST', 'GET'])
    def get_group(id):
        if request.method == 'POST':
            return None
        elif request.method == 'GET':
            return render_template('group.html', group=create_view_group(data.state, id))
        return None

    @helios.route('/hx/group/<id>/edit', methods=['GET'])
    def edit_group(id):
        return render_template('group-edit.html', group=create_view_group(data.state, id))


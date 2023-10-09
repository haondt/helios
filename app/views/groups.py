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
        self.name  = ""
        self.highlight  = ""

def create_view_groups(state):
    groups = []
    for gid in state.group_ids:
        sg = state.groups[gid]
        vg = ViewGroup()
        vg.id = sg.id
        vg.name = sg.name
        
        for mid in sg.mark_ids:
            sm = state.marks[mid]
            vm = ViewMark()
            vm.id = sm.id
            vm.group_id = sm.group_id
            vm.url = sm.url
            vm.name = sm.name
            vm.highlight = sm.highlight
            vg.marks.append(vm)

        groups.append(vg)
    return groups

def create_view_group(state, group_id):
    sg = state.groups[group_id]
    vg = ViewGroup()
    vg.id = sg.id
    vg.name = sg.name
    
    for mid in sg.mark_ids:
        sm = state.marks[mid]
        vm = ViewMark()
        vm.id = sm.id
        vm.group_id = sm.group_id
        vm.url = sm.url
        vm.name = sm.name
        vm.highlight = sm.highlight
        vg.marks.append(vm)

    return vg

def apply(helios, data):
    @helios.route('/groups', methods=['GET', 'POST'])
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

    @helios.route('/group/<id>', methods=['POST', 'GET'])
    def get_group(id):
        if request.method == 'POST':
            return None
        elif request.method == 'GET':
            return render_template('group-view.html', group=create_view_group(data.state, id))
        return None

    @helios.route('/group/<id>/edit', methods=['GET'])
    def edit_group(id):
        return render_template('group-edit.html', group=create_view_group(data.state, id))


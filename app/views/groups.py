from flask import Flask, jsonify, render_template, request
from .marks import ViewMark, create_view_marks

class ViewGroup:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.marks = []

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
        return render_template('groups-readonly.html', groups=create_view_groups(data.state), settings=data.state.settings)

    @helios.route('/hx/groups/search', methods=['POST'])
    def search_groups():
        groups = create_view_groups(data.state)
        q = request.form['search-query'].upper()
        for group in groups:
            if q in group.name.upper():
                continue
            group.marks = [m for m in group.marks if q in m.url.upper() or q in m.name.upper()]
        groups = [g for g in groups if len(g.marks) > 0]
        return render_template('groups-search-result.html', groups=groups)

    @helios.route('/hx/group/<id>', methods=['PUT', 'GET', 'DELETE'])
    def group(id):
        if request.method == 'PUT':
            id = request.form['id']
            name = request.form['name']
            data.state.groups[id].name = name
        elif request.method == 'DELETE':
            data.pop_group(id)
            return ""
        return render_template('group.html', group=create_view_group(data.state, id))

    @helios.route('/hx/group', methods=['POST'])
    def create_group():
        group = data.add_group("")
        return render_template('group-and-marks.html', group=create_view_group(data.state, group.id), edit_group=True)

    @helios.route('/hx/group/<id>/edit', methods=['GET'])
    def edit_group(id):
        return render_template('group-edit.html', group=create_view_group(data.state, id))


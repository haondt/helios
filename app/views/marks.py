from flask import Flask, jsonify, render_template, request
import json

class ViewMark:
    def __init__(self):
        self.id  = ""
        self.group_id  = ""
        self.url  = ""
        self.display_url = ""
        self.link = ""
        self.name  = ""
        self.highlight  = ""
        self.icon = ""

class ViewMarkOptions:
    def __init__(self, mark_width):
        self.mark_width = mark_width

def create_view_mark(state, options, mark_id):
    sm = state.marks[mark_id]
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

    partial_mark_len = len("[] ()") + len(vm.name)
    allowed_url_len = options.mark_width - partial_mark_len
    if allowed_url_len < len(vm.url) and allowed_url_len > 0:
        vm.display_url = vm.url[:max(0, allowed_url_len-3)] + "..."
    else:
        vm.display_url = vm.url

    return vm

def create_view_mark_options(base_options, readonly):
    if readonly:
        return ViewMarkOptions(max(1, base_options.mark_width))
    else:
        return ViewMarkOptions(max(1, base_options.mark_width-14))

def create_view_marks(state, options, mark_ids):
    return [create_view_mark(state, options, mid) for mid in mark_ids]

def apply(helios, data):
    view_mark_options = create_view_mark_options(data.settings, False)

    @helios.route('/hx/mark', methods=['POST'])
    def create_mark():
        mark = data.add_mark(request.form['group_id'], "", "")
        data.save()
        return render_template('mark-edit.html', mark=create_view_mark(data.state, data.settings, mark.id))

    @helios.route('/hx/marks', methods=['POST'])
    def sort_marks():
        group_id = request.form['group_id']
        group = data.state.groups[group_id]
        ids = request.form.getlist('ids')
        assert len(set(ids)) == len(set(group.mark_ids))
        assert all([i in group.mark_ids for i in ids])
        group.mark_ids = ids
        data.save()
        return ''

    @helios.route('/hx/mark/<id>', methods=['GET', 'PUT', 'DELETE'])
    def mark(id):
        if request.method == 'PUT':
            id = request.form['id']
            mark = data.state.marks[id]
            mark.name = request.form['name']
            mark.url = request.form['url']
            mark.icon = request.form['icon']
            data.save()
        elif request.method == 'DELETE':
            data.pop_mark(id)
            data.save()
            return ""
        return render_template('mark.html', mark=create_view_mark(data.state, view_mark_options, id))

    @helios.route('/hx/mark/<id>/edit', methods=['GET'])
    def edit_mark(id):
        return render_template('mark-edit.html', mark=create_view_mark(data.state, data.settings, id))

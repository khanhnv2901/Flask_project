from flask import Blueprint, request, jsonify
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('index.html', user=current_user)


@views.route('/delete-note', methods=['GET', 'POST'])
def delete_note():
    note = json.loads(request.data)
    print(note)
    note_id = note['note_id']
    
    result = Note.query.get(note_id)
    if result:
        if result.user_id == current_user.id:
            db.session.delete(result)
            db.session.commit()
    return jsonify({"code": 200})

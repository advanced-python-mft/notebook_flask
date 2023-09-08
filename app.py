from flask import Flask, render_template, redirect, url_for, flash
import json
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session management
notes = []

# Note Form
class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    
@app.route('/')
def index():
    notes_with_index = [(idx, note) for idx, note in enumerate(notes)]
    return render_template('index.html', notes=notes_with_index)

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        note = {'title': title, 'content': content, 'created_at': current_datetime}
        notes.append(note)
        save_notes_to_json()
        flash('Note created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('create_note.html', form=form)

@app.route('/view/<int:id>')
def view_note(id):
    note = notes[id]
    return render_template('view_note.html', note=note, id=id)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    form = NoteForm()
    note = notes[id]

    form.title.data = note['title']
    form.content.data = note['content']

    if form.validate_on_submit():
        note['title'] = form.title.data
        note['content'] = form.content.data
        save_notes_to_json()
        flash('Note updated successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_note.html', form=form, note=note, id=id)


@app.route('/delete/<int:id>')
def delete_note(id):
    del notes[id]
    save_notes_to_json()
    flash('Note deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/export/<int:id>')
def export_to_pdf(id):
    note = notes[id]
    response = canvas.Canvas(f'note_{id}.pdf')
    response.drawString(100, 750, note['title'])
    response.drawString(100, 700, note['content'])
    response.showPage()
    response.save()
    return redirect(url_for('index'))

def save_notes_to_json():
    with open('notes.json', 'w') as json_file:
        json.dump(notes, json_file)

if __name__ == '__main__':
    try:
        with open('notes.json', 'r') as json_file:
            notes = json.load(json_file)
    except FileNotFoundError:
        notes = []
    app.run(debug=True)

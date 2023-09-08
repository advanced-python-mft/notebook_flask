from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# A list to store the notes
notes = []

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add():
    note = request.form['note']
    notes.append(note)
    return redirect('/')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        note = request.form['note']
        notes[index] = note
        return redirect('/')
    else:
        return render_template('edit.html', index=index, note=notes[index])

@app.route('/delete/<int:index>')
def delete(index):
    del notes[index]
    return redirect('/')

if __name__ == '__main__':
    app.run()
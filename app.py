from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "Secret Key"

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully", "success")
            return redirect('/')
        except:
            flash("An error occurred while adding the task", "error")

    tasks = Task.query.order_by(Task.date_created).all()
    return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully", "success")
    except:
        flash("An error occurred while deleting the task", "error")
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        new_content = request.form['content']

        if new_content:
            task.content = new_content
            try:
                db.session.commit()
                flash("Task updated successfully", "success")
                return redirect('/')
            except:
                flash("An error occurred while updating the task", "error")
        else:
            flash("Content cannot be empty", "error")
    return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('main.html', items=items)

@app.route('/add', methods=['POST', 'GET'])
def add_item():
    name = request.form['name']
    description = request.form['description']
    item = Item(name=name, description=description)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('edit.html', item=item)

@app.route('/update/<int:item_id>', methods=['POST', 'GET'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    item.name = request.form['name']
    item.description = request.form['description']
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
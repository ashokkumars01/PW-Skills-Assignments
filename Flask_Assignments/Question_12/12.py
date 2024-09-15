from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Counter variable to demonstrate real-time updates
counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global counter
    emit('update_counter', {'counter': counter}, broadcast=True)

@socketio.on('increment')
def handle_increment():
    global counter
    counter += 1
    emit('update_counter', {'counter': counter}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

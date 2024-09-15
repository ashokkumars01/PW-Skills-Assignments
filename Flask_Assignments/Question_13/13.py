from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dummy notifications data
notifications = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notify/<message>')
def notify(message):
    global notifications
    notifications.append(message)
    # Emit the notification to all connected clients
    socketio.emit('notification', {'message': message}, broadcast=True)
    return f'Notification sent: {message}'

@socketio.on('connect')
def handle_connect():
    # Send existing notifications to the newly connected client
    global notifications
    for notification in notifications:
        emit('notification', {'message': notification})

if __name__ == '__main__':
    socketio.run(app, debug=True)

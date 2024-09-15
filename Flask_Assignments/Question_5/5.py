from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Set a secret key for session management (replace with a strong secret)
app.secret_key = 'hello'

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    # Perform authentication here (e.g., check against a database)
    if username:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
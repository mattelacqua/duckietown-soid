# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import os



# Start up Flask web env
template_dir = os.path.abspath('webserver/html/')
app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app,cors_allowed_origins="*")
f = open('webserver.out', 'a', os.O_NONBLOCK)

# Home page for website
@app.route("/")
def index():
    return render_template("index.html")

# On socket update,
@socketio.on("update")
def update(data):
    global f
    print('Current Value', data['value'])
    if int(data['value']) > 50:
        print("Writing: {0}".format(data['value']))
        f.write(data['value'])
        f.flush()
    else:
        print("Not Writing: {0}".format(data['value']))




if __name__ == '__main__':
    socketio.run(app)

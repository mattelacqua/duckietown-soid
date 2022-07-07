# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from webserver.gui_utils import guiInput
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Start up Flask web env
template_dir = os.path.abspath('webserver/html/')
app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app,cors_allowed_origins="*")
fifo_out = 'webserver/webserver.out'
out = open(fifo_out, "wb", os.O_NONBLOCK)


# Home page for website
@app.route("/")
def index():
    #return render_template("index.html")
    return render_template("test.html")

# On socket update,
@socketio.on("update")
def update(data):
    global out
    value = int(data['value'])
    agent_change = guiInput(agent=True, agent_id="agent0", cur_pos=[0, 0, 0], cur_angle=value)
    pickled = agent_change.serialize()
    out.write(pickled)
    out.flush()
        

@socketio.on("hello")
def hello():
    return



if __name__ == '__main__':
    socketio.run(app)

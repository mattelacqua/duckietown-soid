# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from webserver.gui_utils import guiAgent, guiEnv, guiDone, read_init, serialize
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Start up Flask web env
template_dir = os.path.abspath('webserver/html/')
app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app,cors_allowed_origins="*")
fifo_out = 'webserver/webserver.out'
fifo_in = 'webserver/webserver.in'
out = open(fifo_out, "wb", os.O_NONBLOCK)
inp = open(fifo_in, "rb", os.O_NONBLOCK)

print("HERE")
agent_list, env_info = read_init(inp)
print("AGENT LIST AGENT LIST")
print(agent_list)
print("ENV INFO")
print(env_info)

# Home page for website
@app.route("/")
def index():
    #return render_template("index.html")
    return render_template("test.html", agent_list=agent_list, env_info=env_info)

# On socket update,
@socketio.on("agent_angle")
def agent_angle(data):
    global out
    a_id = str(data['id'])
    angle = int(data['value'])
    agent_change = guiAgent(change="angle", agent_id=a_id, cur_angle=angle)
    serialize(agent_change, out)
 
@socketio.on("agent_pos")
def agent_pos(data):
    global out
    a_id = str(data['id'])
    pos = list(data['value'])
    agent_change = guiAgent(change="pos", agent_id=a_id, cur_pos=[pos[0], 0, pos[1]])
    serialize(agent_change, out)

@socketio.on("increment_pos")
def increment_pos(data):
    global out
    print("CALLING INCREMENT POS")
    a_id = str(data['id'])
    direction = str(data['direction'])
    agent_change = guiAgent(change="inc_pos", agent_id=a_id, inc_direction=direction)
    serialize(agent_change, out)


@socketio.on("resume_simulation")
def resume_simulation():
    global out
    to_send = guiDone(done=True)
    serialize(to_send, out)



if __name__ == '__main__':
    socketio.run(app)

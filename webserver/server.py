# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from webserver.gui_utils import guiInput, read_init, serialize
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
    value = int(data['value'])
    agent_change = guiInput(agent=True, change="angle", agent_id=a_id, cur_pos=[0, 0, 0], cur_angle=value)
    serialize(agent_change, out)
 
@socketio.on("agent_pos")
def agent_pos(data):
    global out
    a_id = str(data['id'])
    value = list(data['value'])
    agent_change = guiInput(agent=True, change="pos", agent_id=a_id, cur_pos=[value[0], 0, value[1]])
    serialize(agent_change, out)

@socketio.on("increment_pos")
def increment_pos(data):
    global out
    print("CALLING INCREMENT POS")
    a_id = str(data['id'])
    direction = str(data['direction'])
    print("A_id {0}".format(a_id))
    print("Direction {0}".format(direction))
    agent_change = guiInput(agent=True, change="inc_pos", agent_id=a_id, inc_direction=direction)
    serialize(agent_change, out)
    print("DONE")


@socketio.on("resume_simulation")
def resume_simulation():
    global out
    print("\n\n\n HERE \n\n\n ")
    to_send = guiInput(done=True)
    serialize(to_send, out)



if __name__ == '__main__':
    socketio.run(app)

# Flask imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from webserver.gui_utils import guiInput



# Start up Flask web env
template_dir = os.path.abspath('webserver/html/')
app = Flask(__name__, template_folder=template_dir)
socketio = SocketIO(app,cors_allowed_origins="*")
fifo_out = 'webserver/webserver.out'
out = open(fifo_out, "wb", os.O_NONBLOCK)


# Home page for website
@app.route("/")
def index():
    return render_template("index.html")

# On socket update,
@socketio.on("update")
def update(data, data2):
    global out
    if int(data['value']) > 98:
        out.close()
    elif int(data['value']) > 50:
        print("Trying to serialize agent angle change")
        agent_change = guiInput(agent=True, agent_id="agent0", cur_pos=[0, 0, 0], cur_angle=0.0)
        pickled = agent_change.serialize()
        print("Pickled {0}".format(pickled))
        out.write(pickled)
        out.flush()
        

@socketio.on("hello")
def hello():
    return



if __name__ == '__main__':
    socketio.run(app)

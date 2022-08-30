from app_pkg import app, socketio
from app_pkg.models import *


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


# add extra line of code to dodge pycharm reformatting
app = app
socketio = socketio

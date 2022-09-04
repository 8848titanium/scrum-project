from app_pkg import app, socketio
from app_pkg.models import *


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


# add extra line of code to dodge pycharm reformatting
app = app
socketio = socketio

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)

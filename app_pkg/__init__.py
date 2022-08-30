from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from config import Config

ASYNC_MODE = None

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, async_mode=ASYNC_MODE)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app_pkg import routes, models
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

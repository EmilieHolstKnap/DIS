from flask import Flask
from database import init_db
from controllers import event

init_db()

app = Flask(__name__)

app.register_blueprint(event.bp)

from flask import Flask
from database import init_db
from controllers import event, auth

init_db()

app = Flask(__name__)
app.secret_key = "dev-secret-key"

app.register_blueprint(event.bp)
app.register_blueprint(auth.bp)

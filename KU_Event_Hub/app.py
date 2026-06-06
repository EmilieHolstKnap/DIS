import os
from flask import Flask
from controllers import event, auth

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

app.register_blueprint(event.bp)
app.register_blueprint(auth.bp)

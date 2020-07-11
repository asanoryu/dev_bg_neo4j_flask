import os

from app import app

app.secret_key = os.urandom(24)

app.run("0.0.0.0", debug=True)

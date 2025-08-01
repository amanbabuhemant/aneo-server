from flask import Flask
from routes import routes
import os
from config import *

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(routes)

for rdir in [ "animations", "revisions" ]:
    if not os.path.exists(rdir):
        os.mkdir(rdir)

def run_app():
    app.run(debug=True)

if __name__ == "__main__":
    run_app()

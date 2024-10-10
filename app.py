from flask import Flask
from blueprints.accident import accident_bp
app = Flask(__name__)

app.register_blueprint(accident_bp)


if __name__ == '__main__':
    app.run(debug=True)

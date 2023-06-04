from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "It's server one replying"
@app.route('/sv1')
def hello1():
    return "It's server one replying"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



from flask import Flask, redirect, url_for
app = Flask(__name__)
authorize = False

@app.route('/')
def home():
    return "test!"

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    authorize = True
    if authorize:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()



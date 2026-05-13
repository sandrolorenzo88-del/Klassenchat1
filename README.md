from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

users = []
messages = []

CLASSROOM = {
    "id": 1,
    "name": "Klassenraum MVP",
    "beschreibung": "Einfacher gemeinsamer Klassenchat"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip()

        if username and username not in users:
            users.append(username)

        return redirect(url_for("chat", username=username))

    return render_template("index.html")

@app.route("/chat/<username>", methods=["GET", "POST"])
def chat(username):
    if username not in users:
        users.append(username)

    if request.method == "POST":
        text = request.form.get("message", "").strip()

        if text:
            messages.append({
                "sender": username,
                "text": text,
                "time": datetime.now().strftime("%H:%M:%S")
            })

    return render_template(
        "chat.html",
        username=username,
        users=users,
        messages=messages,
        classroom=CLASSROOM
    )

@app.route("/leave/<username>")
def leave(username):
    if username in users:
        users.remove(username)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

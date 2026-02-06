from flask import Flask, request
import redis
import os

app = Flask(__name__)
r = redis.Redis(host="redis-service", port=6379, decode_responses=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        msg = request.form.get("message")
        r.lpush("guestbook", msg) # שומר הודעה חדשה
    
    messages = r.lrange("guestbook", 0, 9) # שולף את 10 האחרונות
    html = "<h1>Guestbook</h1><form method='post'><input name='message'><button>Send</button></form>"
    html += "<ul>" + "".join([f"<li>{m}</li>" for m in messages]) + "</ul>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
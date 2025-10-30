from flask import Flask, render_template, jsonify
import os, socket, time, datetime as dt

app = Flask(__name__)

START_TIME = time.time()

def now_iso():
    return dt.datetime.utcnow().isoformat() + "Z"

@app.route("/")
def index():
    data = {
        "color": os.environ.get("COLOR", "blue"),
        "image_tag": os.environ.get("IMAGE_TAG", os.environ.get("TAG", "latest")),
        "hostname": socket.gethostname(),
        "time_utc": now_iso(),
        "uptime_seconds": int(time.time() - START_TIME),
        "registry": os.environ.get("REGISTRY", "docker.io"),
        "docker_user": os.environ.get("DOCKER_USER", "zk0061"),
        "service_name": os.environ.get("SERVICE_NAME", "demo-web-svc"),
    }
    return render_template("index.html", **data)

@app.route("/api/info")
def api_info():
    return jsonify(
        status="ok",
        color=os.environ.get("COLOR", "blue"),
        image_tag=os.environ.get("IMAGE_TAG", os.environ.get("TAG", "latest")),
        hostname=socket.gethostname(),
        time_utc=now_iso(),
        uptime_seconds=int(time.time() - START_TIME),
    )

@app.route("/healthz")
def healthz():
    # simple liveness probe
    return "ok", 200

@app.route("/readyz")
def readyz():
    # simple readiness probe (extend if you add dependencies)
    return "ready", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

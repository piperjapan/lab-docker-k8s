from flask import Flask, render_template
from redis import Redis, RedisError
import socket
import os
from os.path import dirname, join
from dotenv import load_dotenv

DOTENV_PATH = join(dirname(__file__), ".env")
load_dotenv(DOTENV_PATH)

APP_PORT = os.getenv("APP_PORT", 8080)
REDIS_HOST = os.getenv("DB_HOST", "redis")
REDIS_PORT = os.getenv("DB_PORT", 6379)
MESSAGE = os.getenv("MESSAGE", "Here I'm having fun with Containers.")

print(" * Connecting to Redis: {}:{}".format(REDIS_HOST, REDIS_PORT))
redis = Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=2, socket_timeout=2,
)
app = Flask(__name__)


@app.route("/")
def helloworld():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "Hello, World."

    return render_template(
        "index.html", visits=visits, hostname=socket.gethostname(), message=MESSAGE
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)

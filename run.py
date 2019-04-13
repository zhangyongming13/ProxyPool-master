from proxypool.api import app
from proxypool.db import RedisClient
from proxypool.schedule import Schedule
from proxypool.setting import FLASK_PORT, FLASK_HOST, HOST, PORT
import redis


def main():
    # db = redis.Redis(host=HOST, port=PORT)
    # db.flushall()
    conn = RedisClient()
    conn.flush()
    s = Schedule()
    s.run()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)


if __name__ == '__main__':
    main()


from flask import Flask, g

from .db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/get')
def get_proxy():
    """
    Get a random proxy.
    :return: random proxy
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies.
    :return: the count of proxies.
    """
    conn = get_conn()
    count1 = str(conn.greatcount())
    count2 = str(conn.count())
    s = 'Test success number: {} </br>Total Proxies in Pool: {}'.format(count1, count2)
    return s




if __name__ == '__main__':
    app.run()

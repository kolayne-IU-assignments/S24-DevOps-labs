import datetime

from flask import Flask
import requests

from cache import cache_for


app = Flask(__name__)


# In case of high load, to avoid frequent requests, cache results for
# one second
@cache_for(1000)
def get_time():
    """
    Get current Moscow time from worldtimeapi.org.

    The returned value is of type `datetime.time` and it may be up to
    1000ms out of date, as results of calls to the function are cached
    for up to 1 second.
    """
    r = requests.get('http://worldtimeapi.org/api/timezone/Europe/Moscow')
    dt = datetime.datetime.fromisoformat(r.json()['datetime'])
    return dt.time()


@app.route('/')
def index():
    time = get_time()
    return f"In MSK it's {time.hour}:{time.minute}:{time.second}. " \
        "Have you brushed your teeth today yet?"


if __name__ == '__main__':
    app.run()

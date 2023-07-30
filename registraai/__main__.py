from urllib.parse import urlparse

from db import init_db
from rest import app

if __name__ == "__main__":
    init_db(app)

    url = urlparse('http://0.0.0.0:8001')
    host, port = url.hostname, url.port
    app.run(host=host, port=port, debug=True)

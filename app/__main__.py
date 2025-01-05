from clear import clear
from eventlet import listen
from eventlet.wsgi import server

from app import create_app

app = create_app()
clear()

clear()
if __name__ == "__main__":
    server(listen(("localhost", 5002)), app)

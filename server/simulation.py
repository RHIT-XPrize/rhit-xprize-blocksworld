import sys
import socketio
import tornado.web
import eventlet

import config as cfg

def main():
    config = cfg.generate_config(get_is_local())
    sio = socketio.Server()
    app = tornado.web.Application()
    socketApp = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 8080)), socketApp)

def get_is_local():
    args = sys.argv[1:]
    return len(args) == 0 or args[0] == 'local'

if __name__ == '__main__':
    main()
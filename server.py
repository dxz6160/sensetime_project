import tornado.ioloop
from tornado.httpserver import HTTPServer
import config
from application import Application
from tornado.options import define, options, parse_command_line

define('port', default=8000, type=int)

if __name__ == '__main__':
    #解析启动命令，python xxx.py  --port=80
    parse_command_line()

    server = HTTPServer(Application(), max_buffer_size=504857600, max_body_size=504857600)

    server.bind(options.port)

    server.start(1)  # Forks multiple sub-process

    tornado.ioloop.IOLoop.current().start()

    # app = Application()
    #
    # httpServer = tornado.httpserver.HTTPServer(app, max_buffer_size=504857600, max_body_size=504857600)
    #
    # app.listen(options.port)
    #
    # # httpServer.bind(config.options["port"])
    # #多进程
    # httpServer.start(1)

    # tornado.ioloop.IOLoop.current().start()
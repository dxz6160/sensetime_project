import tornado.web
from views import sensetime
import config
import os

class Application(tornado.web.Application):
    def __init__(self):
        handlers =  [
            (r'/home', sensetime.HomeHandler),
            (r'/post_pic', sensetime.PicHandler),
            (r'/play_pic', sensetime.PlayPicHandler),
            (r'/post_video', sensetime.VideoHandler),
            (r'/play_video', sensetime.PlayVideoHandler),
            (r'/(.*)$', tornado.web.StaticFileHandler,{"path": os.path.join(config.BASE_DIRS, "static/html"), "default_filename": "index.html"})
        ]

        super(Application, self).__init__(handlers, **config.settings)
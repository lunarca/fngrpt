# -*- coding: utf-8 -*-
import json

from handlers.BaseHandlers import *
from models.LinkModel import Link

from libs.ValidationError import ValidationError
from libs.SecurityDecorators import *


class ServeShortenerHandler(BaseHandler):
    """ Handler to serve the shortened URL
    """

    def get(self, *args, **kwargs):
        self._render_page(self.get_argument('l'))

    def _render_page(self, link):
        self.render('shortener/get.html', link=link)


class AnalysisHandler(BaseWebSocketHandler):
    """ Receives the analysis, store data, and forward user
    """

    io_loop = IOLoop.instance()

    def open(self):
        logging.debug("[WebSocket] Opened new analysis handler weboscket")
        self.uuid = self.get_argument("uuid", '')
        if self.get_current_link() is not None:
            self._setup_opcodes()
        else:
            logging.debug("[WebSocket] Link not found")
            self.close()

    def _setup_opcodes(self):
        self.opcodes = {
            'analyze': self.analyze,
        }

    def on_message(self, message):
        try:
            message = json.loads(message)
            if 'opcode' in message and message['opcode'] in self.opcodes:
                self.opcodes[message['opcode']](message)
            else:
                raise ValidationError("Malformed message")
        except ValidationError as error:
            self.send_error('Error', str(error))
        except:
            logging.exception('[WebSocket] Exception while routing JSON message')

    def get_current_link(self):
        _link = Link.by_uuid(self.uuid)
        if _link is not None:
            return _link
        else:
            logging.debug("No link found with uuid %s" % self.uuid)
            return None

    def send_error(self, title, message):
        msg = {
            'opcode': 'error',
            'title': title,
            'message': message,
        }
        self.io_loop.add_callback(self.write_message, msg)

    # Opcodes

    def analyze(self, message):
        # TODO: Implement analyze functionality
        pass
# -*- coding: utf-8 -*-

from handlers.BaseHandlers import *

class ServeShortenerHandler(BaseHandler):
	def get(self, *args, **kwargs):
		self._render_page()

	def _render_page(self, errors=None):
		self.render('shortener/get.html',
					link=)

class AnalysisHandler(BaseWebSocketHandler):

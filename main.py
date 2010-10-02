#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import random
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {
			'body_id': self.random_body_id()
		}
		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		# self.response.out.write('<html>testing</html>')

	def random_body_id(self):
		return random.choice(["darkblue", "lightblue", "yellow", "lightred", "darkred"])


class BookmarkHandler(webapp.RequestHandler):
	def put(self):
		self.response.out.write('putted')


def main():
	application = webapp.WSGIApplication([('/', MainHandler), ('/star', BookmarkHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
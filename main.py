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
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

class Bookmark(db.Model):
	uuid = db.StringProperty()
	title = db.StringProperty()
	url = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp.RequestHandler):
	def get(self):
		bookmarks = []
		
		uuid = self.request.get('uuid')
		if uuid:
			bookmarks_query = Bookmark.gql('WHERE uuid = :1 ORDER BY date', uuid)
			bookmarks = bookmarks_query.fetch(10)
		
		template_values = {
			'body_id': self.random_body_id(),
			'bookmarks': bookmarks
		}
		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		# self.response.out.write('<html>testing</html>')

	def random_body_id(self):
		return random.choice(["darkblue", "lightblue", "yellow", "lightred", "darkred"])


class BookmarksHandler(webapp.RequestHandler):
	"""Displays list of all starred pages"""
	def get(self):
		uuid = self.request.get('uuid')
		logging.debug("uuid %s is requesting all starred pages" % uuid)
		
		bookmarks_query = Bookmark.gql('WHERE uuid = :1 ORDER BY date', uuid)
		bookmarks = bookmarks_query.fetch(10)
		
		template_values = {
			'bookmarks': bookmarks
		}
		
		path = os.path.join(os.path.dirname(__file__), 'starred.html')
		self.response.out.write(template.render(path, template_values))


class BookmarkHandler(webapp.RequestHandler):
	def delete(self):
		uuid = self.request.get('uuid')
		url = self.request.get('url')
		logging.debug("uuid %s is UNSTARRING page %s" % (uuid, url))
		
		bookmark = Bookmark.gql("WHERE uuid = :1 AND url = :2", uuid, url).get()
		if not bookmark:
			self.response.out.write('NOTHING PERFORMED')
			pass
		else:
			bookmark.delete()
			self.response.out.write('deleted')

	def post(self):
		uuid = self.request.get('uuid')
		url = self.request.get('url')
		title = self.request.get('title')
		logging.debug("uuid %s is STARRING page %s" % (uuid, url))
		
		bookmark = Bookmark.gql("WHERE uuid = :1 AND url = :2", uuid, url).get()
		if not bookmark:
			bookmark = Bookmark()
			bookmark.uuid = uuid
			bookmark.title = title
			bookmark.url = url
			bookmark.put()
			self.response.out.write('putted as ' + str(bookmark.key().id()))
		else:
			self.response.out.write('NOTHING PERFORMED')
			pass


def main():
	logging.getLogger().setLevel(logging.DEBUG)
	application = webapp.WSGIApplication([('/', MainHandler), ('/star', BookmarkHandler), ('/star', BookmarkHandler), ('/starred', BookmarksHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
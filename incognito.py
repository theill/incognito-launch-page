#!/usr/bin/env python
#

import os
import random
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import webapp2
import stripe

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

class PrivacyPage(webapp2.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'privacy.html')
		self.response.out.write(template.render(path, {}))

class Charge(webapp2.RequestHandler):
	def post(self):
		# stripe.api_key = "x7bjlAXppzhibZBNtUG7Gz4lIKBefu8R" # dev
		stripe.api_key = "uBQbfhpYjsbvTOZlNcK4ScUNohZUtcZr" # prod
		token = self.request.get('stripeToken')

		try:
			charge = stripe.Charge.create(
				amount=500,
				currency="usd",
				card=token,
				description="Color Browser donation"
			)

			path = os.path.join(os.path.dirname(__file__), 'thanks.html')
			self.response.out.write(template.render(path, {}))
		except stripe.CardError, e: 
			self.response.out.write('Sorry. Could not complete your nice donation - ' + e)
			pass

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'body_id': self.random_body_id()
		}
		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

	def random_body_id(self):
		return random.choice(["darkblue", "lightblue", "yellow", "lightred", "darkred"])

app = webapp2.WSGIApplication([('/', MainPage), ('/privacy', PrivacyPage), ('/charge', Charge)])

#def main():
#	logging.getLogger().setLevel(logging.DEBUG)
#	application = webapp.WSGIApplication([('/', MainHandler), ('/star', BookmarkHandler), ('/star', BookmarkHandler), ('/starred', BookmarksHandler)], debug=True)
#	util.run_wsgi_app(application)
#
#
#if __name__ == '__main__':
#	main()
# Copyright 2016 Google Inc.
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

import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(_file_), 'templates')
jinja_env = jinja2.Environment(loader =  jinja2.FileSystemLoader(template_dir), 
	autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
  subject = db.StringProperty(required = True)
  blog = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  last_modified = db.DateTimeProperty(auto_now = True)

class MainPage(Handler):
  def get(self):
    posts = db.GqlQuery("SELECT * FROM Blog ORDER BY post_date LIMIT 10")
    self.render('front.html', posts = posts)

class NewPost(Handler):
	def render_newpost(self, subject = '', blog = '', error = ''):
		self.render('newpost.html', subject = subject, blog = blog, error = error)

	def post(self):
    	subject = self.request.get('subject')
    	blog = self.request.get('blog')
        
        if not (subject and blog):
          error = 'You must enter a valid subject and blog'
          self.render_newpost(subject = subject, blog = blog, error = error)
          
        else:
          p = Blog(subject = subject, blog = blog)
          p.put()
          post_id = p.key().id()
          self.redirect('/blog/%s' % str(post_id))

class PostPage(Handler):
  def get(self, post_id):
    key = db.Key.from_path('Blog', int(post_id))
    post = db.get(key)
    if post:
      self.render('permalink.html', post = post)
    else:
      self.error(404)
      return

app = webapp2.WSGIApplication([
    ('/blog/?', MainPage),
  	('/blog/newpost', NewPost),
  	('/blog/([0-9]+)', PostPage),
], debug=True)
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

import webapp2

form="""
<form method='post'>
	Enter some text<br>
		<textarea value='%(text)s' name='text' rows='10' cols='50'>
		</textarea><br>
	<input type='submit'>
</form>
"""

def rot(s):
  alpha = ' abcdefghijklmnopqrstuvwxz'
  alpha = list(alpha)
  #s = s.lower()
  b = []
  
  for i in range(len(s)):
    index_in_alpha = alpha.index(s[i].lower())
    new_index = (index_in_alpha + 13) % 26
    new_value = alpha[new_index]
    b.append(new_value)
    
  for i in range(len(s)):
    l = list(s)
    if l[i] == l[i].upper():
      b[i] == b[i].upper()
    s = ''.join(b)

  return s
  
class MainPage(webapp2.RequestHandler):

	def write_form(self, text=''):
		self.response.out.write(form % {'text': text})

	def get(self):
        	self.write_form()

	def post(self):
		text = self.request.get('text')
		text = rot(text)
		self.write_form(text)

app = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True)

import webapp2
form="""
<form method='post'>
	<h1>Sign Up</h1><br>
        <label>Username
                <input name='username' value='%(username)s'>
        
	<br></label>
        <label>Password
                <input type='password' name='password'>

        <br></label>
        <label>Verify Password
                <input type='password' name='verify'>
  
        <br></label>
        <label>Email (optional)
                <input name='email' value='%(email)s'>
        
        </label><br>
        <div style='color: red'>%(error)s</div> 
        <input type='submit'>
</form>
""" 
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
      if USER_RE.match(username):
              return username

	
PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password, verify):
      if PASSWORD_RE.match(password) and password == verify:
              return password
              
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
      if not email or EMAIL_RE.match(email):
              return email
              
class MainPage(webapp2.RequestHandler):

        def write_form(self, error='', username='', email=''):
                self.response.out.write(form % {"error": error,
                                                "username": username,
                                                "email": email})
	def get(self):
		self.write_form()    

	def post(self):
                user_username = self.request.get('username')
                user_password = self.request.get('password')
                user_verify = self.request.get('verify')
                user_email = self.request.get('email')
                
                username = valid_username(user_username)
                password = valid_password(user_password, user_verify)
                email = valid_email(user_email)
                
                if not (username and password and email):
                        self.write_form('error', user_username, user_email)
                else:
                        self.redirect('/welcome')
                        
class WelcomePage(webapp2.RequestHandler):
        def get(self):
		username = self.request.get('username')
                self.response.out.write('Welcome ' + username)
                
app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', WelcomePage)], debug=True)

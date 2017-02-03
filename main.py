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
import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
            color: red;
            }
        </style>
    </head>
    <body>
        <h2>User Signup</h2>
"""

page_footer = """
</body>
</html>
"""

form = """
    <form method="post">
        <label>Username: <input type="text" name="username" value="%(username)s"></label><span class="error">%(error_username)s</span>
        <br>
        <label>Password: <input type="password" name="password"></label><span class="error">%(error_no_password)s</span>
        <br>
        <label>Verify Password: <input type="password" name="verify"></label><span class="error">%(error_password)s</span>
        <br>
        <label>Email (optional): <input type="text" name="email" value="%(email)s"></label><span class="error">%(error_email)s</span>
        <br>
        <br>
        <input type="submit">
    </form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_username="", error_no_password="", error_password="", error_email="", username="", email=""):
        self.response.out.write(page_header + form % {"error_username": error_username,
                                        "error_no_password":error_no_password,
                                        "error_password":error_password,
                                        "error_email":error_email,
                                        "username":username,
                                        "email":email} + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        username = cgi.escape(self.request.get('username'), quote=True)
        email = cgi.escape(self.request.get('email'), quote=True)
        password = cgi.escape(self.request.get('password'), quote=True)
        verify = cgi.escape(self.request.get('verify'), quote=True)

        error_username = ""
        error_no_password = ""
        error_password = ""
        error_email = ""

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        if not username or not USER_RE.match(username):
            error_username = "Please enter a valid username"
        if not password and not PASSWORD_RE.match(password):
            error_no_password = "Please enter a valid password"
        if not password == verify:
            error_password = "Passwords don't match"
        if email:
            if not EMAIL_RE.match(email):
                error_email = "Please enter a valid email address"

        if error_username or error_no_password or error_password or error_email:
            self.write_form(error_username, error_no_password, error_password, error_email, username, email)
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = cgi.escape(self.request.get('username'), quote=True)
        success_message = "Welcome, " + username + "!"
        self.response.out.write(page_header + "<h3>" + success_message + "</h3>" + page_footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', WelcomeHandler)
], debug=True)

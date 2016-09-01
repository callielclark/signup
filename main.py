import re
import webapp2

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style>
        body
        {
            display: block;
            margin: 8px
        }
        .error
        {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

signup_form = """
<form method="post">
<h1>Signup</h1>
<table>
    <tbody>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input name="username" type="text" value="{4}" value required></input>
                <span class="error">{0}</span>
            </td>
        </tr>

        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input name="password" type="password" required>
                <span class="error">{1}</span>
            </td>
        </tr>

        <tr>
            <td>
            <label for="verify">Verify Password</label>
            </td>
            <td>
                <input name="verify" type="password" required>
                <span class="error">{2}</span>
            </td>
        </tr>

        <tr>
            <td>
            <label for="email">Email (optional)</label>
            </td>
            <td>
                <input name="email" type="email" value="{5}" value>
                <span class="error">{3}</span>
            </td>
        </tr>
    </tbody>
</table>
<input type="Submit"/>
</form></center>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):

        temp = ""
        response = page_header + signup_form.format(temp, temp, temp, temp, temp, temp) + page_footer
        self.response.write(response)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error1 = ""
        error2 = ""
        error3 = ""
        error4 = ""

        if not valid_username(username):
            error1 = "Not a valid username"
            have_error = True

        if not valid_password(password):
            error2 = "Not a valid password"
            have_error = True

        elif password != verify:
            error3 = "Passwords didn't match"
            have_error = True

        if not valid_email(email):
            error4 = "Not a valid email"
            have_error = True

        if have_error:
            if error1 == "" and error4 == "":
                response = page_header + signup_form.format(error1, error2, error3, error4, username, email) + page_footer
            elif error1 == "":
                response = page_header + signup_form.format(error1, error2, error3, error4, username, "") + page_footer
            elif error4 == "":
                response = page_header + signup_form.format(error1, error2, error3, error4, "", email) + page_footer
            else:
                response = page_header + signup_form.format(error1, error2, error3, error4, "", "") + page_footer
            self.response.write(response)

        else:
            self.redirect('/welcome?{0}'.format(username))

class Welcome(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        username = url.split('?', 1)[-1]
        self.response.write("Welcome, " + username + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)

#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import MySQLdb as mdb
from template import display
from model.database import con
from passlib.hash import sha512_crypt

#Verifies that login credentials (username, password) are correct

def invalidLogin():
	print display("login.html").render()
	print "<script type='text/javascript'> \
	          alert('Incorrect username or password.');\
	          </script>" 

def main():
	form = cgi.FieldStorage()
	username = form.getvalue('username')
	password = form.getvalue('password')
	enc_password = ""

	cur = con.cursor()

	command = "SELECT password FROM Users WHERE username = %s";
	cur.execute(command, (username))
	row = cur.fetchone()
	if (row != None):
		enc_password = row[0]
		verify = sha512_crypt.verify(password, enc_password)
		if (verify):
			print display("home.html").render(username=username)
		else:
			invalidLogin() 
	else:
		invalidLogin()

if __name__ == '__main__':
	main()

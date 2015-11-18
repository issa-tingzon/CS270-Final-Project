#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import MySQLdb as mdb
from template import display
from model.database import con
from passlib.hash import sha512_crypt
import os, time, sys, session, Cookie, json

def main():

	form = cgi.FieldStorage()
	email = form.getvalue('email') #email of current user
	book = form.getvalue('ISBN')
	total = 0.0

	try:
		# Checks if book already exists in cart
		command = "SELECT * FROM UserCart WHERE Email=%s AND ISBN=%s"
		cur = con.cursor()
		cur.execute(command, (email, book))
		book_ = cur.fetchone()

		#Insert book into user's cart
		if book_ != None:
			command = "DELETE FROM UserCart WHERE Email=%s AND ISBN=%s"
			cur = con.cursor()
			cur.execute(command, (email, book))
			con.commit()
		
		command = "SELECT * FROM Users WHERE Email = '" + email + "'";
		cur.execute(command)
		user= cur.fetchone() 

		command = "SELECT ISBN, Title, Price from ComicBooks NATURAL JOIN UserCart WHERE Email='" + email + "'"
		
		cur.execute(command)
		rows = cur.fetchall()
		titles_temp = []
		for row in rows:
			titles_temp.append(row)

		titles = []
		total = 0
		for title in titles_temp:
			command = "SELECT Format from BookFormat NATURAL JOIN ComicBooks NATURAL JOIN UserCart WHERE ISBN='" + title[0] + "'"
			cur.execute(command)
			format = cur.fetchall()
			title = title + (format,)

			command = "SELECT WriterName, WriterId from ComicBooks NATURAL JOIN BookWriter NATURAL JOIN Writers WHERE ISBN='" + title[0] + "'"
			cur.execute(command)
			row = cur.fetchone()

			new_title = title + (row)
			titles.append(new_title)

		command = "SELECT TotalCost from Users WHERE Email='" + email + "'"
		cur.execute(command)
		row = cur.fetchone()
		total = row[0]

		command = "SELECT Price from ComicBooks WHERE ISBN='" + book + "'"
		cur.execute(command)
		row = cur.fetchone()
		price = row[0]

		if (total >= price):
			total = total - price

		command = "UPDATE Users SET TotalCost='" + str(total) + "' WHERE Email='" + email + "'"
		cur.execute(command)
		con.commit()

		print display("shopping-cart.html").render(user=user,titles=titles,total=total)

	except mdb.Error, e:
		if con:
			con.rollback()

if __name__ == '__main__':
	main()
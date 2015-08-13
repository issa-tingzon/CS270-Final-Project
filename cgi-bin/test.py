#!/usr/bin/python
import cgi
import MySQLdb as mdb
import sys

form = cgi.FieldStorage()
print "Content-Type: text/html"
print ""
print "<html>"
print "<h2>CGI Script Output</h2>"
print "<p>"
print "The user entered data are:<br>"
print "<b>First Name:</b> " + form["firstName"].value + "<br>"
print "<b>Last Name:</b> " + form["lastName"].value + "<br>"
print "<b>Position:</b> " + form["position"].value + "<br>"
print "</p>"
print "</html>"

try:
    con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

    cur = con.cursor()
    cur.execute("SELECT VERSION()")

    ver = cur.fetchone()
    
    print "Database version : %s " % ver
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()

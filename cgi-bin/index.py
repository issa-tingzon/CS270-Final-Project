#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
from template import display

def main():
    form = cgi.FieldStorage()
    print display("reg.html").render()

if __name__ == '__main__':
    main()

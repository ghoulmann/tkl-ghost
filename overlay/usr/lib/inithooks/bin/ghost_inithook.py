#!/usr/bin/python
"""Set Ghost email, name, URL, password

Option:
--password= unless provided, will ask interactively
--email= unless provided, will ask interactively
--URL= unless provided, will ask interactively
--uname= unless provided, will ask interactively

"""

import sys
import getopt
import subprocess
import hashlib
import bcrypt
import sqlite3 as lite
import locale
import dialog
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'password=', 'email=', 'URL=', 'uname='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    URL = ""
    uname = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--password':
            password = val
        elif opt == '--email':
            email = val
	elif opt == '--URL':
	    URL = val
        elif opt == '--username':
            uname = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password("Ghost Password","Enter new password for the Ghost blogger account (>= 8 characters).")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email("Ghost Email","Enter email address for the Ghost blogger account.","admin@example.com")

    if not URL:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')
        URL = d.get_input(
            "Ghost URL",
            "Enter the full URL of the Ghost Blog.",
            "http://tryghost.org")

    if not uname:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        uname = d.get_input(
            "Ghost Account Name",
            "Enter the Ghost blogger's name (real name recommended).",
            "Blogger Unknown")

#Kept for reference
#hash = hashlib.md5(password).hexdigest()

    hash = bcrypt.hashpw(password,bcrypt.gensalt())

#    m = MySQL()
#    Saving and mocking - not used in this build
#    m.execute('UPDATE xoops.xoops_users SET pass=\"%s\" WHERE uname=\"admin\";' % hash)
#    m.execute('UPDATE xoops.xoops_users SET email=\"%s\" WHERE uname=\"admin\";' % email)
#    m.execute('UPDATE xoops.xoops_config SET conf_value=\"%s\" WHERE conf_name=\"adminmail\";' % email)

    dbase = "/var/www/ghost/content/data/ghost.db"
    uid = "1"
    con = lite.connect(dbase)
    with con:
        cur = con.cursor()
        cur.execute('UPDATE Users SET Password=\"%s\" WHERE Id="1";' % hash)
        cur.execute('UPDATE Users SET name=\"%s\" WHERE id="1";' % uname)
        cur.execute('UPDATE Users SET email=\"%s\" WHERE id="1";' % email)
        cur.execute('UPDATE Users SET status=\"active\" WHERE id="1";')
        con.commit()

    for line in fileinput.FileInput("/opt/ghost/config.js",inplace=1):
        line = line.replace("http://my-ghost-blog.com",addy)
        print line

if __name__ == "__main__":
    main()

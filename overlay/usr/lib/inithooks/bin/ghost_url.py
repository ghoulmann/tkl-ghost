#!/usr/bin/python
"""Set Ghost URL

Option:
--URL= unless provided, will ask interactively

"""

import sys
import getopt
import subprocess
import fileinput
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
    addy = ""
    uname = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
	elif opt == '--URL':
	    addy = val

    if not addy:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        addy = d.get_input(
            "Ghost URL",
            "Enter the full URL of the Ghost Blog.",
            "http://tryghost.org")

    for line in fileinput.FileInput("/opt/ghost/config.js",inplace=1):
        line = line.replace("http://my-ghost-blog.com",addy)
        print line
    

if __name__ == "__main__":
    main()

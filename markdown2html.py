#!/usr/bin/python3
import sys
import os

if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    exit (1)

if not os.path.exists(sys.argv[1]):
    sys.stderr.write('Missing ' + sys.argv[1] + '\n')
    exit(1)

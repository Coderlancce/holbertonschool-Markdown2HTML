#!/usr/bin/python3
import sys
import os

if len(sys.argv) < 3:
    print('Usage: ./markdown2html.py README.md README.html')
    exit (1)

if not os.path.exists(sys.argv[1]):
    sys.stderr.write('Missing ' + sys.argv[1] + '\n')
    exit(1)
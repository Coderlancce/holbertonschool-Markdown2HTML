#!/usr/bin/python3
''' review if some file is here '''

import re
import hashlib
import sys
import os

if __name__ == "__main__":
    # check if the lenght are the correctly
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit (1)

    # check if the given file exist
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write('Missing ' + sys.argv[1] + '\n')
        exit(1)

    # open file in read mode
    with open(sys.argv[1]) as r:
        # open file in write mode
        with open(sys.argv[2], 'w') as w:
            # states for open and close tags in name
            change_status = False
            ordered_status = False
            paragraph = False
            # check each lines
            for line in r:
                # check for tags where are posible change in a line mandatory
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # check if md5 is required in the file for traslate
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                # check if is requiered delete letter "c"
                delete_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_inside = re.findall(r'\(\((.+?)\)\)', line)
                if delete_c:
                    remove_c_inside = ''.join(
                        c for c in remove_c_inside[0] if c not in 'Cc')
                    line = line.replace(delete_c[0], remove_c_inside)

                # check length line
                length = len(line)
                # check headlings
                headings = line.lstrip('#')
                # count the number of heading for headings if state
                heading_count = length - len(headings)
                # check unordered
                unordered = line.lstrip('-')
                # count the number of unordered for unordered if state
                unordered_count = length - len(unordered)
                # check ordered
                ordered = line.lstrip('*')
                # count the number of ordered for ordered if state
                ordered_count = length - len(ordered)

                # here check the number of heading and save the line information
                if 1 <= heading_count <= 6:
                    line = '<h{}>'.format(
                        heading_count) + headings.strip() + '</h{}>\n'.format(
                        heading_count)

                # here check if any unordered exist and check status for change and write in the new file
                if unordered_count:
                    if not change_status:
                        w.write('<ul>\n')
                        change_status = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if change_status and not unordered_count:
                    w.write('</ul>\n')
                    change_status = False

                # here check if any ordered exist and check status for change and write in the new file
                if ordered_count:
                    if not ordered_status:
                        w.write('<ol>\n')
                        ordered_status = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_status and not ordered_count:
                    w.write('</ol>\n')
                    ordered_status = False

                #check if nothing especial simbol exist and interptret how a paragraph
                if not (heading_count or change_status or ordered_status):
                    if not paragraph and length > 1:
                        w.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        w.write('<br/>\n')
                    elif paragraph:
                        w.write('</p>\n')
                        paragraph = False

                if length > 1:
                    w.write(line)

            # check if is needed close tag ol
            if ordered_status:
                w.write('</ol>\n')
            # check if is needed close tag p
            if paragraph:
                w.write('</p>\n')

    exit(0)

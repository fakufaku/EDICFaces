
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <fakufaku@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
# ----------------------------------------------------------------------------

# 2012-09-11 v0.1 Robin Scheibler

import urllib
import re
import sys

def print_help():
  print 'Usage: ' + sys.argv[0] + ' [OPTION]'
  print 'Options:'
  print '   -w <num> : images width'
  print '   -o <fil> : output file'
  print '   -c <col> : number of columns'
  print '   -h       : print this message'

# create regexp for the lines we are looking for
# example of line to match : 
# <td class="tdpeople" valign="top"><a href="http://people.epfl.ch/runwei.zhang">Zhang&nbsp;Runwei</a></td>
exp = re.compile('^\s*<td class="tdpeople" valign="top"><a href="http://people.epfl.ch/(?P<id>.*)">(?P<name>.*)</a></td>')

# height of pictures in the page
width = 100

# number of columns to display pictures
ncol = 5

# output file name
out_name = 'index.html'

# parse arguments
p = 1
while (p < len(sys.argv)):
  if (sys.argv[p] == '-w'):
    width = int(sys.argv[p+1])
    p += 2
  elif (sys.argv[p] == '-o'):
    out_name = sys.argv[p+1]
    p += 2
  elif (sys.argv[p] == '-c'):
    ncol = int(sys.argv[p+1])
    p += 2
  else:
    print_help()
    sys.exit(1)

# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen("http://phd.epfl.ch/page-19717-en.html")

# create an array of students
students = []

# Read and parse line by line
lines = f.readlines()
for l in lines:
  m = exp.match(l)
  # if match occurs, store name and id in array
  if m:
    students.append({'name' : m.group("name"), 'id' : m.group("id")})

# close pseudo file
f.close()

# open new file for output
f = open(out_name, 'w')

# make an html file
f.write('<html><head><title>Faces</title></head>\n')
f.write('<body><center>\n')

f.write('<h1>Here are the ' + str(len(students)) + ' faces of <a href="http://phd.epfl.ch/page-19717-en.html">EDIC</a>.</h1>\n')

# start a table
f.write('<p>\n')
f.write('<table>\n')

# start a row counter to keep track of when to break lines
sc = 0

# write students
for s in students:
  # create new row if necessary
  if (sc % ncol == 0):
    f.write('<tr>\n')

  # write student's face and name
  f.write('<td>\n')
  f.write('<center>\n')
  f.write('<a href="http://people.epfl.ch/' + s['id'] + '">\n')
  f.write('  <img src="http://people.epfl.ch/cgi-bin/people/getPhoto?id=' + s['id'] + '&show=" width=' + str(width) + '><br>\n')
  f.write('</a>\n')
  f.write('<b>' + s['name'] + '</b>\n')
  f.write('</center>\n')

  # update row if necessary
  sc += 1
  if (sc % ncol == 0):
    f.write('</tr>\n')

while (sc % ncol != 0):
  f.write('<td>\n')
  f.write('</td>\n')

  # update row if necessary
  sc += 1
  if (sc % ncol == 0):
    f.write('</tr>\n')

# end table
f.write('</table>\n')

f.write('<p> This page was generated using <a href="https://github.com/fakufaku/EDICFaces">EDICFaces</a>. 2012 (c) \n')
f.write('    <a href="http://fakufaku.github.com">Robin</a> <a href="http://people.epfl.ch/robin.scheibler">Scheibler</a>, \n')
f.write('    <a href=http://en.wikipedia.org/wiki/Beerware>Beerware License</a>.<br>\n')


# end html file
f.write('</body></html>\n')

# close file
f.close()


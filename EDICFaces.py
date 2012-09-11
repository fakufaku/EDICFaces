
import urllib
import re
import sys

# create regexp for the lines we are looking for
# example of line to match : 
# <td class="tdpeople" valign="top"><a href="http://people.epfl.ch/runwei.zhang">Zhang&nbsp;Runwei</a></td>
exp = re.compile('^\s*<td class="tdpeople" valign="top"><a href="http://people.epfl.ch/(?P<id>.*)">(?P<name>.*)</a></td>')

# height of pictures in the page
width = 100

# number of columns to display pictures
ncol = 3

# output file name
out_name = 'index.html'

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

# start a table
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
  f.write('<img src="http://people.epfl.ch/cgi-bin/people/getPhoto?id=' + s['id'] + '&show=" width=' + str(width) + '><br>\n')
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

# end html file
f.write('</body></html>\n')

# close file
f.close()


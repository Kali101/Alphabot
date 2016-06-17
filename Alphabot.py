import sys
import os
import random
from PIL import Image

maxWidth = 800
inputStr = "HELLO WORLD!"

def getRandomLetter(dirname, c):
    files = [i for i in os.listdir('./'+dirname) if i.startswith(c+'_')]
    return './'+dirname+'/'+random.choice(files)

filenames = []
skipNext = False
spaces = []
for i in range(len(inputStr)):
    c = inputStr[i]
    if skipNext:
        skipNext = False
    elif c.isspace():
        filenames.append('other/space.png')
        spaces.append(i)
    elif c.isalpha():
        dirname = 'upper' if c.isupper() else 'lower'
        filenames.append(getRandomLetter(dirname, c))
    elif c.isdigit():
        filenames.append(getRandomLetter('number', c))
    elif c == '<':
        if inputStr[i+1] == '3':
            skipNext = True
            filenames.append(getRandomLetter('other', 'heart'))
        else:
            filenames.append(getRandomLetter('other', 'lessthan'))
    elif c == '>':
        filenames.append(getRandomLetter('other', 'greaterthan'))
    elif c == ',':
        filenames.append(getRandomLetter('other', 'comma'))
    elif c == '*':
        filenames.append(getRandomLetter('other', 'asterisk'))
    elif c == '\'':
        filenames.append(getRandomLetter('other', 'apostrophe'))
    elif c == '_':
        filenames.append(getRandomLetter('other', 'underscore'))
    elif c == '-':
        filenames.append(getRandomLetter('other', 'dash'))
    elif c == '^':
        filenames.append(getRandomLetter('other', 'caret'))
    elif c == '!':
        filenames.append(getRandomLetter('other', 'exclamation'))
    elif c == '?':
        filenames.append(getRandomLetter('other', 'question'))
    elif c == '#':
        filenames.append(getRandomLetter('other', 'hashtag'))
    elif c == '@':
        filenames.append(getRandomLetter('other', 'at'))
    
images = map(Image.open, filenames)
widths, heights = zip(*(i.size for i in images))

newlines = []
total_width = sum(widths)
rowHeight = max(heights)
numRows = 1
if total_width > maxWidth and spaces:
    rowWidth = 0
    for i in range(len(images)):
        rowWidth += images[i].size[0]
        if rowWidth > maxWidth:
            spacesBefore = filter(lambda s:s < i, spaces)
            if spacesBefore:
                latestSpace = spacesBefore[-1]
                spaces.remove(latestSpace)
                newlines.append(latestSpace)
                i = latestSpace + 1
                numRows += 1
                rowWidth = 0
max_height = rowHeight * numRows

max_row_width = 0
row_width = 0
for i in range(len(images)):
    if i in newlines:
        max_row_width = max(row_width, max_row_width)
        row_width = 0
    else:
        row_width += images[i].size[0]
max_row_width = max(row_width, max_row_width)

print newlines
print max_row_width

new_im = Image.new(mode='RGB',
                   size=(max_row_width, max_height),
                   color=(255,255,255,0))

x_offset = 0
y_offset = 0
for i in range(len(images)):
    if i in newlines:
        x_offset = 0
        y_offset += rowHeight
    else:
      new_im.paste(images[i], (x_offset,y_offset))
      x_offset += images[i].size[0]

new_im.save('test.jpg')

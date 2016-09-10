#!/usr/bin/python
"""
put script in a directory run it, get playlist
then run with mpv --playlist
"""
import os

#set options
relativePaths = True
#where to scan
dir = os.getcwd()
#what extensions to find
ext = [".asf", ".avi", ".flv", ".m4v", ".mov", ".mp4", ".mpg", ".webm", ".wmv"]


#define empty list
result = []
#define output
if os.name == 'nt':
	output = "allW.m3u"
else:
	output = 'all.m3u'

#find it python
for root, dirs, files in os.walk(dir):
	for file in files:
		if file.endswith(tuple(ext)):
            #before adding it to list try printing the whole path to check Errors
			try:
				if relativePaths:
					print("Found file {}".format(os.path.join(root, file).replace(dir, '.')))
				else:
					print("Found file at {}".format(os.path.join(root, file)))
			except UnicodeEncodeError as e:
				print(e)
				input()
				exit(1)
			if relativePaths:
				result.append(os.path.join(root, file).replace(dir, '.'))
			else:
				result.append(os.path.join(root, file))

print("\nFound {0} files".format(len(result)))
#write everything in ALPHABETIC order
print("\nWriting playlist to {0}".format(dir + '/' + output))
write_playlist = open(dir + "/" + output, "w")
for item in result:
	write_playlist.write(item+'\n')
write_playlist.close()
print ("Writing sucessfull")

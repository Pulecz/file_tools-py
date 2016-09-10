#!/usr/bin/python
"""
put script in a directory run it, get playlist
then run with mpv --playlist
#V0.1 	- long time ago, basic for root, dirs, files in os.walk(dir):
#		- extensions filtered, relativePaths support
#		- UnicodeEncodeError on Python 3 sort of resolved
#V.02 	- filter directories added - TODO proper testing
#		- printing in loop is now in print_got_file function
"""
import os

#set options
debug = False
relativePaths = True
filterDirectories = True
#where to scan
dir = os.getcwd()
#what extensions to find
ext = [".asf", ".avi", ".flv", ".m4v", ".mov", ".mp4", ".mpg", ".webm", ".wmv"]
#what names in full path(os.path.join(root,file)) to filter
filter_dir = [
'Black Sails',
'Rick and Morty',
'Twin Peaks'
]

#define empty lists
result = []
result_debug = []
#define output
if os.name == 'nt':
	output = "allW.m3u"
else:
	output = 'all.m3u'

def print_got_file(root, dir, file, relativePaths, found):
	if relativePaths:
		if found:
			print("Found file {0}".format(os.path.join(root, file).replace(dir, '.')))
		else:
			print("Skipping file {0}".format(os.path.join(root, file).replace(dir, '.')))
	else:
		if found:
			print("Found file at {0}".format(os.path.join(root, file)))
		else:
			print("Skipping file {0}".format(os.path.join(root, file)))


#find it python
for root, dirs, files in os.walk(dir):
	for file in files:
		if filterDirectories and any(fdir in os.path.join(root,file) for fdir in filter_dir):
			print_got_file(root,dir,file, relativePaths, found = False)
			if debug:
				result_debug.append(os.path.join(root, file)) #check with ipython -i
			break;
		else:
			if file.endswith(tuple(ext)):
				#before adding it to list try printing the whole path to check Errors
				try:
					print_got_file(root,dir,file, relativePaths, found = True)
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

#!/usr/bin/env python
"""
Get uniq urls from your Pocket (Read it Later) export
V0.1 - basic idea and printing uniq and non_uniq links
TODO:
    Clean input file from header, html, body and ul tags, maybe edit re_http_link
    Add which line is the non_uniq link on
    Make a menu what to do with the link
    export uniq and non_uniq to json
        delete from input file and ril database? (ril api)
"""
from re import compile as re_compile
from re import match as re_match

verbose = False
print_only_uniq = True
random_uniq_link_print = False


def get_occurences(uniq_values, data):
    occurences = {}
    for index, uniq in enumerate(uniq_values):
        #for each item, get lines where the uniq item is
        #stolen from http://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
        occurences[index] = [line for line, item in enumerate(data) if item == uniq]
    return occurences

#define RIL html file and compile regex for base url
#get yours pocket export (ril_file) at https://getpocket.com/export
ril_file = '/home/pulec/ril_export_www.html'
re_http_link = re_compile(".*(http://[\w.-]+)")

#load RIL file and put all in ril_data list
with open(ril_file, 'r') as ril_file_h:
    ril_data = ril_file_h.read().split('\n')

#now define list to have only base url
ril_data_base_urls_only = []
for item in ril_data:
    match = re_match(re_http_link, item)
    if match is not None:
        ril_data_base_urls_only.append(match.group(1))

#get uniq base_urls
uniq_base_urls = list(set(ril_data_base_urls_only))

#get occurences
occurences = get_occurences(uniq_base_urls, ril_data_base_urls_only)

#sort out uniq items and nonuniq items
uniq = {}
non_uniq = {}

for occurence in occurences.values():
    #if there is just one occurence, its uniq
    if len(occurence) == 1:
        if verbose:
            print('Item on line', occurence[0] + 1,'the', ril_data_base_urls_only[occurence[0]], 'is uniq.')
        uniq[occurence[0]+1] = ril_data[occurence[0]]
    #else its non_uniq
    else:
        if verbose:
            print('There are', len(occurence),'items for', ril_data_base_urls_only[occurence[0]])
        for index, not_uniq in enumerate(occurence):
            #each non_uniq link needs special key, hence index
            if index < 10:
                nice_index = '00' + str(index)
            elif index < 100:
                nice_index = '0' + str(index)
            non_uniq[ril_data_base_urls_only[occurence[0]] + '_' + nice_index] = ril_data[not_uniq]

if print_only_uniq:
    if random_uniq_link_print:
        from random import choice
        random_uniq_link_key = choice(list(uniq.keys()))
        print('On line', random_uniq_link_key,'item:',uniq[random_uniq_link_key])
    else:
        for index, link in enumerate(sorted(list(uniq.keys()))):
            print('On line', link,'item:',ril_data[link])
            input('Got it? {0} remaining.'.format(len(list(uniq.keys()))-index))
else:
    for key in sorted(list(non_uniq.keys())):
        print(key,':',non_uniq[key])
        input('Got it?')

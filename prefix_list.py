import re

def convert_prefix_set(lines):
    len_prefix = len(lines)
    name = lines[0].split(' ')[2]
    print "prefix-set {}".format(name)
    i = 0
    for line in lines:
        i = i+1
        line = line.strip('\n')
        is_description = re.match('.*description.*',line)
        is_deny = re.match('.*deny.*',line)
        if is_deny:
            print "check the list"
        if is_description:
            print ("# {}".format(' '.join((line.split(' ')[4:]))))
            continue
        if i == len_prefix:
            print (" {}".format(' '.join((line.split(' ')[6:]))))
        else:
            print (" {},".format(' '.join((line.split(' ')[6:]))))
    print "end-set"
    
def split_lines(file_lines):
    temp_lines = []
    #print file_lines
    for each_line in file_lines:
        is_end = re.match('^!',each_line)
        if is_end:
            convert_prefix_set(temp_lines)
            #print temp_lines
            temp_lines = []
        else:
            temp_lines.append(each_line)
        
file_hd_temp = open('prefix-list.txt')
file_lines = file_hd_temp.readlines()

split_lines(file_lines)

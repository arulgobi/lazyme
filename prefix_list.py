import re
prefix  = """ip prefix-list 4300400971-Prefix seq 5 permit 103.31.24.0/23
ip prefix-list 4300400971-Prefix seq 10 permit 103.31.24.0/24
ip prefix-list 4300400971-Prefix seq 15 permit 103.31.25.0/24"""


lines = prefix.split('\n')
#of lines 
len_prefix = len(lines)
#print len_prefix
name = lines[0].split(' ')[2]
print "prefix-set {}".format(name)
i = 0
for line in lines:
    i = i+1
    is_description = re.match('.*description.*',line)
    if is_description:
        print ("# {}".format(''.join((line.split(' ')[4:]))))
        continue
    if i == len_prefix:
        print (" {}".format(' '.join((line.split(' ')[6:]))))
    else:
        print (" {},".format(' '.join((line.split(' ')[6:]))))
print "end-set"

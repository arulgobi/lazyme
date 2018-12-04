import re
from collections import defaultdict

def check_bundle_number(config_interface):
#need to check this funcation 
    interface_name = ""
    bundle_id = ""
    for config in config_interface:
        is_bundle = re.match(".*bundle id.*",config)
        is_interface = re.match('^interface TenGigE',config)
        if is_interface:
            interface_name = config.split(' ')[1].strip('\n')
            #print interface_name
        if is_bundle:
            bundle_id = config.split(' ')[1]
            #print(bundle_id)
    if bundle_id:
        #print "",interface_name,"",bundle_id
        return(interface_name,bundle_id)

def print_be_per_bd(config_bg):
  #need to check this funcation 
    bundle_id = []
    for config_line in config_bg:
        is_bundle = re.match(".*interface Bundle-Ether.*",config_line)
        if is_bundle:
            #print config_line
            bundle_id.append(config_line.split(' ')[-1].split('.')[0])
    bundle_set = set(bundle_id)
    print bundle_set
        
        
def config_split(start_string,end_string,temp_file_hd):
    #function to split based on start and end strings 
    #print start_string
    splited_config = []
    splited_config_main = []
    is_match_start = False 
    is_end_marker = False
    for line in temp_file_hd:
        is_match_string = re.match(start_string,line)
        is_match_end = re.match(end_string,line)
        if is_match_string:
            is_match_start = True
        if is_match_start and is_match_end:
            is_end_marker = True
        if is_match_start and not is_end_marker:
            splited_config.append(line)
        if is_match_start and is_end_marker:
            is_match_start = False
            is_end_marker = False
            splited_config = []
            splited_config_main.append(splited_config)
    return  splited_config_main

bundle = defaultdict(list)
fd_hd = open('running_config.txt','r')
file_lines = fd_hd.readlines()
for config_set in config_split('^interface TenGigE','^!',file_lines):
    bundle_set = check_bundle_number(config_set)
    print(bundle_set)
    #if bundle_set:
    #    bundle[bundle_set[1]].append(bundle_set[0])

for k in bundle:
    print k,bundle[k]

for config_bg_set in config_split('^ bridge group',' !',file_lines):
    print_be_per_bd(config_bg_set)

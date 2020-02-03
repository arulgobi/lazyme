#3rd Feb 2020 , to identify the ACL from interfaces & convert it to XR 
#convering XR  = only the relevant object groups (network / port) are in the ACL & replace the names
#need to update for IPv6. 
import re
from collections import defaultdict
import glob

def check_acl_name (int_temp_config):
    #from interface config set identify the acl name
    acl_temp_list = []
    #print(int_temp_config[0])
    for line in int_temp_config:
        is_acl = re.match('.*access-group.*',line)
        if is_acl:
            acl_temp_list.append(line.split()[2])
   #print(acl_temp_list)
    return(acl_temp_list)
        
def retrive_net_group (acl_config_temp):
    net_group_list = []
    for line in acl_config_temp[0]:
        is_net_grp = re.match('.*addrgroup.*',line)
        if is_net_grp:
            net_group_list.append(line.split('addrgroup')[1].split()[0])
    return net_group_list

def retrive_port_group (acl_config_temp):
    port_group_list = []
    for line in acl_config_temp[0]:
        is_port_grp = re.match('.*portgroup.*',line)
        if is_port_grp:
            port_group_list.append(line.split('portgroup')[1].split()[0])
    return port_group_list

        
def config_split(start_string,end_string,temp_file_hd):
    #function to split based on start and end strings 
    #print (start_string)
    #start_string_tmp = re.escape(start_string)
    start_string_tmp = start_string
    #print(start_string_tmp)
    splited_config = []
    splited_config_main = []
    is_match_start = False 
    is_end_marker = False
    count = 0
    for line in temp_file_hd:
        #print (line)
        is_match_string = re.match(start_string_tmp,line)
        is_match_end = re.match(end_string,line)
        if is_match_string:
            is_match_start = True
            #print ("start string set")
            count = 1
        if is_match_start and is_match_end and count > 1:
            is_end_marker = True
            #print "start and end string matched"
        if is_match_start and not is_end_marker:
            splited_config.append(line)
            count = count +1
        if is_match_start and is_end_marker:
            is_match_start = False
            is_end_marker = False
            splited_config_main.append(splited_config)
            splited_config = []
    return  splited_config_main

for filename in glob.glob('*.txt'):
    file_hd = open(filename,'r')
    file_lines = file_hd.readlines()
    interface_config = config_split('interface','^$',file_lines)  #split the interfaces ( end string is empty char)
    acl_list = []
    for int_config in interface_config:
        if check_acl_name(int_config):  
            acl_list = acl_list + check_acl_name(int_config)
    #print set(acl_list)
    for acl in set(acl_list):
        #print(acl)
        acl_name = "ip access-list "+acl 
        acl_config = config_split(acl_name,'[a-z|A-Z]',file_lines)
        #network object group list i need to parse and change it to ASR9K
        net_list = retrive_net_group(acl_config)
        for net_obj in set(net_list):
            net_grp_name = "object-group ip address "+net_obj
            net_grp_config = config_split(net_grp_name,'[a-z|A-Z]',file_lines)
            net_grp_config[0][0] = net_grp_config[0][0].replace('ip address','network ipv4')
            #print(net_grp_config)
            for line in net_grp_config[0] :
                is_header = re.match('.*object.*',line)
                if not is_header:
                    print(' '.join(line.strip('\n').split()[1:]))
                else:
                    print(line.strip('\n'))
    
            
        #port object group list i need to parse and change it to ASR9K
        port_grp_list = retrive_port_group(acl_config)
        #print(port_grp_list )
        for port_obj in set(port_grp_list):
            #finding port group and change it to XR format.
            prt_grp_name = "object-group ip port "+port_obj
            prt_grp_config =config_split(prt_grp_name,'[a-z|A-Z]',file_lines) 
            prt_grp_config[0][0] = prt_grp_config[0][0].replace('object-group ip port','object-group port')
            for line in prt_grp_config[0] :
                is_port = re.match('.*eq.*',line)
                if is_port:
                    print(' '.join(line.strip('\n').split()[-2:]))
                else:
                    print(line.strip('\n'))
        #go through ACL 
        for line in acl_config[0]:
            line = line.replace('addrgroup','net-group')
            line = line.replace('portgroup','port-group')
            print(line.strip('\n'))
    print(acl_list)
    

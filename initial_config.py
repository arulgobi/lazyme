# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 16:23:43 2018

@author: aemmanue

RCG,CO2,SIX,N71,N72,CO3,Blackhole,IP
Gi0/0/0/1,Gi0/0/0/1,,,,,,192.168.1.0


"""
from collections import defaultdict

def find_position(list_of_connections):
    j=0
    position = []
    for i in list_of_connections:
        if i:
            position.append(j)
        j = j+1
    return position

def print_interface(list_of_lines):
    header_list = ['']
    line_count = 0
    for line in list_of_lines:
        if line_count ==0:
            line_count = line_count +1
            header_list = line.split(',')  # usually ","
        else:
            line = line.strip('\n')
            list_of_edges = line.split(',')  # usually ","
            #print (list_of_edges)
            i= 0
            counter=0
            connection_matrix = find_position(list_of_edges[0:-2])
            for each_item in list_of_edges[0:-2]:
                if each_item and i <3:
                    print(header_list[counter])
                    #print (each_item,list_of_edges[-1])
                    i = i+1
                    ip_address = list_of_edges[-2].split('.')
                    ip_address[-1] = int(ip_address[-2])+i
                    new_ip_address = '.'.join(str(e) for e in ip_address)
                    #print(new_ip_address)
                    print(" interface {}".format(each_item))
                    if i == 1:
                        print(" description {} to {}".format(header_list[connection_matrix[0]],header_list[connection_matrix[1]]))
                    else:
                        print(" description {} to {}".format(header_list[connection_matrix[1]].split('-')[0],header_list[connection_matrix[0]].split('-')[0]))
                    if header_list[counter].split('-')[1] == "XR":
                        print(" ipv4 address {}/30".format(new_ip_address))
                    if header_list[counter].split('-')[1] == "IOS":   
                        print(" ip address {} 255.255.255.252".format(new_ip_address))
                    print(" no shutdown")
                    
                counter = counter+1               
                
def print_isis(list_of_lines):
  header_list = ['']
  interface_isis_dic = dict()

  line_count = 0
  for line in list_of_lines:
      if line_count ==0:
          line_count = line_count +1
          header_list = line.split(',')  # usually ","
      else:
         line = line.strip('\n')
         list_of_edges = line.split(',')  # usually ","
            #print (list_of_edges)
         i= 0
         counter=0
         for each_item in list_of_edges[0:-2]:
             if each_item and i <3:
                 #print(header_list[counter])
                 i = i+1
                 if list_of_edges[-1] == "ISIS": #check the protoco if its ISIS activate , can change it to OSPF as well
                     if header_list[counter] not in interface_isis_dic:
                         interface_isis_dic[header_list[counter]] = []
                         interface_isis_dic[header_list[counter]].append(each_item)
                          # append some value 
                     else:
                         interface_isis_dic[header_list[counter]].append(each_item)
             counter = counter+1
  #print(interface_dic)
  j = 0
  for key in interface_isis_dic:
       j = j+1
       if key.split('-')[1] == "XR":
           print(key)
           print("========")
           print("router isis SCV")
           print("is-type level-2-only")
           print("net 49.0000.1720.2000.200{}.00".format(j))
           print("nsf ietf")
           print("log adjacency changes")
           print("address-family ipv4 unicast")
           print(" metric-style wide")
           print("maximum-paths 16")
           print("!")
           print("address-family ipv6 unicast")
           print("metric-style wide")
           for interface in interface_isis_dic[key]:
               print("interface {}".format(interface))
               print("point-to-point")
               print("address-family ipv4 unicast")
               print("mpls ldp sync")
               print("address-family ipv6 unicast")
           print("!")
       if key.split('-')[1] == "IOS":
           print(key)
           print("========")
           print("router isis SCV")
           print("net 49.0000.1720.2000.200{}.00".format(j))
           print("log adjacency changes")
           print(" metric-style wide")
           print("!")
           print("address-family ipv6")
           print("multi-topology")
           print("exit-address-family")
           for interface in interface_isis_dic[key]:
               print("interface {}".format(interface))
               print("ip router isis SCV")
               print("ipv6 router isis SCV")
               print("isis network point-to-point")

           print("!")
#file_hd = open('Book2.csv')
f = open('Book2.csv','r')
lines = f.readlines()
f.close()

print_interface(lines)
print("*************************")
print("*************************")
print_isis(lines)



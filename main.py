from datetime import datetime
import nmap
import scapy.all as scapy

print('Please do not use this toolkit in a way which harasses the 1990 Computer Misuse Act.\nThis toolkit only has over-simple/basic tools and there are also lots of bugs, as this is the developer\'s first time writing full code, sorry.') 
userscmd = str(input('chaos>>> '))

def error_msg():
    print('It seems their is an error. Please do not contact the developer, she is anti-social(or contact killmyself174236981651321000678123456789000678@tor2box.com (checked every few years)).')
    exit()

class cmd():

    def __init__(self):
        self.cmd = userscmd.split()

    def process_cmd(self):
        while self.cmd[0] != 'exit':
            if self.cmd[0] == 'scan':
                if self.cmd[1] in ['UDP','udp' ]:
                    if self.cmd[2] in ['ports', 'ports:']:
                        scan_udp(self.cmd[3])
                        cmd_done() 
                elif self.cmd[1] in ['TCP', 'tcp']:
                    if self.cmd[2] in ['ports', 'ports:']:
                        scan_tcp(self.cmd[3])
                        cmd_done() 
                elif self.cmd[1] == 'both':
                    if self.cmd[2] in ['ports', 'ports:']:
                        scan_tcp(self.cmd[3])
                        scan_udp(self.cmd[3])
                        cmd_done()
            elif self.cmd[0] == 'ping-sweep':
                psw(self.cmd[1])
            elif self.cmd[0] in ['help','cmds','commands']:
                help()
            elif self.cmd[0] == 'packet-sniff':
                sniff(self.cmd[1])
            else:
                print('Please enter a valid command.')
            self.cmd = (str(input('chaos>>> '))).split()
        exit()
    
    def psw(self, SUBNET):
        nm = nmap.PortScanner()
        print(f'Please wait. Pinging devices on subnet {SUBNET}.')
        output = []
        try:
            result = nm.scan(hosts=SUBNET, arguments='-sn')
            for host in nm.all_hosts():
                State = nm[host].state()
                if State == 'up':
                    output.append(f'The device with the IPv4 address {host} is on and connected to the internet.')
            for i in range(len(output)): print(output[i])
        except BaseException as Exception:
             print(f'Error:{Exception.args}')

    def scan_tcp(self, address): 
        print(f'Please wait. The program has recieved the address: {address}, and is now working on scanning it to find the open TCP ports.\nThis will take ~30 seconds.')
        nm = nmap.PortScanner()
        result = nm.scan(address, arguments='-sV -Pn --disable-arp-ping')
        output = []
        scannedbynmap = nm[address]['tcp'].keys()
        for port in scannedbynmap:
            if (nm[address]['tcp'][port]['state']) == 'open': 
                output.append(f'Port {port} is open with TCP running, using {nm[address]['tcp'][port]['version']}')
        if (len(scannedbynmap)) == 0: 
            print('The device you are trying to scan seems unreachable.')
        for i in range(len(output)): 
            print(output[i])

    def scan_udp(self, address): 
        print(f'Please wait. The program has recieved the address: {address}, and is now working on scanning it to find the open UDP ports.\nThis will take ~90+ seconds.')
        nm = nmap.PortScanner()
        nm.scan(address, arguments='-sU --top-ports 50 -Pn --disable-arp-ping')
        output = []
        if address not in nm.all_hosts():
            print('The device you are trying to reach is unreachable.')
            return 0
        elif 'udp' not in nm[address].keys(): 
            print('It seems that there is no UDP ports open. UDP is sketchy I don\'t like it.')
            return 0
        elif nm[address]['udp'] == {}: 
            print('It seems that you have UDP ports, but nmap didnt get any response from them. How unreliable of UDP.')
            return 0
        scannedbynmap = nm[address]['udp'].keys()
        for port in scannedbynmap:
            check_state = nm[address]['udp'][port]['state']
            if check_state == 'open': 
                output.append(f'Port {port} is {check_state} with UDP.')
        if not(output):
            print('Scan finished, no UDP ports detected.')
        else:
            for i in range(len(output)): print(output[i])

    def help(self):
        file = open('documentation.md','r')
        content = file.read()
        print(' There are currently three main tools from this toolkit.\n1: Port scanner\n2: Ping sweeper\n3: Packet sniffer\nHere is the documentation of this toolkit.\n', content) 


    def sniff(self, pc):
        pkts = scapy.sniff(count = pc)
        counter = 0
        for packet in pkts:
            ask = str(input('The algorithm has captured a packet, would you like to know more information? [y/n]'))
            if ask.lower() in ['y','yes']:
                try: 
                    print(f"Source IP: {packet['IP'].src}\nDestination MAC: {packet['Ether'].dst}")
                except: 
                    f.error_msg()
            counter += 1

    def cmd_done(self):
        print(f'This command has been sucsessfully been completed at {datetime.now()}')

try: 
    uhhh = cmd()
    uhhh.process_cmd()
except BaseException as e: 
    print(f'Toolkit closed down. Reason:{e.args}')
    

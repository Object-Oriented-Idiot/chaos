from datetime import datetime
import nmap
import scapy.all as scapy
from functools import wraps

def uhh(func):
    @wraps(func)
    def inner(self):
        print('Process started.')
         result = func(self)
        print('Process ended.')
        return result
    return inner

    
class exceptions(type):
    list_of_custom_exceptions = []
    def __new__(cls, name, bases, namespace):
        namespace['__str__'] = lambda self: f'Error: {self.errormsg}'
        return super().__new__(cls, name, bases, namespace) 

class CustomError(Exception, metaclass=exceptions):
    def __init__(self):
        self.errorname = type(self).__name__
        try: self.errormsg = re.findall('[A-Z][^A-Z]*', self.errorname.removesuffix('Error'))
        except: error_msg()
        self.errormsg = (' '.join(self.errormsg)).lower()
        super().__init__(self.errormsg)

    class PortScanningError(CustomError): pass

print('Please do not use this toolkit in a way which harasses the 1990 Computer Misuse Act.\nThis toolkit only has over-simple/basic tools and there are also lots of bugs, as this is the developer\'s first time writing full code, sorry.') 
userscmd = str(input('chaos>>> '))

def error_msg():
    print('It seems their is an error. Please do not contact the developer, she is anti-social.')
    exit()

class cmd():

    def __init__(self):
        self.cmd = userscmd.split()

    def process_cmd(self):
        while self.cmd:
            while self.cmd[0] != 'exit':
                if self.cmd[0] == 'scan':
                    if self.cmd[1].lower == 'udp':
                        if self.cmd[2] in ['ports', 'ports:']:
                            scan_udp(self.cmd[3])
                            cmd_done() 
                    elif self.cmd[1].lower() == 'tcp':
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

    @uhh
    def psw(self, subnet):
        nm = nmap.PortScanner()
        print(f'Please wait. Pinging devices on subnet {subnet}.')
        try:
            result = nm.scan(hosts=subnet, arguments='-sn')
            for host in nm.all_hosts():
                State = nm[host].state()
                if State == 'up':
                    print(f'The device with the IPv4 address {host} is on and connected to the internet.')
        except Exception as Error:
            raise PortScanningError from Error

    @uhh
    def scan_tcp(self, address): 
        print(f'Please wait. The program has recieved the address: {address}, and is now working on scanning it to find the open TCP ports.\nThis will take ~30 seconds.')
        nm = nmap.PortScanner()
        result = nm.scan(address, arguments='-sV -Pn --disable-arp-ping')
        scannedbynmap = nm[address]['tcp'].keys()
        for port in scannedbynmap:
            if (nm[address]['tcp'][port]['state']) == 'open': 
                print(f'Port {port} is open with TCP running, using {nm[address]['tcp'][port]['version']}')
        if (len(scannedbynmap)) == 0: 
            print('The device you are trying to scan seems unreachable.')

    @uhh
    def scan_udp(self, address): 
        print(f'Please wait. The program has recieved the address: {address}, and is now working on scanning it to find the open UDP ports.\nThis will take ~90+ seconds.')
        nm = nmap.PortScanner()
        nm.scan(address, arguments='-sU --top-ports 50 -Pn --disable-arp-ping')
        if address not in nm.all_hosts():
            print('The device you are trying to reach is unreachable.')
            return 0
        elif 'udp' not in nm[address].keys(): 
            print('It seems that there is no UDP ports open. UDP is sketchy I don\'t like it.')
            return 0
        elif nm[address]['udp'] == []: 
            print('It seems that you have UDP ports, but nmap didnt get any response from them. How unreliable of UDP.')
            return 0
        scannedbynmap = nm[address]['udp'].keys()
        for port in scannedbynmap:
            check_state = nm[address]['udp'][port]['state']
            if check_state == 'open': 
                print(f'Port {port} is {check_state} with UDP.')
        if not(output):
            print('Scan finished, no UDP ports detected.')

    def help(self):
        file = open('documentation.md','r')
        content = file.read()
        print('There are currently three main tools from this toolkit.\n1: Port scanner\n2: Ping sweeper\n3: Packet sniffer\nHere is the documentation of this toolkit.\n', content) 

    @uhh
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

uhhh = cmd()
uhhh.process_cmd()

import re
import scrypt
import tempfile
from pathlib import Path
from copy import deepcopy 
from getpass import getpass
from functools import wraps

SUPPORTED_FILE_ENDING_TYPES = ( '.txt', '.csv', '.json',
                                '.xml', '.docx', '.rtf', 
                                '.md', '.png', '.zip', 
                                '.pdf') 

class exceptions(type): 
    def __new__(cls, name, bases, namespace):
        namespace['__str__'] = lambda self: f'Error: {self.errormsg}'
        return super().__new__(cls, name, bases, namespace) 

class CustomError(Exception, metaclass=exceptions):
    def __init__(self):
        self.errorname = type(self).__name__
        try: self.errormsg = re.findall('[A-Z][^A-Z]*', self.errorname.removesuffix('Error'))
        except as Error: print('An error has occured:', Error.args)
        self.errormsg = (' '.join(self.errormsg)).lower()
        super().__init__(self.errormsg)

class FileTypeUnsupportedError(CustomError): pass
class FileEmptyError(CustomError): pass
class InputUnrecognisedError(CustomError): pass
class ProcessingError(CustomError): pass
class FileWritingError(CustomError): pass
class FileIsAlreadyEncryptedError(CustomError): pass
class FileIsNotEncryptedError(CustomError): pass

def format_(function):
    """This decorator(function) notifies the user when the process of en/decryption starts and finished. I am too lazy to write more docstrings.
    """
    @wraps(function)
    def inner(self):
        try: 
        except: 
            print(f'{function.__name__.capitalize()}ion process ended- thank you for waiting.')
        try:
            result = function(self)
        except Exception as Error:
            raise ProcessingError from Error
        finally:
            print(f'{function.__name__.capitalize()}ion process ended- thank you for waiting.')
        return result
    return inner


class FileConverter(): 
    def __init__(self, filename):
        self.filename = filename 
        self.path = Path(self.filename).resolve()
        if self.path.stem.endswith('.encrypted'): 
            self.encrypted = True
        else: 
            self.encrypted = False
        if self.path.suffix not in SUPPORTED_FILE_ENDING_TYPES: 
            raise FileTypeUnsupportedError
        if not self.path.is_file(): 
            raise FileNotFoundError
        self.password = getpass('Please enter a password you can use to acsess your file.')
        while not self.password: 
            self.password = getpass('Please enter a password you can use to acsess your file which is not empty.')


    def rename(self): 
        try:
            if self.encrypted: 
                self.new_filename = self.path.stem + '.encrypted' + self.path.suffix
            else: 
                self.new_filename = self.path.stem.removesuffix('.encrypted') + self.path.suffix
            try:
                self.new_path = self.path.with_name(self.new_filename)
                if self.new_path.exists():
                    nOT_A_CONSTANT = -1
                    while self.new_path.exists():
                        nOT_A_CONSTANT += 1
                        self.new_filename = self.path.stem + str(nOT_A_CONSTANT) + '.encrypted' + self.path.suffix
                        self.new_path = self.path.with_name(self.new_filename)
                self.path.rename(self.new_path) 
            self.path , self.filename = self.new_path, self.new_filename
          
        except OSError: 
            Input = str(input('Error:Rename failed.\n Would you like to try again?(Y/N)'))
            if Input.lower() in ['y', ' yes']:
                  self.rename()
            elif Input.lower() in [ 'n', 'no']:
                  return
            else:
                raise InputUnrecognisedError
        

    @format_
    def decrypt(self):
        if  not self.path.stem.endswith('.encrypted'):
            raise FileIsNotEncryptedError
        with self.path.open('rb') as file:
            contents = file.read()
        self.second_copy = deepcopy(contents)
        if len(contents):
            try:
                contents = scrypt.decrypt(contents, self.password) 
                with tempfile.TemporaryFile(mode='w+b') as file:
                    file.write(contents)
                    file.seek(0)
                    content_check = file.read()
                if content_check != contents:
                         raise FileWritingError
                with self.path.open('wb') as file: 
                    file.write(contents)
                self.encrypted = False
            except (scrypt.error, FileWritingError) as Error:
                print(f'Error: {Error.args}, attempting to restore original content\'s')
                with self.path.open('wb') as file: 
                    file.write(self.second_copy)
                return
        else:
            raise FileEmptyError
        self.rename()

    @format_
    def encrypt(self):
        if self.path.stem.endswith('.encrypted'): 
            raise FileIsAlreadyEncryptedError 
        try:
            with self.path.open('rb') as file:
                contents = file.read() 
            self.second_copy = deepcopy(contents)
        except PermissionError:
            print('Error: The file does not seem to be compatible with reading.')
            return 
        try:
            contents = scrypt.encrypt(contents, self.password) 
        except scrypt.error as e:
            print(f'Error: {e.args}')
            return 
        try:
            with tempfile.TemporaryFile(mode='w+b') as file:
                file.write(contents)
                file.seek(0)
                content_check = file.read()
            if content_check != contents: 
                raise FileWritingError
            with self.path.open('wb') as file:
                file.write(contents)
            self.encrypted = True
          
        except (OSError, FileWritingError) as Error:
            print(f"Error: {Error.args}, attempting to restore file's original contents")
            try:
                with self.path.open('wb') as file: 
                    file.write(self.second_copy)
            except (OSError, FileWritingError): 
                print('Attempt failed, proceeding with process. File may turn corrupted.')
            return
        self.rename()o



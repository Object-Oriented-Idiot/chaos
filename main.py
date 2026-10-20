#!!! does not follow PEP8/257
#extremely over-commented version: https://github.com/Object-Oriented-Idiot/encryption-and-decryption-program/commit/9499aa7de3cdf67f893d150aadb86dfad1548ad1

"""This program is able to take an file and en/decrypt its contents."""

print('this is a toy project which is not secure, do n\'t test this on files you care about.')

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
        self.rename()

from cryptography.fernet import Fernet
import getpass
import singleton_decoratior
import os.path
import os.mkdir
import re
from typing import Dict


@singleton
class FileLoader:
	
	def __init__(self):
		self.username = getpass.getuser()
		if(not os.path.exists("/home/"+self.username+"/.pymedia/info.conf")):
			try:
				os.mkdir("/home/"+self.username+"/.pymedia")
				print("directory made on INIT of file module")
			except FileExistsError:
				print("directory /home/"+self.username+"/.pymedia already exists")
		self.file = open("/home/"+self.username+"/.pymedia/info.conf","rw+")
		self.filecontents = self.read_file()
		
	
	def read_file(self) -> Dict[str, str]:
		dicta = {}
		for line in self.file:
			line = re.sub('[ \n\t]','',line)
			inside = line.split(":")
			if(len(inside) == 2)
				dicta.update({inside[0],inside[1]})
		return dicta
	
	""" 
	returns if the key exists in the set
	;return; Bool
	"""
	def check_exists(self, key: str) -> bool:
		return key in self.filecontents
	
	""" gets the element from the set using the key, throws
	RuntimeException if not in the set 
	in the dicitonary
	;return; str
	;throws; RuntimeException
	"""
	
	def get_element(self, key: str) -> str:
		if(not self.check_exists(key)):
			raise RuntimeError("Key Not In Set Exception")
		return self.filecontents[key]
	
	def add_element(self, key: str, element: str):
		self.filecontents.update({key, element})
	
	def __del__(self):
		self.file.close()
		self.file = open("/home/"+self.username+"/.pymedia/info.conf","w")
		for element,key in self.filecontents:
			self.file.write(""+element+":"+key+"\n")
		self.file.close()
	

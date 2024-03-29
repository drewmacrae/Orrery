
import random
import string
import time
import sys

class OnlineMarkov:
    def __init__(self):
        self.starts = []
        self.dictionary = {}
        self.maxLength = 0
        self.contributions = 1
        self.averageContributionLength = 0

    def print(self):
    	print(self.dictionary)

    def erase(self):
    	self.starts = []
    	self.dictionary = {}
    	self.maxLength = 0
    	self.contributions = 1
    	self.averageContributionLength = 0

    """This solution from WISSAM JARJOUI at Shippo to find the size of a dictionary really helped"""
    def get_size(self,obj,seen=None):
        """Recursively finds size of objects"""
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        # Important mark as seen *before* entering recursion to gracefully handle
        # self-referential objects
        seen.add(obj_id)
        if isinstance(obj, dict):
            size += sum([self.get_size(v, seen) for v in obj.values()])
            size += sum([self.get_size(k, seen) for k in obj.keys()])
        elif hasattr(obj, '__dict__'):
            size += self.get_size(obj.__dict__, seen)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum([self.get_size(i, seen) for i in obj])
        return size

    def markov_get_size(self):
        return self.get_size(self.dictionary)

    def prune(self,targetSize = 25000):
      while(self.get_size(self.dictionary))>targetSize:
        randomKey = random.choice(list(self.dictionary.keys()))
        if randomKey not in self.starts:
	        self.dictionary.pop(randomKey,None)

    def contribute(self,string,keyLength=1):
      """Contribute to the markov chain's dictionary"""
      #print(">"+string)
      if(len(self.dictionary)==0):
        self.contributions = 1
        self.averageContributionLength = len(string)
      else:
        self.contributions+=1
        self.averageContributionLength = 1.0/self.contributions*len(string)+self.averageContributionLength*(self.contributions-1)/self.contributions
      
      string = ">"+string+"\0"
      while True:
        if len(string)<2:
         return
        documenting = True
        while documenting:
          if keyLength == len(string)-1:
            documenting = False
          if string[0:keyLength] not in self.dictionary:
            documenting = False
            self.dictionary[string[:keyLength]]=[string[keyLength]]
            if(string[0]=='>'):
            	self.starts+=[string[0:keyLength]]
          else:
            self.dictionary[string[:keyLength]]+=[string[keyLength]]
            keyLength += 1
          if keyLength>self.maxLength:
            self.maxLength = keyLength
        keyLength = 1
        string = (string[1:])

    def generate(self):
      
      if(len(self.dictionary))==0:
      	print("tried to generate with an empty dictionary")
      	return ""

      if(len(self.starts))==0:
      	print("tried to generate without any valid beginnings")
      	return ""

      """Generate a message without a prompt"""
      randomKey = random.choice(list(self.starts))
      output = randomKey+random.choice(self.dictionary[randomKey])
      
	  #pick a key length
      keyLength = random.choice(list(range(1,self.maxLength))+[self.maxLength]*8)
        
      while len(output)<self.averageContributionLength**2:
        key = output[-keyLength:]
        #print(key)
        if key in self.dictionary:
          output += random.choice(self.dictionary[key])
          keyLength = random.choice(list(range(1,self.maxLength))+[self.maxLength]*8)
        if keyLength <= 1 and key not in self.dictionary:
          break
        keyLength -= 1

      if output[-1]=="\0":
      	output = output[:-1]#trim \0 from end
      return output[1:]

    def prompt(self,string):
      """Prompt the markov generator to continue a message"""
      output = string
      while len(output)<self.averageContributionLength:
        #pick a key length
        keyLength = random.randint(1,self.maxLength)
        key = output[-keyLength:]
        if key in self.dictionary:
          output += random.choice(self.dictionary[key])
        if keyLength == 1 and key not in self.dictionary:
          return output
      return output
        
    def randomString(self,stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters+" ,.") for i in range(stringLength))

def main():
	#test and demo code
	onlineMarkov = OnlineMarkov()    
	onlineMarkov.contribute("..........................................................."*2)
	onlineMarkov.contribute(onlineMarkov.randomString())
	onlineMarkov.contribute(onlineMarkov.randomString())
	onlineMarkov.contribute(onlineMarkov.randomString())
	print(onlineMarkov.markov_get_size())
	onlineMarkov.prune()
	print(onlineMarkov.markov_get_size())
	print(onlineMarkov.generate())
	onlineMarkov.contribute("hello")
	print(onlineMarkov.generate())
	print(onlineMarkov.generate())
	onlineMarkov.contribute("..enemy!!")
	print(onlineMarkov.generate())
	print(onlineMarkov.generate())
	onlineMarkov.contribute("I was here August 1 2010 and number these peoples among my enemies.")
	print(onlineMarkov.generate())
	print(onlineMarkov.generate())
	print(onlineMarkov.generate())
	print(onlineMarkov.generate())

if __name__ =="__main__":
	main()

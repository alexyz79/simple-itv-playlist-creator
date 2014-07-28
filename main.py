import os
import re
from tools.BeautifulSoup import BeautifulSoup
from channels.channelProvider import channelProvider
import tools.adenUtils as utils

class Playlist():
    
    def __init__(self):
        self.quiet = False
        self.VERSION = "0.1"
        self.providersList = list()

    """
    This method load all the dynamic modules defined
    in the modules list """
    def loadProviders(self):

        #Current path
        cwd = os.path.dirname(os.path.realpath(__file__))

        #Loading modules
        for filename in os.listdir(cwd + "/channels"):
            if filename[-3:] != ".py" or filename in ["__init__.py","channelProvider"]:
                continue
            module = filename[:-3]
            self.out("#Loading channels '%s'... " % module)
            __import__("channels.%s" % module, globals={}, locals={}, fromlist=[], level=-1)

        #Adding modules to the list
        for cls in channelProvider.__subclasses__():
            self.providersList.append(cls)

        self.out("")
        
            
    def getm3uList(self):
        
        result = ""
        
        for provider in self.providersList:                
    
            pro = provider()
            channels = pro.getChannels()
            for channel in channels:
                result += pro.getChannel(channel,'m3u')

        
        return result
        
    """
    Output function wrapper """
    def out(self, str):
        if self.quiet == False:
            print str        

pl = Playlist()
pl.loadProviders()
print pl.getm3uList()


import os
import sys
import re
from BeautifulSoup import BeautifulSoup
from adenMod import adenMod
import adenUtils as utils

class aden():

    def __init__(self):

        self.quiet = False
        self.VERSION = "0.2"
        self.moduleList = list()

    """
    This method load all the dynamic modules defined
    in the modules list """
    def loadModules(self):

        #Current path
        cwd = os.path.dirname(os.path.realpath(__file__))

        #Loading modules
        for filename in os.listdir(cwd + "/modules"):
            if filename[-3:] != ".py" or filename in ["__init__.py"]:
                continue
            module = filename[:-3]
            self.out("#Loading module '%s'... " % module)
            __import__("tools.modules.%s" % module, globals={}, locals={}, fromlist=[], level=-1)

        #Adding modules to the list
        for cls in adenMod.__subclasses__():
            self.moduleList.append(cls)

        self.out("")

    """
    Starting from the provided url, this method looks from known embedded
    players, in the current page and in the sub frames/iframes.
    If a known players is found, the RTMP data will be grabbed and printed. """
    def scan(self, url, referer = ""):
        self.out("> Scanning url: %s..." % url)
        
        if referer == "":
            referer = url

        try:

            #Getting page content
            pagedata = utils.getUrlData(url, referer)

        except Exception as e:
            self.out("*** Error requesting %s: %s" % (url, e))
            return False

        #Looking for embedded player in the page
        player_found = self.grab(url, pagedata,referer)

        #If the player was not found in the current page, let's start to
        #scan internal iframes
        if not player_found:
            soup = BeautifulSoup(pagedata)
            for iframe in soup.findAll(["iframe", "frame"]):
                if iframe.has_key("src") and iframe["src"] and re.search("^http[s]*://.*", iframe["src"], re.IGNORECASE):
                    player_found = self.scan(iframe["src"], referer)
                    if player_found:
                        return player_found
            return ""

        return player_found 

    """
    Running all modules against the url
    This methon takes two arguments to reuse the data fetched with the
    last request """
    def grab (self, url, pagedata, referer = ""):
        
        player_found = ""

        for tvmod in self.moduleList:
            try:
                mod = tvmod()
                mod.initialize(quiet=self.quiet)
                if mod.probe(pagedata):
                    self.out("> %s player found!" % mod.name)
                    if mod.scan(url,referer) == True:
                        
                        if (self.out_mode == "list"):
                            player_found += mod.getRTMPdata()
                        elif (self.out_mode == "m3u"):
                            player_found += mod.getM3Uentry()
                        elif (self.out_mode == "rtmpdump"):
                            player_found += mod.getRTMPDump()
                    else:
                        self.out("*** Error grabbing player properties!\n")
                        sys.exit(1)

            except Exception as e:
                self.out("*** Error running module %s: %s\n    Maybe the channel is not longer available." % (mod.name, e))
                return ""

        return player_found

    """
    Prints out the results """
    def print_results(self, mod):
        if (self.out_mode == "list"):
            mod.printRTMPdata()
        elif (self.out_mode == "m3u"):
            mod.printM3Uentry()
        elif (self.out_mode == "rtmpdump"):
            mod.printRTMPDump()

    """
    Set some object properties """
    def setProperties (self, quiet=False, out_mode=None):
        if not out_mode:
            out_mode="list"
        self.quiet = quiet
        self.out_mode = out_mode

    """
    Output function wrapper """
    def out(self, str):
        if self.quiet == False:
            print str

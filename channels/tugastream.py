'''
Created on 26 de Jul de 2014

@author: Alexandre
'''
#!/usr/bin/env python
#
# Copyright (C) 2013 Andrea Fabrizi <andrea.fabrizi@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#
import re
from tools.BeautifulSoup import BeautifulSoup
import tools.adenUtils as utils
from tools.aden import aden
from channels.channelProvider import channelProvider

class tugastream(channelProvider):

    def __init__(self):
        self.domain = "http://www.tugastream.com"
        self.links = None
        self.channels = None
        
    def scan(self):

        self.links = dict()
        self.channels = list()
        
        data = utils.getUrlData(self.domain)
        parsed_html = BeautifulSoup(data)
        h4 = parsed_html.body.find('h4')
        
        for a in h4.findAll('a'): 
            
            if a.has_key('class') or a.has_key('target'):
                continue
            
            channel = a.text
            
            if channel.startswith('RTP') or channel.find('LINK') >= 0:
                continue
            
            link = self.domain + '/' + a['href']
            
            self.links[channel] = link
            self.channels.append(channel)
         
    def getChannel(self, channel, fmt='m3u'):
        
        if self.channels is None:
            return None
        
        
        adn = aden()
        adn.setProperties(quiet=True, out_mode='m3u')
        adn.loadModules()

        data = utils.getUrlData(self.links[channel])        
        soup = BeautifulSoup(data)        
            
        for iframe in soup.findAll(["iframe", "frame"]):
            
            if iframe.has_key("src") and iframe["src"] and re.search("^http[s]*://.*", iframe["src"], re.IGNORECASE): 

                if fmt in ['m3u']:
                    return adn.scan(iframe["src"], self.links[channel])
                else:
                    raise NotImplementedError

        
            
    """
    Prints out the RTMP properties using the m3u format """
    def getChannels(self):
        
        if self.channels is None:
            self.scan()

        return self.channels
         

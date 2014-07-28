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
from channels.channelProvider import channelProvider

class rtpplay(channelProvider):

    def __init__(self):
        self.domain = "http://www.rtp.pt"
        self.url_list = "http://www.rtp.pt/play/direto"
        self.links = None
        self.titles = None
        self.channels = None
        
    def scan(self):

        self.links = dict()
        self.titles = dict()
        self.channels = list()
        
        html = utils.getUrlData(self.url_list)
        parsed_html = BeautifulSoup(html)
    
        for li in parsed_html.body.findAll('li', attrs={'class':'LiveTVLogo'}):
            channel = li['id']
            a = li.find('a')
            self.channels.append(channel)
            self.links[channel] = self.domain + a['href']
            self.titles[channel] = a['title']
         
    def getChannel(self, channel, fmt='m3u'):
        
        if self.channels is None:
            return None
        
        html = utils.getUrlData(self.links[channel])
        
        parsed_html = BeautifulSoup(html)
        
        div = parsed_html.body.find('div', attrs={'class':'player_media'})
        script = div.find('script')
                    
        m = re.search(r'"file":"([^\"]*)","application":"([^\"]*)","streamer":"([^\"]*)"', utils.trimData(script.text))
        
        if not m:
            return        
        
        if fmt in ['m3u']:
            
            result = "#EXTINF:0," + self.titles[channel] + "\n"
            result += 'rtmp://' + m.group(3) + '/' + m.group(2) + '/' + m.group(1) + ' swfUrl=' + self.domain + '/play/player.swf live=true timeout=15'+"\n"
            return result
        
        else:
            raise NotImplementedError
            
    """
    Prints out the RTMP properties using the m3u format """
    def getChannels(self):
        
        if self.channels is None:
            self.scan()

        return self.channels
         

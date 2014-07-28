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
from tools.BeautifulSoup import BeautifulSoup
import tools.adenUtils as utils
from channels.channelProvider import channelProvider

class euronews(channelProvider):

    def __init__(self):
        self.url = "http://pt.euronews.com/noticias/en-direto"
    
    def getChannel(self, channel, fmt='m3u'):
        
        data = utils.getUrlData(self.url)
        parsed_html = BeautifulSoup(data)
        
        data = parsed_html.body.find('div', attrs={'id':'livePlayer'}).find('a')
        
        if fmt in ['m3u']:
            
            result = "#EXTINF:0, Euronews\n"
            result += data['href']+"\n"
            return result
        
        else:
            raise NotImplementedError
            
    """
    Prints out the RTMP properties using the m3u format """
    def getChannels(self):
        return ['euronews']
         

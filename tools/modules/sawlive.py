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
from tools.adenMod import adenMod
import tools.adenUtils as utils

class yycast(adenMod):

    def __init__(self):
        self.name = "sawlive.tv"
        self.description = "sawlive.tv aden module"
        self.url_embed = "http://sawlive.tv/embed"
        self.url_watch = "http://sawlive.tv/embed/watch"

        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["http://sawlive.tv/embed"]

    def scan(self, url, referer=""):

        m=re.search(r'src="http://sawlive.tv/embed/(.+?)">',utils.trimData(self.pageData))
        
        if m:
            channel_name = m.group(1)
        else:
            return None
        
        m = re.search(r'swidth=([0-9]*),sheight=([0-9]*),g="([0-9]*)"',utils.trimData(self.pageData))

        if not m:
            return None
        
        data = utils.getUrlData(self.url_embed+'/'+channel_name)
        
        m = re.search(r'embed\|view\|(.+?)\|write',data)
        
        if m:
            token = m.group(1).decode('string-escape').replace('|','/')
        else:
            return None

        print self.url_watch+'/'+token
        data = utils.getUrlData(self.url_watch+'/'+token)
        
        m =re.search(r"SWFObject\('(.+?)',",data)
        
        if m:
            swf = m.group(1)
        else:
            return None

        m =re.search(r"'file', '(.+?)'",data)
        
        if m:
            path = m.group(1)
        else:
            return None

        m =re.search(r"'streamer', '(.+?)'",data)
        
        if m:
            rtmp = m.group(1)
        else:
            return None
        
        #Saving the RTMP properties
        self.channel_name = channel_name
        self.RTMP["url"] = rtmp
        self.RTMP["pageUrl"] = self.url_embed+'/'+channel_name
        self.RTMP["swfUrl"] = swf
        self.RTMP["playPath"] = path
        return True

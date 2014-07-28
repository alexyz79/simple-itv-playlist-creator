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
        self.name = "ezcast.tv"
        self.description = "ezcast.tv aden module"
        self.url_lb = "http://www.ezcast.tv:1935/loadbalancer"
        self.domain = "www.ezcast.tv"

        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["http://www.ezcast.tv/static/scripts/ezcast.js", "channel"]

    def scan(self, url, referer=""):

        m = re.search(r'width=([0-9]*),height=([0-9]*),channel="([^\"]*)",g="([0-9]*)"',utils.trimData(self.pageData))
        
        if m:
            width = m.group(1)
            height = m.group(2)
            channel_name = m.group(3)
            g = m.group(4)
        else:
            return None

        #Building ucast url
        ucast_url = "http://%s/embedded/%s/%s/%s/%s" % (self.domain, channel_name, g, width, height)

          
        #Requesting ucast url, with a fake Referer
        data = utils.getUrlData(ucast_url, url)

        #Reading FlashVars from the page
        m = re.search(".*SWFObject\(\"([^\"]*)\".*FlashVars','id=([0-9]*).*", utils.trimData(data))
        
        if m:
            swfUrl = m.group(1)
            channel_id = m.group(2)
        else:
            return None

        #Getting server IP from the load balancer
        data = utils.getUrlData(self.url_lb, url)            
        
        
        m = re.search("^redirect=(.*)", data)
        if m:
            server_ip = m.group(1)
        else:
            return None
        
        #Saving the RTMP properties
        self.channel_name = channel_name
        self.RTMP["app"] = "live"
        self.RTMP["url"] = "rtmp://%s/%s/%s?id=%s" % (server_ip, self.RTMP["app"], channel_name, channel_id)
        self.RTMP["extra"] = "OK"
        self.RTMP["pageUrl"] = ucast_url
        self.RTMP["swfUrl"] = "http://%s%s" % (self.domain, swfUrl)
        self.RTMP["tcUrl"] = "rtmp://%s/%s" % (server_ip, self.RTMP["app"])
        self.RTMP["playPath"] = "%s?id=%s" % (channel_name, channel_id)
        return True

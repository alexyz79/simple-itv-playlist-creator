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
        self.domain = "http://yukons.net"
        self.name = "yukons.net"
        self.description = "yukons.net aden module"
        self.url_embed = "http://yukons.net/embed"
        self.url_yaem = "http://yukons.net/yaem"
        self.url_ld = "http://yukons.net/srvload"
        self.id = '37333730364637323734373333313632'
        self.headers_yaem = { 'Host': 'yukons.net','Connection': 'keep-alive','Accept': '*/*','Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch'}
        self.headers_embed = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Host': 'yukons.net','Cache-Control': 'max-age=0','Accept-Encoding': 'gzip,deflate,sdch','Connection': 'keep-alive'}
        self.headers_ld = {'Host': 'yukons.net','Connection': 'keep-alive','Accept':'*/*','Accept-Encoding': 'gzip,deflate,sdch'}
        """
        The probing strings don't have to be too accurate. In fact they are used only to filter out
        the useless pages and reduce the load for the more accurate function 'scan' """
        self.probeMatches = ["http://yukons.net/share.js"]

    def scan(self, url, referer=""):

        m = re.search(r"'kuyo&file=(.+?)&'",utils.trimData(self.pageData))

        if not m:
            m = re.search(r"file='(.+?)'.+?</script>",utils.trimData(self.pageData))
        
        if not m:
            m = re.search(r'channel="(.+?)".+?</script>',utils.trimData(self.pageData))

        if not m:
            m = re.search(r'file=(.+?)&',utils.trimData(self.pageData))

        if not m:
            return None
        
        self.channel_name = m.group(1)
        
        yaem = self.url_yaem+'/'+self.id
        
        data = utils.getUrlDataT0mm0(yaem, self.headers_yaem, url )
    
        m = re.search(r"return '(.+?)'",data)
        
        if not m:
            return None
        
        embed = self.url_embed+'/'+self.id+'/'+m.group(1)+'/600/450'
        
        data = utils.getUrlDataT0mm0(embed, self.headers_embed, url )
        
        m = re.search(r'FlashVars\|id\|(.+?)\|',data)
        
        if not m:
            return None
        
        id=m.group(1)

        m = re.search(r'\|pid\|\|(.+?)\|',data)
        
        if not m:
            return None
        
        pid = m.group(1)

        m = re.search(r'SWFObject\|.+?\|\|\|(.+?)\|swf\|eplayer',data)
        
        if not m:
            return None
        
        swf = m.group(1)

        ld = self.url_ld+'/'+ id
        
        data = utils.getUrlDataT0mm0(ld, self.headers_ld, url)

        serveraddr = data.replace('srv=','')
        
        self.RTMP["url"] = "rtmp://"+serveraddr+":443/kuyo"
        self.RTMP["playPath"] = self.channel_name + '?id=' + id + '&pid=' + pid
        self.RTMP["swfUrl"] = self.domain + '/' + swf +".swf"
        self.RTMP["pageUrl"] = embed
        
        return True

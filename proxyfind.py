# VisionOnTV player, based on Miro.
# Copyright (C) 2008 VisionOnTV
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

"""proxyfind.py.  Get proxy info from windows."""

from ctypes import Structure, byref, windll
from ctypes.wintypes import LPWSTR, BOOL
import logging
import re

class WINHTTP_CURRENT_USER_IE_PROXY_CONFIG(Structure):
    _fields_ = [
        ('fAutoDetect', BOOL),
        ('lpszAutoConfigUrl', LPWSTR),
        ('lpszProxy', LPWSTR),
        ('lpszProxyBypass', LPWSTR),
        ]

class ProxyInfo:
    def __init__(self):
        self.active = False
        self.host = self.port = None
        self.ignore_hosts = []

def get_proxy_info():
    proxy_info = ProxyInfo()
    ie_proxy_info = WINHTTP_CURRENT_USER_IE_PROXY_CONFIG()
    rv = windll.winhttp.WinHttpGetIEProxyConfigForCurrentUser(
        byref(ie_proxy_info))

    if not rv or ie_proxy_info.lpszProxy is None:
        return proxy_info
    proxy_info.host, proxy_info.port =\
    parse_host_and_port(ie_proxy_info.lpszProxy)
    if ie_proxy_info.lpszProxyBypass is not None:
        proxy_info.ignore_hosts = re.split("[;\s]*",
            ie_proxy_info.lpszProxyBypass)
    return proxy_info

def parse_host_and_port(windows_proxy_string):
    for proxy in re.split("[;\s]*", windows_proxy_string):
        original_string = proxy
        if proxy.startswith("http="):
            proxy = proxy[len('http='):]
        elif '=' in proxy or proxy == '':
            continue
        if '://' in proxy:
            if proxy.startswith("http://"):
                proxy = proxy[len("http://"):]
            else:
                logging.warn("unsupported proxy scheme: %s" % original_string)
                continue
        if ':' in proxy:
            proxy, port = proxy.split(":")
            try:
                port = int(port)
            except ValueError:
                logging.warn("bad proxy port: %s" % original_string)
                continue
        else:
            port = 80
        return proxy, port
    logging.warn("couldn't find proxy: %s" % windows_proxy_string)
    return None, None

if __name__ == "__main__":
    proxy = get_proxy_info()
    print proxy.host
    print proxy.ignore_hosts
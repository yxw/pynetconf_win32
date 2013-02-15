# Copyright (C) 2013 yang.xiaowei@gmail.com
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

"""win32_proxy_config.py.  Configure internet proxy info for windows."""

__author__ = 'yang.xiaowei@gmail.com'
import _winreg

def _get_proxy_key(access=_winreg.KEY_READ):
    return _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
        0, # reserved parameter, always 0
        access # key access type
        )

def get_proxy():
    proxy_key = _get_proxy_key()
    server, stype = _winreg.QueryValueEx(proxy_key, "ProxyServer")
    enabled, etype = _winreg.QueryValueEx(proxy_key, "ProxyEnable")
    _winreg.CloseKey(proxy_key)
    return enabled and server or None

def set_proxy(server):
    proxy_key = _get_proxy_key(_winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(proxy_key, "ProxyServer", 0, _winreg.REG_SZ, server)
    _winreg.SetValueEx(proxy_key, "ProxyEnable", 0, _winreg.REG_DWORD, 1)
    _winreg.CloseKey(proxy_key)

def enable_proxy():
    proxy_key = _get_proxy_key(_winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(proxy_key, "ProxyEnable", 0, _winreg.REG_DWORD, 1)
    _winreg.CloseKey(proxy_key)

def disable_proxy():
    proxy_key = _get_proxy_key(_winreg.KEY_SET_VALUE)
    _winreg.SetValueEx(proxy_key, "ProxyEnable", 0, _winreg.REG_DWORD, 0)
    _winreg.CloseKey(proxy_key)


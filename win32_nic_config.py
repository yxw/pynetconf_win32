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

"""
win32_nic_config.py.  Configure a specific network adaptor info for windows
                by using WMI (http://timgolden.me.uk/python/wmi/index.html).

Usage:
    from win32_nic_config import *
    from win32_proxy_config import *

    import wmi
    interfaces = wmi.WMI().Win32_NetworkAdapterConfiguration( IPEnabled=True )
    for nic in interfaces:
        if nic.Description == "Intel(R) Centrino(R) Advanced-N 6200 AGN":
            #print 'IP address:', nic.IPAddress
            #print 'DHCP enabled:', nic.DHCPEnabled
            nic.EnableStatic(IPAddress=(u'10.81.112.136',), SubnetMask=(u'255.255.255.128',))

            # set a DHCP + dynamic DNS + non-proxy connection
            set_dhcp_conn(nic)
            disable_proxy()

            # set a static IP + static DNS + proxy connection
            set_static_conn(nic, '10.81.112.136', '255.255.255.128', '10.81.112.129', ['10.81.112.129',])
            set_proxy(server="www.example.com:8080")
"""

# -*- coding: utf-8 -*-
__author__ = 'yang.xiaowei@gmail.com'

def set_static_conn(nic, ip_addr, subnet_mask, default_gateway, dns_servers):
    """
    Set static connection for the given Win32_NetworkAdapterConfiguration instance nic.
    """
    if isinstance(ip_addr, str):
        ip_addr = [ip_addr,]
    if isinstance(subnet_mask, str):
        subnet_mask = [subnet_mask,]
    if isinstance(default_gateway, str):
        default_gateway = [default_gateway, ]

    # set defult gateway. return value:
    #   0: success & no reboot required, 
    #   1: sucess & reboot required
    ret = nic.SetGateways(default_gateway)
    print 'Default Gateway updated (status %d)' % ret

    # Set IP adrress & subnet mask. return value:
    #   0: success & no reboot required, 
    #   1: sucess & reboot required
    ret = nic.EnableStatic(IPAddress=ip_addr, SubnetMask=subnet_mask)
    print 'IP Address / Subnet Mask updated (status %d)' % ret

    # set dns servers
    if dns_servers:
        #assert 0 == nic.EnableDNS(DNSServerSearchOrder=dns_servers)
        # or 
        ret = nic.SetDNSServerSearchOrder(dns_servers)
        print 'DNS Server updated (status %d)' % ret

def set_dhcp_conn(nic):
    """
    set given Win32_NetworkAdapterConfiguration instance nic as
    DHCP + dynamic DNS server detection.
    """
    nic.EnableDHCP()
    # After static DNS servers are specified to start using Dynamic Host
    # Configuration Protocol (DHCP) instead of static DNS servers,
    # you can call the method without supplying "in" parameters.
    nic.SetDNSServerSearchOrder()


# -*- coding: utf-8 -*-
from win32_nic_config import *
from win32_proxy_config import *

def set_jaguar_conn(nic):
    """ Set wireless connection as intranet (jaguar) connection.

    test SSID: jaguar
    IP address: 10.81.113.86
    subnet mask: 255.255.255.128
    Default Gateway: 10.81.113.1
    DNS servers: 10.81.112.12, 10.81.112.14
    """
    set_static_conn(nic, '10.81.112.136', '255.255.255.128', '10.81.112.129', ['10.81.112.12','10.81.112.14'])
    enable_proxy()

def set_lion_conn(nic):
    set_dhcp_conn(nic)
    disable_proxy()

if __name__ == "__main__":
    import wmi
    interfaces = wmi.WMI().Win32_NetworkAdapterConfiguration( IPEnabled=True )
    for nic in interfaces:
        if nic.Description == "Intel(R) Centrino(R) Advanced-N 6200 AGN":
            # Ip address: (u'192.168.112.133', u'fe80::31fa:e6d4:261d:5f3a', u'2001:db8:1::1024')
            ip_addr = nic.IPAddress[0]
            if ip_addr.startswith('192.168'):
                print 'Switching from lion to jaguar ...'
                set_jaguar_conn(nic)
            elif ip_addr.startswith('10.81'):
                print 'Switching jaguar to lion ...'
                set_lion_conn(nic)
            else:
                print 'Unknow network connection, pass'


Python scripts to configure network settings for windows:
- TCP/IPv4 properties configuration (DHCP or static)
- DNS server configuration (Dynamic or manual)
- Proxy server configuration

Usage:
```python
import wmi
from win32_nic_config import *
from win32_proxy_config import *
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
```

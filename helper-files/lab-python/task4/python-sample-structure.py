# -*- mode: python; python-indent: 4 -*-
import re
import ipaddress
import ncs
from ncs.application import Service

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        tvars = ncs.template.Variables()
        template = ncs.template.Template(service)
        tvars.add('VPN_ID', service.vpn.vpn_id)
        tvars.add('VPN_NAME', service.vpn_name)
        <... Add code for other common variables>

        for link in service.link:
            tvars.add('LINK_NAME', link.link_name)
            tvars.add('LINK_ID', link.link_id)
            tvars.add('LINK_DESC', link.link_description)
            tvars.add('LINK_VLAN', link.vlan)
            tvars.add('PE_DEVICE', link.pe.device)
            res = re.match('^([a-zA-Z]+)([0-9/]+)$', link.pe.interface)
            tvars.add('PE_INTF_NUM', res.group(2))
            <... Add code for other link variables>

            # Apply PE Configuration
            template.apply('pe-vrf', tvars)
            template.apply('pe-bgp', tvars)
            template.apply('pe-interface', tvars)
            
            # Static routing on PE
            for st in link.pe.static:
                svars = ncs.template.Variables()
                svars = tvars
                if '::' in st:
                  <... Add code for other IPv6 static routing variables>
                  
                else:
                  <... Add code for other IPv4 static routing variables>

                self.log.info(svars)
                template.apply('pe-static', svars)

            # Apply CE Configuration
            template.apply('ce-bgp', tvars)
            template.apply('ce-interface', tvars)

            # Static routing on CE
            for st in link.ce.static:
                svars = ncs.template.Variables()
                svars = tvars
                if '::' in st:
                    svars.add('CE_STATIC', '')
                    svars.add('CE_STATIC_MASK', '')
                    svars.add('CE_STATIC_V6', st)
                else:
                    svars.add('CE_STATIC', ipaddress.ip_network(st).network_address)
                    svars.add('CE_STATIC_MASK', ipaddress.ip_network(st).netmask)
                    svars.add('CE_STATIC_V6', '')
                self.log.info(svars)
                template.apply('ce-static', svars)

# -*- mode: python; python-indent: 4 -*-
from .actions import LinkAction
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
        tvars.add('VPN_DESC', service.vpn.vpn_description)
        tvars.add('VPN_CUST', service.vpn.customer)
        tvars.add('VPN_MAX_PREF', 1000)
        tvars.add('VPN_PREF_THRESH', 80)

        for link in service.link:
            tvars.add('LINK_NAME', link.link_name)
            tvars.add('LINK_ID', link.link_id)
            tvars.add('LINK_DESC', link.link_description)
            tvars.add('LINK_VLAN', link.vlan)
            tvars.add('PE_DEVICE', link.pe.device)
            res = re.match('^([a-zA-Z]+)([0-9/]+)$', link.pe.interface)
            tvars.add('PE_INTF_NUM', res.group(2))
            tvars.add('PE_IP', link.pe.ip)
            tvars.add('PE_IPV6', link.pe.ipv6)
            tvars.add('CE_DEVICE', link.ce.device)
            res = re.match('^([a-zA-Z]+)([0-9/]+)$', link.ce.interface)
            tvars.add('CE_INTF_NUM', res.group(2))
            tvars.add('CE_IP', link.ce.ip)
            tvars.add('CE_IPV6', link.ce.ipv6)
            template.apply('pe-vrf', tvars)
            template.apply('pe-bgp', tvars)
            template.apply('pe-interface', tvars)
            for st in link.pe.static:
                svars = ncs.template.Variables()
                svars = tvars
                if '::' in st:
                    svars.add('PE_STATIC', '')
                    svars.add('PE_STATIC_V6', st)
                else:
                    svars.add('PE_STATIC', st)
                    svars.add('PE_STATIC_V6', '')
                self.log.info(svars)
                template.apply('pe-static', svars)
            template.apply('ce-bgp', tvars)
            template.apply('ce-interface', tvars)
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




    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('l3vpn-servicepoint', ServiceCallbacks)
        self.register_action('l3vpn-check-uplink', LinkAction)
        self.register_action('l3vpn-check-connectivity', LinkAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')

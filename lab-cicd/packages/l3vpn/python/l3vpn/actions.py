import ncs
from ncs.dp import Action
import genie.testbed

class LinkAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('LinkAction: ', name)
        link = ncs.maagic.get_node(trans, kp)
        service = link._parent._parent
        root = ncs.maagic.get_root(trans)

        if name == 'check-uplink':
            self.check_uplink(service, link, root, output)
        if name == 'check-connectivity':
            self.check_connectivity(service, link, root, output)

    def check_uplink(self, service, link, root, output):
        ce_ip = link.ce.ip
        vrf_name = service.vpn_name
        pe_router = link.pe.device

        action = root.devices.device[pe_router].live_status.exec.any
        input = action.get_input()
        input.args = [ f'ping vrf {vrf_name} {ce_ip}' ]

        output.output = action(input).result
        output.success = '100 percent' in output.output

    def check_connectivity(self, service, link, root, output):
        host_data = {
            'protocol': 'telnet',
            'username': 'cisco',
            'password': 'cisco',
            'os': 'ios',
        }
        host_data['ip'] = root.devices.device[link.ce.device].address

        test_setup = genie.testbed.load({'devices': {'host': host_data}})
        host = test_setup.devices['host']
        host.connect(learn_hostname=True)

        output.output = ''
        output.success = True

        this_link = link.link_name
        for l in service.link:
            if l.link_name == this_link:
                continue

            output.output += f'\n{l.link_name} '
            try:
                host.ping(l.ce.ip)
                output.output += 'PASS'
            except:
                output.output += 'FAIL'
                output.success = False

        host.disconnect()

import ncs
from ncs.dp import Action
from _ncs import decrypt
import genie.testbed

class LinkAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, action_input, action_output, trans):
        self.log.info('LinkAction: ', name)
        link = ncs.maagic.get_node(trans, kp)
        service = link._parent._parent
        root = ncs.maagic.get_root(trans)
        trans.maapi.install_crypto_keys()

        if name == 'check-uplink':
            self.check_uplink(service, link, root, action_output)
        if name == 'check-connectivity':
            self.check_connectivity(service, link, root, action_output)

    def check_uplink(self, service, link, root, action_output):
        ce_ip = link.ce.ip
        vrf_name = service.vpn_name
        pe_router = link.pe.device

        exec_action = root.devices.device[pe_router].live_status.exec.any
        exec_input = exec_action.get_input()
        exec_input.args = [ f'ping vrf {vrf_name} {ce_ip}' ]

        action_output.output = exec_action(exec_input).result
        action_output.success = '100 percent' in action_output.output

    def check_connectivity(self, service, link, root, action_output):
        host_data = {
            'protocol': 'ssh',
            'os': 'ios',
        }
        host_data['ip'] = root.devices.device[link.ce.device].address

        auth = root.devices.authgroups.group['labadmin'].default_map
        host_data['username'] = auth.remote_name
        host_data['password'] = decrypt(auth.remote_password)

        test_setup = genie.testbed.load({'devices': {'host': host_data}})
        host = test_setup.devices['host']
        host.connect(learn_hostname=True)

        action_output.output = ''
        action_output.success = True

        this_link = link.link_name
        for l in service.link:
            if l.link_name == this_link:
                continue

            action_output.output += f'\n{l.link_name} '
            try:
                host.ping(l.ce.ip)
                action_output.output += 'PASS'
            except:
                action_output.output += 'FAIL'
                action_output.success = False

        host.disconnect()

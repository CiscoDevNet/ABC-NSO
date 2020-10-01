import argparse
import json
import requests
from ncclient import manager
from ncclient.xml_ import to_ele
from lxml import etree


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description='NSO northbound interface script')

    # Subcommand config
    subparsers = parser.add_subparsers(dest='subcommand')
    get_config = subparsers.add_parser('get-config', help='Subcommand to get a configuration')
    config = subparsers.add_parser('config', help='Subcommand to push a configuration')
    action = subparsers.add_parser('action', help='Subcommand for actions')

    # The method option is used for all subcommands
    method_argument_params = {
        'help': 'Connection method (default: restconf)',
        'default': 'restconf',
        'choices': ['restconf', 'netconf']
    }
    get_config.add_argument('--method', **method_argument_params)
    config.add_argument('--method', **method_argument_params)
    action.add_argument('--method', **method_argument_params)

    # Options for get-config subcommand
    get_config.add_argument('--filter', help=('A resource path for RESTCONF (from restconf/data/) '
                                              'or XPath for NETCONF'))

    # Options for config subcommand
    config.add_argument('--path', required=True,
                        help='A path to a config file (JSON for RESTCONF or XML for NETCONF)')

    # Options for action subcommand
    action.add_argument('--path', help='Action path for RESTCONF (from restconf/data/) or '
                                       'path to the XML action file for NETCONF')
    return parser.parse_args()


class NsoConfig:

    def __init__(self, config_file='config.json'):
        self.config = self.load_config_file(config_file)

    @staticmethod
    def load_config_file(config_file):
        with open(config_file) as f:
            config = json.load(f)
        return config

    @property
    def host(self):
        return self.config.get('host')

    @property
    def username(self):
        return self.config.get('username')

    @property
    def password(self):
        return self.config.get('password')

    @property
    def restconf_port(self):
        return self.config.get('restconf_port')

    @property
    def netconf_port(self):
        return self.config.get('netconf_port')

class Restconf:

    def __init__(self, nso_config):
        self.config = nso_config

        # Common parameters
        self.base_url = f"http://{self.config.host}:{self.config.restconf_port}/restconf/data"
        self.headers = {
            'Accept': 'application/yang-data+json',
            'Content-Type': 'application/yang-data+json'
        }
        self.auth = (self.config.username, self.config.password)

    @staticmethod
    def load_config_file(filename):
        # Load a configuration file in JSON format
        with open(filename) as f:
            content = json.load(f)
        return content

    def get_config(self, filter=None):
        # Code to get a configuration from NSO using RESTCONF
        url = self.base_url
        if filter:
            url += '/' + str(filter)
        headers = self.headers
        auth = self.auth
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        raise Exception(f'Unable to find the running configuration (path: {filter})')

    def push_config(self, filename):
        # Code to push a configuration to NSO using RESTCONF
        url = self.base_url
        headers = self.headers
        auth = self.auth
        content = self.load_config_file(filename)

        response = requests.post(url, json=content, headers=headers, auth=auth)
        if response.status_code != 201:
            raise Exception(f'Error occured: {response.text}')

    def execute_action(self, path):
        # Code to execute an action on NSO using RESTCONF
        url = self.base_url + '/' + path
        headers = self.headers
        auth = self.auth

        response = requests.post(url, headers=headers, auth=auth)
        print(response)
        print(response.text)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        raise Exception(f'Error occured while executing the action: {path}.')

class Netconf:

    def __init__(self, nso_config):
        self.config = nso_config

    @staticmethod
    def load_config_file(filename):
        # Load a configuration file in XML format
        etree_element = etree.parse(filename)
        content = etree.tostring(etree_element).decode('utf-8')
        return content

    def get_config(self, filter=None):
        # Code to get a configuration from NSO using NETCONF
        conf_filter = ('xpath', str(filter)) if filter else None
        with manager.connect(host=self.config.host,
                             port=self.config.netconf_port,
                             username=self.config.username,
                             password=self.config.password,
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False) as m:
            c = m.get_config(source='running', filter=conf_filter)
        if c.ok:
            return etree.tostring(c.data_ele, pretty_print=True).decode('utf-8')
        raise Exception(f'Unable to find the running configuration (path: {filter})')

    def push_config(self, filename):
        # Code to push a configuration to NSO using NETCONF
        content = self.load_config_file(filename)
        with manager.connect(host=self.config.host,
                             port=self.config.netconf_port,
                             username=self.config.username,
                             password=self.config.password,
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False) as m:
            c = m.edit_config(target='running', config=content)
        if not c.ok:
            raise Exception(f'Error occured while pushing the configuration: {str(c.error)}')

    def execute_action(self, path):
        # Code to execute an action on NSO using NETCONF
        content = self.load_config_file(path)
        print(content)
        with manager.connect(host=self.config.host,
                             port=self.config.netconf_port,
                             username=self.config.username,
                             password=self.config.password,
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False) as m:
            c = m.dispatch(to_ele(content))
        if c.ok:
            if c.data_ele.findall('.//{http://com/example/l3vpn}success')[0].text.lower() != "true":
                print("Action Failed!\n{}".format(etree.tostring(c.data_ele, pretty_print=True).decode('utf-8')))
                exit(1)
            return etree.tostring(c.data_ele, pretty_print=True).decode('utf-8')
        raise Exception(f'Error occured while executing the action: {content}.')


def load_api(method):
    if method == 'restconf':
        return Restconf
    return Netconf

if __name__ == "__main__":
    args = parse_cli_arguments()

    nso_config = NsoConfig()

    api_class = load_api(args.method)
    api = api_class(nso_config)

    if args.subcommand == 'get-config':
        filter = args.filter if 'filter' in args else None
        config = api.get_config(filter)
        print(config)
    if args.subcommand == 'config':
        api.push_config(args.path)
    elif args.subcommand == 'action':
        output = api.execute_action(args.path)
        print(output)

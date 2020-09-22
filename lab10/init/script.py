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
        self.base_url = None
        self.headers = None
        self.auth = None

    @staticmethod
    def load_config_file(filename):
        # Load a configuration file in JSON format
        pass

    def get_config(self, filter=None):
        # Code to get a configuration from NSO using RESTCONF
        pass

    def push_config(self, filename):
        # Code to push a configuration to NSO using RESTCONF
        content = self.load_config_file(filename)
        pass

    def execute_action(self, path):
        # Code to execute an action on NSO using RESTCONF
        pass

class Netconf:

    def __init__(self, nso_config):
        self.config = nso_config

    @staticmethod
    def load_config_file(filename):
        # Load a configuration file in XML format
        pass

    def get_config(self, filter=None):
        # Code to get a configuration from NSO using NETCONF
        pass

    def push_config(self, filename):
        # Code to push a configuration to NSO using NETCONF
        content = self.load_config_file(filename)
        pass

    def execute_action(self, path):
        # Code to execute an action on NSO using NETCONF
        pass


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

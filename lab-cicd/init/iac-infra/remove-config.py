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
    config = subparsers.add_parser('config', help='Subcommand to push a configuration')

    # The method option is used for all subcommands
    method_argument_params = {
        'help': 'Connection method (default: restconf)',
        'default': 'restconf',
        'choices': ['netconf']
    }
    config.add_argument('--method', **method_argument_params)

    # Options for config subcommand
    config.add_argument('--path', required=True,
                        help='A path to a config file (JSON for RESTCONF or XML for NETCONF)')

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

class Netconf:

    def __init__(self, nso_config):
        self.config = nso_config

    @staticmethod
    def load_config_file(filename):
        # Load a configuration file in XML format
        etree_element = etree.parse(filename)
        content = etree.tostring(etree_element).decode('utf-8')
        return content

    def push_config(self, filename):
        # Remove each node of the config
        content = self.load_config_file(filename)
        root = etree.fromstring(content.encode('utf-8'))
        for elem in root.getchildren():
            elem.attrib["operation"] = "remove"
        content = etree.tostring(root).decode('utf-8')
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

def load_api(method):
    if method == 'restconf':
        return Restconf
    return Netconf

if __name__ == "__main__":
    args = parse_cli_arguments()

    nso_config = NsoConfig()

    api_class = load_api(args.method)
    api = api_class(nso_config)

    if args.subcommand == 'config':
        api.push_config(args.path)

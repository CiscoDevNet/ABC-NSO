"""
Sample script to interact with Cisco NSO using RESTCONF or NETCONF.
"""
import argparse
import json
import requests
from ncclient import manager
from ncclient.xml_ import to_ele
from lxml import etree


def parse_cli_arguments():
    """
    Parse arguments provided to the script via the CLI and return the results.

    :return: Object reference of argparse.ArgumentParser.parser_args()
    """

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
    """
    Base NSO configuration class to be inherited by classes defined for
    manipulating data within Cisco NSO.  Reads connection parameters for
    NSO and enables access to those properties (host, username, password,
    port data, etc.)
    """

    def __init__(self, config_file='config.json'):
        """
        Initialize the class.  Reads config_file if specified, else read the
        default "config.json" to obtain NSO parameters.

        :param config_file: Optional - name of JSON-formatted config file
          containing the NSO connection information.
        """
        self.config = self.load_nso_config_file(config_file)

    def __enter__(self):
        """
        Placeholder method to support Python context manager invocation

        :return: Object reference for this class
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Python context manager exit tasks - place any object cleanup tasks here

        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Traceback details if needed
        :return: True
        """
        return True

    @staticmethod
    def load_nso_config_file(config_file):
        """
        Given a JSON-formatted configuration file, load the data into a Python
        object and return the resulting data structure.

        :param config_file: Name of configuration file to load.  Defaults to
          "config.json"

        :return: Python JSON object representing the config file contents.
        """
        with open(config_file, "r", encoding="utf-8") as filehandle:
            config = json.load(filehandle)
        return config

    @property
    def host(self):
        """
        Set the object property "host" to the NSO host

        :return: NSO hostname or IP property specified in JSON config file.
        """
        return self.config.get('host')

    @property
    def username(self):
        """
        Set the object property "username" to the username for connecting to
        NSO.

        :return: NSO connection username as specified in JSON config file.
        """
        return self.config.get('username')

    @property
    def password(self):
        """
        Set the object property "password" to the password used for the NSO
        connection.

        :return: NSO connection password as specified in JSON config file.
        """
        return self.config.get('password')

    @property
    def restconf_port(self):
        """
        Set the object property "restconf_port" to the port used for the NSO
        RESTCONF connection.

        :return: NSO RESTCONF connection port as specified in JSON config file.
        """
        return self.config.get('restconf_port')

    @property
    def netconf_port(self):
        """
        Set the object property "netconf_port" to the port used for the NSO
        NETCONF connection.

        :return: NSO NETCONF connection port as specified in JSON config file.
        """
        return self.config.get('netconf_port')


class Restconf(NsoConfig):
    """
    Class definition containing methods for interacting with NSO via the
    RESTCONF protocol.
    """

    def __init__(self):
        """
        Initialize the object upon instantiation.

        Call super() to instantiate the NsoConfig object and set the available
        object properties.  Afterward, create a new session for Python Requests
        which will be used for interacting with RESTCONF via HTTP/HTTPS.
        """
        super().__init__()

        self.http = requests.Session()
        # Common parameters
        self.base_url = f"http://{self.host}:{self.restconf_port}/restconf/data"
        self.http.headers = {
            "Accept": "",  # <TODO> - Set correct value for Accept header
            "Content-Type": ""  # <TODO> - Set correct value for Content-Type
        }
        self.http.auth = ()  # <TODO> - Set auth username and password

    @staticmethod
    def load_config_file(filename):
        """
        Given a JSON-formatted file containing device configuration, load the
        contents into a Python JSON object and return the object reference.

        :param filename: Name of the configuration file to import

        :return: JSON object reference of configuration file contents
        """
        # Load a configuration file in JSON format
        with open() as filehandle:  # <TODO> - Open the file read-only with utf-8 encoding
            content = json.load(filehandle)
        return content

    def get_config(self, path=None):
        """
        Given an optional xpath filter, get the configuration from NSO via
        RESTCONF

        :param path: (Optional) URL endpoint for RESTCONF config retrieval
          filtering.

        :return: JSON object reference of the RESTCONF response.
        """
        # Code to get a configuration from NSO using RESTCONF
        url = self.base_url

        if path:
            url = f"{url}/{str(path)}"  # <TODO> - Append query_path to the URL

        print()  # <TODO> - print a message indicating the path for the GET request
        response = self.http.get(url)

        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        raise Exception(f'Unable to find the running configuration (path: {filter})')

    def push_config(self, filename):
        """
        Given a JSON-formatted configuration file "filename", load the config
        data and send the configuration to NSO to be applied to the device.

        :param filename: JSON-formatted filename containing device
          configuration data.

        :return: None (no return)
        """
        # Code to push a configuration to NSO using RESTCONF
        url = self.base_url

        # <TODO> - Create variable "content" containing the result from
        # loading the configuration file "filename"


        # <TODO> - Create the "response" variable containing the HTTP POST


        print(f"{response.status_code}: {response.text}")
        if response.status_code != 201:
            raise Exception(f'Error occured: {response.text}')

    def execute_action(self, path):
        """
        Execute an arbitrary RESTCONF action against NSO.

        :param path: NSO Endpoint path to use for the RESTCONF POST operation.

        :return: JSON object reference of the NSO RESTCONF result.
        """
        # Code to execute an action on NSO using RESTCONF
        url = f""  # <TODO> - Create the URL endpoint for the HTTP POST

        print(f"Executing HTTP POST to endpoint {url}...")

        # <TODO> - Create the "response" variable to execute an HTTP POST
        # and store the result.


        print(response)
        print(response.text)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        raise Exception(f'Error occured while executing the action: {path}.')

class Netconf(NsoConfig):
    """
    Class definition containing methods for interacting with NSO via the
    NETCONF protocol.
    """

    def __init__(self):
        """
        Initialize the object upon instantiation.

        Call super() to instantiate the NsoConfig object and set the available
        object properties.  Afterward, create a new session for Python Requests
        which will be used for interacting with NETCONF via SSH.
        """
        super().__init__()

        self.netconf_manager = manager.connect()  # <TODO> - Define connection parameters

    @staticmethod
    def load_config_file(filename):
        """
        Given an XML-formatted file containing device configuration, load the
        contents into a Python etree object and return the object reference.

        :param filename: Name of the configuration file to import

        :return: XML etree object reference of configuration file contents
        """
        # Load a configuration file in XML format
        etree_element = etree.parse()  # <TODO> - Specify the filename to load
        content = etree.tostring().decode()  # <TODO> - Specify the variable to cast to string and the file encoding
        return content

    def get_config(self, xpath_filter=None):
        """
        Given an optional xpath filter, get the configuration from NSO via
        NETCONF

        :param filter: (Optional) xpath filter for NETCONF config retrieval
          filtering.

        :return: XML string representation of the NETCONF response.
        """
        # Code to get a configuration from NSO using NETCONF
        conf_filter = ('xpath', str(xpath_filter)) if xpath_filter else None

        # <TODO> - Create a get_config NETCONF request with proper parameters


        if nc_result.ok:
            return etree.tostring(nc_result.data_ele, pretty_print=True).decode('utf-8')
        raise Exception(f'Unable to find the running configuration (path: {xpath_filter})')

    def push_config(self, filename):
        """
        Given an XML-formatted configuration file "filename", load the config
        data and send the configuration to NSO to be applied to the device.

        :param filename: XML-formatted filename containing device
          configuration data.

        :return: None (no return)
        """
        # Code to push a configuration to NSO using NETCONF
        content = self.load_config_file(filename)

        # <TODO> - Complete the print statement to show the XPath
        print()

        # <TODO> - Create the nc_result variable containing the result of edit_config


        if not nc_result.ok:
            raise Exception(f'Error occured while pushing the configuration: {str(nc_result.error)}')

    def execute_action(self, path):
        """
        Execute an arbitrary NETCONF action against NSO.

        :param path: NSO Endpoint path to use for the NETCONF RPC.

        :return: XML string representation of the NSO NETCONF response
        """
        # Code to execute an action on NSO using NETCONF

        # <TODO> - Load the config specified by "path" and print the contents

        # <TODO> - Send an arbitrary payload using the NETCONF client
        nc_result = self.netconf_manager.dispatch()

        if nc_result.ok:
            return etree.tostring(nc_result.data_ele, pretty_print=True).decode('utf-8')
        raise Exception(f'Error occured while executing the action: {content}.')


def get_class_name(method):
    """
    Given the CLI argument --method, determine if NETCONF or RESTCONF should be
    used for the NSO operations.  The value returned will be used to
    instantiate the proper class for interaction with NSO.

    :param method: argparse value specified for --method on the CLI

    :return: "Restconf" if "--method restconf" is passed, otherwise "Netconf"
      by default (or if --method netconf is passed via the CLI)
    """

    if method == 'restconf':
        api_method = "Restconf"
    else:
        api_method = "Netconf"

    return api_method


if __name__ == "__main__":
    # Grab the command-line arguments and determine what to do
    args = parse_cli_arguments()

    # Use load_api to identify the class to instantiate
    api_class = get_class_name(args.method)

    # Finally, instantiate an object from the returned class name.
    with globals()[api_class]() as api:

        # Determine what to do based on the "subcommand" argument parser result.
        if args.subcommand == 'get-config':
            query_filter = args.filter if 'filter' in args else None
            device_config = api.get_config(query_filter)
            print(device_config)
        if args.subcommand == 'config':
            api.push_config(args.path)
        elif args.subcommand == 'action':
            output = api.execute_action(args.path)
            print(output)

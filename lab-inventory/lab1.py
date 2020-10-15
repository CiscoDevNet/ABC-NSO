import ncs

def add_devices(ned_id, devices):
    """Bulk add devices to NSO.

    ned_id: ID of the NED to use, e.g. 'cisco-ios-cli-3.8'.
    devices: Dictionary of device name -> address mapping.

    Return: none.

    Example: add_devices('cisco-ios-cli-3.8', { 'some-router-1': '10.0.0.1' })
    """
    with ncs.maapi.single_write_trans('admin', '') as t:
        root = ncs.maagic.get_root(t)
        if not hasattr(devices, '__iter__'):
            print('Error: Devices should be a dictionary!')
            return

        for device in devices:
            if device not in root.devices.device:
                d = root.devices.device.create(device)
                d.address = devices[device]
                d.authgroup = 'default'
                d.device_type.cli.ned_id = ned_id
                d.state.admin_state = 'unlocked'
                print('Added ' + device)

        t.apply()

def add_devices_to_group(group, prefix):
    """Adds all devices with names matching prefix to group.

    group: Device group to add to.
    prefix: Prefix of device names that will be added.

    Example: add_devices_to_group('test-group', 'some-router-')
    """
    with ncs.maapi.single_write_trans('admin', '') as t:
        root = ncs.maagic.get_root(t)
        try:
            devices = root.devices.device_group[group].device_name
        except KeyError:
            print('Error: Group not found!')
            return

        for d in root.devices.device:
            device = d.name
            if device.startswith(prefix):
                devices.create(device)
                print('Added ' + device)

        t.apply()

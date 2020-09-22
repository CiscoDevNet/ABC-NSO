# ABC-NSO

## Mandatory Steps Pre-Bootcamp

1. Install the remote extension pack for Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
2. Connect to the remote developer@10.10.20.50
3. Open a Terminal in VSCode (which should be on the Devbox)
4. Clone this repo:
```sh
git clone https://github.com/CiscoDevNet/ABC-NSO.git
```

## Starting a Lab

To prepare the lab environment, call the `start` script with the desired lab from a Terminal pane within VSCode. e.g.:

```sh
$ sh start lab-<name>
```

Then, change directory to `~/nso-lab-<name>` and run `code -a .` to open that directory within the VSCode window.

The script expects NSO to be installed in `~/nso`, which must include all of the required NEDs.  Everything will deploy to the `~/nso-lab-<name>` directory, with a `~/nso-lab` symlink for convenience.

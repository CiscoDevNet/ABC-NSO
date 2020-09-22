# ABC-NSO

## Mandatory Steps Pre-Bootcamp

1. Install the remote extension pack for Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
2. Connect to the remote developer@10.10.20.50
3. Open a Terminal in VSCode (which should be on the Devbox)
4. Clone this repo (or optionally fork the repo from https://github.com/CiscoDevNet/ABC-NSO and clone your fork)
```sh
git clone https://github.com/CiscoDevNet/ABC-NSO.git
```
5. Change directory to `ABC-NSO` and run `code -a .` from the VSCode Terminal

## Starting a Lab

To prepare the lab environment, call the `start` script with the desired lab. e.g.:

```sh
$ sh start lab-<name>
```

The script expects NSO to be installed in `~/nso`, which must include all of the required NEDs.  Everything will deploy to the `~/nso-<lab>` directory, with a `~/nso-lab` symlink for convenience.

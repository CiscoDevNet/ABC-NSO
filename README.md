# ABC-NSO

## Mandatory Steps Pre-Bootcamp

1. Install the remote extension pack for Visual Studio Code (https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
2. Clone this repo.
```
git clone https://github.com/CiscoDevNet/ABC-NSO.git
```
3. Open the ABC-NSO directory inside of Visual Studio Code.
4. When prompted, select to 'reopen in container'.

## Starting a Lab

To prepare the lab environment, call the `start` script with the desired lab. e.g.:

```sh
$ sh start lab-<name>
```

The script expects NSO to be installed in `~/nso`, which must include all of the required NEDs.  Everything will deploy to the `~/nso-<lab>` directory, with a `~/nso-lab` symlink for convenience.

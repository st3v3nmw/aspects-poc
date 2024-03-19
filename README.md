# Aspects PoC

A proof of concept for snap configuration sharing across snaps using snapd's aspects.

## Installation

The snaps are currently available from the Snap Store on the edge channel:

```console
$ sudo snap install aspects-follower --edge --devmode
aspects-follower (edge) 0.1 from Stephen Mwangi (st3v3nmw) installed

$ sudo snap install aspects-registration-agent --edge --devmode
aspects-registration-agent (edge) 0.1 from Stephen Mwangi (st3v3nmw) installed

$ sudo snap install aspects-server --edge --devmode
aspects-server (edge) 0.1 from Stephen Mwangi (st3v3nmw) installed
```

## Development

### Building the snaps

Run `make` or `make all` to build all snaps at once or run the following commands to build them individually:

```console
$ make follower
Building follower snap...
Generated snap metadata
Created snap package aspects-follower_0.1_amd64.snap

$ make registration-agent
Building registration-agent snap...
Generated snap metadata
Created snap package aspects-registration-agent_0.1_amd64.snap

$ make server
Building server snap...
Generated snap metadata
Created snap package aspects-server_0.1_amd64.snap
```

### Installing the snaps

To use the make targets below, make sure you have [yq](https://github.com/mikefarah/yq) installed. You can install it using [Homebrew](https://brew.sh/) or as a snap:

```console
$ brew install yq
$ snap install yq
```

Run `make install-all` to install all the snaps at once or run the following commands to install them individually:

```console
$ make install-follower
Installing follower snap...
aspects-follower 0.1 installed

$ make install-registration-agent
Installing registration-agent snap...
aspects-registration-agent 0.1 installed

$ make install-server
Installing server snap...
aspects-server 0.1 installed
```

#!/bin/bash

ACCOUNT_ID=f22PSauKuNkwQTM9Wz67ZCjNACuSjjhN
SIGNING_PUBLIC_KEY=xkd_Y2ay5N2Uo14v_wsCtfVJYLAVbJgxbiKM8Ne4mZBflaROriZgk2nb5i9Oebum
CHANNEL=edge


# Ack the assertions
echo "Acknowledging account/$ACCOUNT_ID assertion..."
snap known --remote account account-id=$ACCOUNT_ID | snap ack /dev/stdin

echo "Acknowledging account-key/$SIGNING_PUBLIC_KEY assertion..."
snap known --remote account-key public-key-sha3-384=$SIGNING_PUBLIC_KEY | snap ack /dev/stdin

echo "Acknowledging aspect-bundle/aspects-poc assertion..."
curl -fsSL https://raw.githubusercontent.com/st3v3nmw/aspects-poc/main/aspects-poc.aspect-bundle | snap ack /dev/stdin


# Enable experimental features
sudo snap set system experimental.aspects-configuration=true
sudo snap set system experimental.parallel-instances=true


# Install the snaps
install_snap() {
    echo "Installing $1..."
    sudo snap install $1 --$CHANNEL --devmode
    snap connections $1 | awk '{print $2}' | tail -n +2 | xargs -I {} sudo snap connect {}
}

install_snap aspects-server
install_snap aspects-registration-agent
install_snap aspects-follower_1
install_snap aspects-follower_2
install_snap aspects-follower_3
install_snap aspects-follower_4

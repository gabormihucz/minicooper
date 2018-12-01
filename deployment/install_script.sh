#!/bin/bash
echo "Deploying project..."

echo "Installing git and ssh..."
apt-get install git

apt-get install ssh
ssh-add darryl_key
eval $(ssh-agent -s)

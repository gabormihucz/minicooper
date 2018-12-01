#!/bin/bash
echo "Deploying project..."

echo "Installing git and ssh..."
apt-get install git

apt-get install ssh
ssh-add darryl_key
eval $(ssh-agent -s)

git init
git add remote origin git@stgit.dcs.gla.ac.uk:tp3-2018-cs15/dissertation.git
git pull origin master

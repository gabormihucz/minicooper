#!/bin/bash
echo "Deploying project..."

echo "Installing git and ssh..."
apt-get install git
apt-get install ssh

echo "Setting up ssh..."
chmod 400 darryl_key
eval $(ssh-agent -s)
ssh-add darryl_key

echo "Receiving latest working build from remote repository..."
git init
git remote add origin git@stgit.dcs.gla.ac.uk:tp3-2018-cs15/dissertation.git
git pull origin master


echo "Installing requirements and dependencies..."
pip install -r requirements.txt
pip install -r dependencies.txt

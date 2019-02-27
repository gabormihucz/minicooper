#!/bin/bash
echo "Deploying project..."

echo "Installing dependencies from apt..."
sudo apt -y install python3 python3-pip tesseract-ocr libtesseract-dev virtualenv

echo "Setting up virtual environment..."
virtualenv -p python3 venv
. venv/bin/activate

echo "Installing dependencies..."
pip3 install -r dependencies.txt

echo "Populating database..."
python3 MCweb/MCwebDjango/manage.py makemigrations
python3 MCweb/MCwebDjango/manage.py migrate

echo "Running server..."
python3 MCweb/MCwebDjango/manage.py runserver

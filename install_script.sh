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
cd MCweb/MCwebDjango
python3 manage.py makemigrations
python3 manage.py migrate
python3 populate.py

echo "Running server..."
python3 manage.py runserver
#!/bin/bash
echo "Running project..."

echo "Activating virtual environment..."
. venv/bin/activate

echo "Running server..."
cd MCweb/MCwebDjango
python3 manage.py runserver
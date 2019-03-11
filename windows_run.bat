ECHO OFF

ECHO "Running Virtual Environment..."
CALL venv\scripts\activate.bat &:: W waits for the program to end, B starts it in the same command prompt instance

ECHO "Creating database..."
cd MCweb\MCwebDjango\
python manage.py migrate
python manage.py makemigrations

ECHO "Starting server..."
python manage.py runserver

CD ..\..
:End
cmd /k
ECHO OFF

ECHO "Deploying project..."

ECHO "Installing Python 3 (pip3 included)..."
powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe -OutFile python3.exe"
start /W python3.exe
DEL python3.exe

ECHO "Installing Tesseract OCR..."
powershell -Command "Invoke-WebRequest https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0.20181030.exe -OutFile tesseract.exe"
start /W tesseract.exe
DEL tesseract.exe

ECHO "Installing Windows Server 2003 Resource Kit Tools..."
powershell -Command "Invoke-WebRequest https://download.microsoft.com/download/8/e/c/8ec3a7d8-05b4-440a-a71e-ca3ee25fe057/rktools.exe -OutFile rktools.exe"
start /W rktools.exe
DEL rktools.exe

pathman /au "C:\Program Files (x86)\Tesseract-OCR"
pathman /au "C:\Program Files\Poppler"
pathman /au "%USERPROFILE%\AppData\Local\Programs\Python\Python37\Scripts\"
pathman /au "%USERPROFILE%\AppData\Local\Programs\Python\Python37\"


ECHO "Installing virtualenv..."
pip3 install virtualenv

ECHO "Creating & initializing virtual environment..."
virtualenv venv
CALL venv\scripts\activate.bat &:: W waits for the program to end, B starts it in the same command prompt window

ECHO "Installing dependencies..."
pip3 install -r dependencies.txt

ECHO "Creating database..."
cd MCweb\MCwebDjango\
python manage.py migrate
python manage.py makemigrations

ECHO "Starting server..."
python manage.py runserver

CD ..\..
:End
cmd /k
# dissertation
CS15 --- team project

## Get the software

If you do not have the project in a zip file yet: click on CI/CD/Pipelines. Then under the button CI Lint, click on the latest button with a cloud symbol and an arrow pointing downards and click on 'Download build artifacts'.  

## OS Requirements:

- Currently the website has been tested on Debian-based Linux and on Windows environments
- The app works on Windows and UNIX-based systems as well

## Deployment guide: 

### On Linux

Extract the zipped project file to a directory of your choice.  

After that, open a terminal window in the folder 'dissertation'.  
Give the file 'install_script.sh' execution permission by executing `chmod +x install_script.sh`.  
Then run  `sudo bash install_script.sh`.  

Once that's done, open your preferred web browser and go to http://127.0.0.1:8000/  to load the website  

To login as a superuser:  
username: superuser  
password: superpass  


In order to start the file watching, go to the MCapp folder and execute

`python3 filewatcher.py`

You can change the watched folder in `filewatcher.py` and you can change the server address in `post_to_server.py`

### On Windows

Firstly, you will need to install poppler. [Download poppler by clicking here.](http://blog.alivate.com.au/wp-content/uploads/2018/10/poppler-0.68.0_x86.7z) 
Extract the contents of the poppler directory in the archive you just downloaded under `C:\Program Files\Poppler`.

Double-click on `windows_install.bat`. If you get any error regarding "python3", just ignore it.
Install Tesseract and Windows Server by following the pop-up setup wizards with default settings.

Once that's done, open your preferred web browser and go to http://127.0.0.1:8000/  to load the website  

To login as a superuser:  
username: superuser  
password: superpass  

In order to start the file watching, go to the MCapp folder and double-click

`filewatcher.py`

Leave the black window open as long as you want to have the file watcher running.

The default folder the PDFs are uploaded to the website is the current working directory of `filewatcher.py`. You can change the watched folder in `filewatcher.py` and you can change the server address in `post_to_server.py`


## User guide

Minicooper allows you to automatically upload PDFs to a website by copying them to a directory of your choice. The PDFs will be converted to JSON based on user-created templates and displayed on the website.

### User Scenario

Company A deals with thousands of PDF files each day. There is a dedicated employee whose job is to manually open these PDFs and enter the relevant information on them to an online form.
There are only a few types of PDFs however (e.g. flight tickets, invoices for a certain product, etc.), and the relevant information (e.g. price, quantity, date, etc.) appears at the same place on each PDF.
Company A would like to automise this repetitive task by converting the contents of the PDFs to JSON format (key: value pairs, where the value should be the relevant content of the PDF), based on user-defined templates.
Templates indicate the areas where the relevant content of a PDF will be found. Each area (a rectangle on an A4 PDF page) will have a label, which will serve as the key of the JSON.

Company A would like to make the process as automatic as possible. Because of this, PDFs dragged to a specific folder should be automatically uploaded to a website where the processing will take place and where the results will be stored.
Furthermore, the template being applied to each PDF should depend on the filename of the PDF. 

### The website

##### As a regular user

###### Results page

You first need to register/login to access the results page.

Once logged in, you can see the previously converted PDF files, along with their corresponding JSON files. Status indicated whether the conversion was successful, that is, if all mandatory fields in a template were populated. You can also see the template that was applied during the conversion and the user who created that template. Finally the date and time of the conversion is also listed.
In the search bar, you can search for patterns appearing in the JSON file. Hitting enter will list all the files that have the pattern you searched for.

#### As a superuser

###### Template Creator

You can create *templates* by clicking on 'Create Template'.

First give a title to your template to be created.
Then click on 'Upload PDF' to upload a PDF based on which you will draw your pattern. Once your PDF is uploaded, click on the 'Draw Rectangle' button, and draw a rectangle over a field you would like to process in subsequent PDFs. Once you drew the rectangle, if you click and hold it, you can move it around the template. To get meaningful results, please draw rectangles **containing only one line of text**. If you want to convert something that is broken into multiple lines, (e.g. an address field), please draw multiple rectangles. 
On the right hand side, give a name to your rectangle: this will be they key in your JSON output. Select whether the rectangle's conversion should be mandatory or optional. If the output of any mandatory rectangle in a template is empty that will label the status of the conversion as 'Fail'. Empty outputs of optional rectangles will not be flagged as failed conversions. You can manually change the coordinates of the rectangles by changing the x and y values of the top left and bottom right corners.
If you made a mistake and you want to delete a rectangle, select a rectangle and click on the 'Delete' button.
Finally, once you finished creating the template, click on 'Save Template'.

###### Template Manager

To manage the properties of already existing templates, click on 'Manage'. You will see the list of templates currently in the database. Clicking on one template will open a drop-down, where you can define *patterns*.
Patterns are used to automatically match PDF files to templates. From the drop-down, you can select 'Starts with', 'Contains' and 'Ends with'.
For example, if you wanted to upload PDFs with the title of the form SupermarketBills_XX, and convert them based on the template 'SuperBills', you could select 'Starts with', write 'SupermarketBills' into the entry field and click Add.
After having done this, if you dropped a PDF filename that begins with 'SupermarketBills', that file would be converted based on the template 'SuperBills'.
You can add multiple patterns to a template. If a filename matches any of the defined patterns of a template, that template will be applied to the patterns.

If a filename matches multiple templates, the first template in the list will be applied.

On Template Manager, for each template you can also see two buttons: 'Edit' and 'Delete'. Delete will delete the template. Clicking on 'Edit' will take you to the page to edit that template.

###### Template Editor

Once at the Template Editor, click on 'Upload PDF' and upload a PDF file that you would like your template to be based upon. Once the PDF is uploaded, you will be able to see the predefined rectangles on it, and you can alter them as you like. Similarly, you can changed the labels of the rectangles, as well as the title of the template as well.
Click 'Save' to save your changes.

###### Admin site

Clicking on 'Admin' lands you on the Django Administration page, where you can directly view and alter the database. Click on 'Users' to view/delete/update existing users or add new ones. Click on a specific user and tick/untick the superuser box to grant/revoke superuser rights.
Under MCWEBAPP, you can view/delete/update the other entities in the database. To delete a record on the results page, click 'Json files', and find the name of the Json file you would like to delete.

### The app

In order to run the app, open a terminal window in the folder 'dissertation/MCapp' and run
python3 filewatcher.py

This will start the filewatching process. Drag and drop files with the extension ".pdf" into the current folder. These will then be uploaded to the webserver and deleted from the local filesystem.
On the results page, you will be able to see the uploaded PDF, as well as the converted JSON, based on the template the file's filename indicated.
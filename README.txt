User guide

Minicooper allows you to automatically upload PDFs to a website by copying them to a directory of your choice. The PDFs will be converted to JSON based on user-created templates and displayed on the website.

The website

As a regular user

Results page

You first need to register/login to access the results page.

Once logged in, you can see the previously converted PDF files, along with their corresponding JSON files. Status indicated whether the conversion was successful, that is, if all mandatory fields in a template were populated. You can also see the template that was applied during the conversion and the user who created that template. Finally the date and time of the conversion is also listed.
In the search bar, you can search for patterns appearing in the JSON file. Hitting enter will list all the files that have the pattern you searched for.

As a superuser

Template Creator

You can also create templates by clicking on 'Create Template'.

First give a title to your template to be created.
Then click on 'Upload PDF' to upload a PDF based on which you will draw your pattern. Once your PDF is uploaded, click on the 'Draw Rectangle' button, and draw a rectangle over a field you would like to process in subsequent PDFs. Once you drew the rectangle, if you click and hold it, you can move it around the template. To get meaningful results, please draw rectangles containing only one line of text. If you want to convert something that is broken into multiple lines, (e.g. and address field), please draw multiple rectangles. 
On the right hand side, give a name to your rectangle: this will be they key in your JSON output. Select whether the rectangle's conversion should be mandatory or optional. If the output of any mandatory rectangle in a template is empty that will label the status of the conversion as 'Fail'. Empty outputs of optional rectangles will not be flagged as failed conversions. You can manually change the coordinates of the rectangles by changing the x and y values of the top left and bottom right corners.
Select a rectangle and click on the 'Delete' button to delete it.
Finally, once you finished creating the template, click on Save Template.

Template Manager

...

Admin site

Clicking on 'Admin' lands you on the Django Administration page, where you can directly view and alter the database. Click on 'Users' to view/delete/update existing users or add new ones. Click on a specific user and tick/untick the superuser box to grant/revoke superuser rights.
Under MCWEBAPP, you can view/delete/update the other entities in the database. To delete a record on the results page, click 'Json files', and find the name of the Json file you would like to delete.

The app

In order to run the app, open a terminal window in the folder 'dissertation/MCapp' and run
python3 filewatcher.py
While filewatcher.py is running, all files with the extension '.pdf' in 'dissertation/MCapp' will be uploaded to the website and deleted from the directory subsequently. Please refresh the results page to see the conversion details.
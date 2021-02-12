# Information
This project implemented a calculator for the opening and closing times for an ACP brevet.
A brevet is a course in which cyclists will travel through various control points.
A control is basically a checkpoint. 

# Testing
To test the calculator, simply run 'nosetests' (if you have it installed). Otherwise, you can run 
the following command:

'docker exec -it <container-id> nosetests --tests=<file-name>

The testing file is located within the 'test/' folder.

# Running
To run the container, type the following into the terminal:
'docker build -t <name> .'
'docker run -d -p 5000:5000 <name>'

# Function Info
The open_time() function requires a control location as an int, the brevet length as an int, and 
the brevet start time as a string in ISO 8610 format.
It will return the starting time of the control location in ISO 8610 format.

The close_time() function takes the same arguments, and returns the closing time of the control 
location in ISO 8610 format.

# Contact Info
Author: River Veek
Date: 10 November 2020
Email: riverv@uoregon.edu

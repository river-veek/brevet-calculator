# Project 6: Brevet Time Calculator Service
Implementing RESTful architecture.

## What is in this Repository
You have a minimal implementation of Docker compose in DockerRestAPI folder, using which you can 
create REST API-based services (as demonstrated in class).

## URI Options
"http://<host:port>/listAll" => displays all open and close times (default to JSON)
"http://<host:port>/listOpenOnly" => displays only open times (default to JSON)
"http://<host:port>/listCloseOnly" => displays only close times (default to JSON)

"http://<host:port>/listAll/csv" => displays all open and close times in CSV
"http://<host:port>/listOpenOnly/csv" => displays only open times in CSV
"http://<host:port>/listCloseOnly/csv" => displays only close times in CSV

"http://<host:port>/listAll/csv?top=k => shows top k results in CSV
"http://<host:port>/listAll/json?top=k => shows top k results in JSON

## Other Options
Go to http://localhost:5000 (Consumer Product) to view database info in more easily readable format.
Go to http://localhost:5001 to input brevet controls into the calculator.

  
## Contact Info
River Veek
riverv@uoregon.edu

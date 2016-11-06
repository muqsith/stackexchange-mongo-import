# stackexchange-mongo-import
Python script to import stack exchange site dump into MongoDB.

This script was written/tested/used on Ubuntu 16.04 (never used on windows, feel free to modify)

Please install 7zip, if it is not installed.

`$ sudo apt install p7zip-full`

Steps to import stack exchange site data into MongoDB

Assuming you have site dump like askubuntu.com.7z

* Open mongo-db.conf file and set the database parameters.
* Opten terminal and execute the script
	
	`
	$ ./script.py /path/to/askubuntu.com.7z
	`
	
	`
	(or)
	`
	
	`
	$ python3.5 script.py /path/to/askubuntu.com.7z
	`

rdb-fullstack
=============

15th of August 2016

# Item Catalog

This is a project done by Unnar Thor Bachmann in the Udacity's full stack web developer nanodegree program. This is an implementation of a CRUD backend system. Each user can create, update and delete his/her itemsand read all other items. 

##Short explanation of functionality.

This project was made using [Flask](http://flask.pocoo.org/) and [sqlAlchemy](http://www.sqlalchemy.org/) and is supposed to run on a linux sytem. Either a local machine or [virtual machine](https://www.virtualbox.org/wiki/Downloads) using a [vagrant](https://www.vagrantup.com/) software to configure it. The project itself is inside the folder `catalog`.

##How to run the webpage.

1. Fork the repository.

2. Clone the repository to your machine by typing `git clone <url>.git` in the commmand line interface (e.g. Git bash). 

3. If running the project on a virtual machine type `vagrant up` followed by `vagrant ssh`.

4. Remove the current database with the commands `rm *.db` and `rm *.pyc`.

5. Create a new database with the commands `python database_setup.py` and populate it with the command `python AddingToDatabase.py`.

6. Run the client with `python project_item_catalog.py`.

7. Connect to it in a webbrowser using the url [http://localhost:8000/](http://localhost:8000/).




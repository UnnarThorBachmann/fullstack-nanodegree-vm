rdb-fullstack
=============

13th of June 2016

#Tournament Results

This is a project done by Unnar Thor Bachmann in the Udacity's full stack web developer nanodegree program. This is a python module which implements a database system. The system keeps track of players and matches during a Swiss-system tournament were player can either win or lose a match. 

##Short explanation of functionality.

This project was made using [PostgreSQL](https://www.postgresql.org/) and [python](https://www.python.org/) and is supposed to run on a linux sytem. Either a local machine or [virtual machine](https://www.virtualbox.org/wiki/Downloads) using a [vagrant](https://www.vagrantup.com/) software to configure it. The project itself is inside the folder `tournament`.

##How to run the webpage.

1. Fork the repository.

2. Clone the repository to your machine by typing `git clone <url>.git` in the commmand line interface (e.g. Git bash). 

3. If running the project on a virtual machine type `vagrant up` followed by `vagrant ssh`.

4. Navigate to `tournament` folder. Inside the folder there are three files: `tournament.py`, `tournament_test.py` and `tournament.sql`. 

5. Setup the database schema with `psql -f tournament.sql`.

6. Run the program using the commands `python tournament_test.py`.




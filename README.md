## Project
This project is a movie catalogue, RESTful web application created using the python Flask microframework.

It provides a login for users to Create new movie Genres and add movies to each genre. Logged in users can update and
delete and their own entries while reading other users entries.
 
Users not logged in have full read capabilities to view what movies others have added into the application.

## Running the virtual machine
* A terminal program such as GitBash is required and can be downloaded from [here for windows](https://git-scm.com/download/win)
* Vagrant and VirtualBox are required to be installed prior to running the application.
    * They can be installed from here: [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
* Clone the Full Stack VM repository [Here](https://github.com/udacity/fullstack-nanodegree-vm)
    * The clone contains the folder _catalogue_ this is where you save the files.
* Launch the Vagrant VM in the terminal by typing _'vagrant up'_ in the directory _fullstack/vagrant_
* In the terminal type: 
    * vagrant ssh
    * cd /vagrant
    * cd /catalogue

## Running the Catalogue App
* To create the database type **python database_setup.py**
* To populate the database with sample data type **python popdataset.py**
* Type **python app.py** to run the Flask web server. In your browser type **_http://localhost:5000/_** to view and
modify the movie cataloguing app. You will be able to view, create, edit and delete movies from the database.

# WebODM
A Flask Web Application for OpenDroneMap

## What is it?

WebODM is a web interface for [OpenDroneMap](https://github.com/OpenDroneMap/OpenDroneMap). Currently, this app is in development and does not do anything at all. The end goal for this project is:

* To create an avenue for running ODM remotely
* To provide a GUI for running ODM
* To be able to queue ODM processes
* to visualize, analyze, and share results

## Steps for getting it running locally

This app is based on [Flask](http://flask.pocoo.org/). The database is PostgreSQL. At this point in development, using a virtual environment would be best. Here's what I did to get started (assuming you have python and pip already installed:

```
sudo apt-get install python-virtualenv
git clone https://github.com/dakotabenjamin/WebODM.git
cd WebODM
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

In order to run the server, simply type `python manage.py runserver` and you should be able to open up the app at 127.0.0.1:5000/

## Development Plans

1. Add the sequence blueprint, basically a database view of the photos and ODM results.
  * Needs an form for the upload/parameters
2. Finish adding user profile stuff, like password recovery, etc. 
3. Email server
4. Backend: 
  * Once ODM is ported to python, getting it running smoothly with WebODM
  * Figure out how to get a queue working
  * Error logging, email to users when the process finishes, etc.
  * Getting the results to show on the front end (like an orthophoto in leaflet or something)
5. Social aspects



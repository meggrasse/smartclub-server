# SmartClub - Server

This is the server module of the SmartClub project. It is a Flask app that provides endpoints to
collect and provide data for the other modules.

The master repo for this project is located at https://github.com/meggrasse/smartclub.

## Requirements

Python: written using the Flask framework in Python 2.7.10. Should work on all versions of Python 2.7.

If you want to run locally, you will have to locally install the necessary libraries for this project.
Navigate to the smartclub-server directory in your shell and run:

```bash
$ pip install -r requirements.txt
```

## Setup

If you want to work together with the other modules of Smartclub you will need to put this code on a remote server.
I strongly recommend Heroku. Instructions as to how to deploy to Heroku can be found
[here](https://devcenter.heroku.com/articles/getting-started-with-python).

## Usage

If you are looking to run locally, run:

```bash
$ python app.py
```

The module will be available at http://0.0.0.0:1024/

Otherwise, functionality will be available at your server location.

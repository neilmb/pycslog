# Contributing to Pycslog

Pycslog is open-source software. All contributions are welcomed. To get
started, you will need to have Python installed. The python environment
is managed using Pipenv. To install Pipenv, just

```
pip3 install pipenv
```

Then, to install the required packages and set up a virtual environment, run

```
pipenv install
```

Finally, you can run the server with

```
pipenv run python3 ./run_server.py
```

or enter a shell in the virtualenv with

```
pipenv shell
```

## To Do

This is an attempt at a "what-next" list, but in no particular order

- Switch server to SQLite backend
- Add mode and date/time fields to data store
- Add /search endpoint to API for dupe checking
- Make a React client that can be served by the same Flask app
- Reduce python dependencies in requirements.txt to a minimum (bottle?)
- Add POST to /contact/<id> to allow editing an existing contact
- Add an admin section to the web app to allow loading different SQLite databases
- Add "export to ADIF" option to the clients to take the output of /contacts and make an ADIF file
- Test and document an access point setup for the RPi to use in the field
- Add other clients: iOS? Android? desktop app?
- Reproduce this list of projects as Github Issues

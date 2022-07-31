# finMessages
I wanted to rapidly build a small REST service to play around with.  Most of my work experience has been on existing services or on productionized highly-scalable environments.  Since I was focused on spinning something up quickly I chose Python 3 as the language for speed.  Additionally, I haven't had much experience with the Django framework yet, so I wanted to use the Django REST Framework.  By using this framework most of the REST boiler-plate code is already provided, which helps speed up development time.

# Setup
## TODO - Dockerize 
To make setup and running easier and faster for people I could containerize the code with something like Docker.  It's user-friendly because it spins up a new virtual environment with all the environment configured and managed.  I haven't had time to play around with this yet.

## Install Python 3
First you'll want to install Python 3.
https://www.python.org/downloads/
If you're on a Mac you can also use brew:
$ brew install python@3.9

To verify your installation try the following:
$ python3 -V
If python has been installed you should see something like:  
Python 3.9.13

## Clone This Repo
Using git, clone this repo onto your local machine.  
You should see a folder called finMessages where you cloned it, and beneath that should be finmessages a db file with some scant test data, the code, and the requirements.txt file.

## Import Dependencies
I used Django and the Django REST Framework.  In order to make local environment setup easier I created a requirements.txt file.  This should be maintained if new dependencies are added, or removed.  
To import the dependencies, navigate into finMessages/finmessages/  then execute:
$ pip3 install -r requirements.txt

This article provides an excellent overview of what the requirements.txt file is, how to create/update it, and why.  
https://learnpython.com/blog/python-requirements-file/

## Model Changes/Database Updates
Django provides a simple SqlLiteDb by default, though it can be configured to point to any other type of database.  Since speed and a functioning API were my goals here I left the default for my Db.  If you change any of the Models found in finMessages/finmessages/messageapi/models.py you will need to update the db.  You might also need to run these commands when you first spin up the service.
The first command creates a migration entry - this tracks the history of the db changes and what they are.
$ python3 manage.py makemigrations

The next command actually performs the migration updates.
$ python3 manage.py migrate

## Run The Server
The next step is to start the server. Execute this command:
$ python3 manage.py runserver
You'll see output like this:
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
July 30, 2022 - 23:26:52
Django version 4.0.6, using settings 'finmessages.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

Note that this prints out the server and port.  In this case it's just localhost:8000

Now you should be able to call the APIs using this as the base URL.  Errors and print statements output directly to the console while running locally.

# API Documentation
## Create  (POST only)
http://localhost:8000/create
I limited this endpoint to POST requests only because it should only be used to create new messages.  The inputs required:
* sender
* receiver
* body
Right now there is no validation on specific formatting other than max length of each field.
On the server side the following fields are added:
* id  (auto-incrementing numeric)
* created (datetime applied only on creation)
* modified (datetime applied on modification - editing not currently supported)
* received (boolean, defaults to False, updated to True when messages are received by specific recipient)

## Receive Messages - General Access  (GET)
http://localhost:8000/messages/
This will return a list of all the messages.
Query Parameter Options:
* Pagination: ?limit=10&offset=0  Overrides the number of messages returned and enables paging via the offset.  Limit and offset should be positive whole numbers.  
* Filter By Sender:  ?sender=sendernamehere  Where sendernamehere is replaced with the real sender name.  This returns a subset of the messages where only messages from this sender are returned.
* Filter By Recipient:  ?receiver=receivernamehere  Where receivernamehere is replaced with the real receiver name.  This returns a subset of the messages where only messages for this recipient are displayed.
* Filter By Age:  ?max_days_old=2  Where max_days_old should be a positive whole number.  This returns a subset of the messages that were created within the past max_days_old value.  The default is 30 days.
* Filter By Unreceived:  ?only_unreceived=true  Where the value is not null this flag is applied.  This returns a subset of ONLY the messages that have not be marked as received yet.

## Receive Messages - Specific Recipient  (GET)
http://localhost:8000/messages/receivernamehere/
Replace receivernamehere with the actual receiver name.
When messages are received via this URL path the received boolean is set to True.
Query parameter options are the same as general EXCEPT the filter by receiver is ignored in deference to this receiver on the path.

# TODOs
## Tests
I didn't have time to write the tests that I wanted to, so I only tested manually so far.  My idea was to use python to execute calls to the server to validate the following scenarios:
* Create - validate required fields - curl create, then assert based on the response values (id, received)
* Create - validate field sizes - curl create with values 
* Messages - validate each parameter filters to an expected subset of messages.
* Messages - validate defaults with no parameters
* Messages - validate that multiple parameters applies all of the filters
* Messages/receiver - validate each parameter
* Messages/receiver - validate that having reciever in query params is ignored in deference to the URL path value
* Messages/receiver - validate that messages received via this path set the received flag to True 
For backend APIs like this I prefer to start tests against the API behavior because this is the most stable type of testing and is language agnostic.  This type of testing makes me feel most comfortable making changes.  Unit tests are also useful, but in my mind are secondary to the integration tests.

## Logging/Metrics
Need to add logging for exceptions and metrics/actions.  Django provides something similar to Log4J via it's message API with the messages module:
https://docs.djangoproject.com/en/4.0/ref/contrib/messages/#module-django.contrib.messages  This is something to explore further.

## Authentication/Authorization
Django REST Framework provides this by default via Users and Groups.  This could be used for authentication and the groups could be used for authorization to certain resources.  More information on that here:  
https://www.django-rest-framework.org/api-guide/authentication/  Authenticate via users and authorize via groups.

## Dockerize 
By configuring Docker or some other container for this application it would be much easier to distribute and setup.  Containers like Docker manage the environment and dependencies so you don't have to do anything extra to set it up and run it.  I didn't have time yet to research how to set up a Docker container from scratch yet.  

# Additional Useful References
* Quick Overview: https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
* Model Best Practices (TODO):  https://dev.to/pragativerma18/django-models-basics-and-best-practices-49e4
* QuerySet API Reference:  https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.query.QuerySet.update
* Pagination Configuration Reference: https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination

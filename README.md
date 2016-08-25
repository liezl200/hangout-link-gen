# hangout-link-gen
Google Hangout link generator to create a large amount of public hangout links (the Hangouts API doesn't allow for this directly)

## Install

### Flask
- If you don't already have virtualenv:
`pip install virtualenv`

- Create a local virtual environment. Do not commit this.
`virtualenv venv`

_Reference:_ http://flask.pocoo.org/docs/0.11/installation/#installation

## Usage

1. Activate the virtual environment.
`source /venv/bin/activate`

2. Update dependencies.
`pip install -r requirements.txt`

3. To exit virtual environment:
`deactivate`

## Requirements

- To update dependencies:
`pip install -r requirements.txt`

- To save current dependencies:
`pip freeze > requirements.txt`

- Get `client_secret.json` (for Google OAuth 2) and `settings.py` (for the database)

## Using the endpoints
1. Go to www.google.com/calendar, click the Settings gear icon, click Settings, and then find "Automatically add Google+ hangouts to events I create" and select "Yes" (http://www.riskcompletefailure.com/2012/11/programmatically-scheduling-hangouts.html)
2. http://localhost:5000/login
3. Complete authentication
4. http://localhost:5000/get?n=100
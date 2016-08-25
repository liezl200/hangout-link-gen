#!flask/bin/python
import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client

app = flask.Flask(__name__)

@app.route('/get')
def getNLinks():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    http = credentials.authorize(httplib2.Http())

  if not 'n' in flask.request.args:
    return 'Add parameter n (example: /get?n=100)'
  n = int(flask.request.args.get('n'))

  links = []
  for i in range(n):
    event = {
      'summary': 'Google founded',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'Placeholder to extract hangout links',
      'start': {
        'dateTime': '1998-09-04T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '1998-09-04T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'reminders': {
        'useDefault': True,
      },
    }

    cal_service = discovery.build('calendar', 'v3', http=http)
    event = cal_service.events().insert(calendarId='primary', body=event).execute()
    link = event['hangoutLink']
    links.append(link)
    print link
  return json.dumps(link)

@app.route('/login')
def login():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  return 'You may now call /get?n=n'

@app.route('/login_success')
def oauth2callback():

  # To add more scopes, just add a new entry to the scope_list below
  # http://stackoverflow.com/questions/8449544/multiple-scope-values-to-oauth2
  scope_list = [
    'https://www.googleapis.com/auth/calendar'
  ]
  scope_str = " ".join(scope_list)
  flow = client.flow_from_clientsecrets(
    'client_secret.json',
    scope=scope_str,
    redirect_uri=flask.url_for('oauth2callback', _external=True)
  )
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('login'))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
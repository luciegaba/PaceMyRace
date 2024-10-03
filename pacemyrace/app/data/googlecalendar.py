import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events.owned']


def authentificate_googlecalendar():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  print(creds)
  service = build("calendar", "v3", credentials=creds)
  return service

def synchronise_planning(service, events):
    existing_events = service.events().list(calendarId='primary').execute().get('items', [])
    for event_data in events:
        summary = event_data.get("session_type")
        description = "{} {} {} {}".format(
            event_data.get("session_description", ""),
            event_data.get("pace_target", ""),
            event_data.get("time_target", ""),
            event_data.get("distance_target", "")
        )
        description = description.replace("None","")
        start_datetime = event_data.get("date")  
        if not start_datetime:
            print(f"Invalid or missing datetime for event: {summary}")
            continue

        end_datetime = event_data.get("end_datetime") if event_data.get("end_datetime") else start_datetime
        if any((existing_event.get('summary') == summary and existing_event.get('start').get('date') == start_datetime) for existing_event in existing_events):
            continue

        # Create the event structure
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'date': start_datetime,
            },
            'end': {
                'date': end_datetime,
            },
            'colorId': '10',  # Light green color,
        }
        try:
            html = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event '{summary}' created successfully.")
        except HttpError as error:
            print(f"Failed to create event '{summary}': {error}")

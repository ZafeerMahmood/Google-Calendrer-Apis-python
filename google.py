from google_calendar import create_event
from googleapiclient.errors import HttpError

def main():
    try:
        summary = 'Testing'
        location = 'testing/io'
        description = 'testing testing'
        start_datetime = '2023-05-28T09:00:00-07:00'
        end_datetime = '2023-05-28T17:00:00-07:00'
        recurrence = ['RRULE:FREQ=DAILY;COUNT=2']
        attendees = [{'email': 'lpage@example.com'}, {'email': 'sbrin@example.com'}]
        reminders = {
            'useDefault': False,
            'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}],
        }
        
        event_link = create_event(summary, location, description, start_datetime, end_datetime,
                                  recurrence, attendees, reminders)
        print('Event created:', event_link)

    except HttpError as error:
        print('An error occurred:', error)

if __name__ == '__main__':
    main()

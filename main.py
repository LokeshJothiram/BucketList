import pandas as pd
import datetime
import os

EXCEL_FILE = 'events.xlsx'

def load_events():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        return df
    else:
        return pd.DataFrame(columns=['Date', 'Event'])

def save_events(df):
    df.to_excel(EXCEL_FILE, index=False)

def show_events(df, selected_date):
    events = df[df['Date'] == selected_date]
    if events.empty:
        print("No events found for this date.")
    else:
        print(f"Events for {selected_date}:")
        for event in events['Event']:
            print(f"- {event}")

def add_event(df, selected_date, event):
    date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    today = datetime.datetime.now().date()

    if date_obj.date() < today:
        print("Cannot add event for a past date.")
        return df

    new_event = pd.DataFrame({'Date': [selected_date], 'Event': [event]})
    df = pd.concat([df, new_event], ignore_index=True)
    save_events(df)
    print("Event added successfully!")
    return df

def delete_event(df, selected_date, event_to_delete):
    if ((df['Date'] == selected_date) & (df['Event'] == event_to_delete)).any():
        df = df[~((df['Date'] == selected_date) & (df['Event'] == event_to_delete))]
        save_events(df)
        print("Event deleted successfully!")
    else:
        print("Event not found. No changes made.")
    return df

df = load_events()

while True:
    print("\nSimple Calendar App")
    print("1. Show Events")
    print("2. Add Event")
    print("3. Delete Event")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        selected_date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            show_events(df, selected_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    elif choice == '2':
        selected_date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            today = datetime.datetime.now().date()

            if date_obj.date() < today:
                print("Cannot add event for a past date.")
            else:
                event = input("Enter the event: ")
                if event:
                    df = add_event(df, selected_date, event)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    elif choice == '3':
        selected_date = input("Enter date (YYYY-MM-DD): ")
        event_to_delete = input("Enter the event to delete: ")
        if event_to_delete:
            try:
                datetime.datetime.strptime(selected_date, '%Y-%m-%d')
                df = delete_event(df, selected_date, event_to_delete)
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    elif choice == '4':
        print("Exiting the application.")
        break

    else:
        print("Invalid choice. Please select a valid option.")

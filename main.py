import json
import sqlite3
from datetime import datetime


def timestamp_to_milliseconds(timestamp):
    # Convert timestamp string to datetime object
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    # Convert datetime object to milliseconds value
    return int(dt.timestamp() * 1000)


def action_to_name(action):
    if action == 1:
        return "Ban"
    elif action == 2:
        return "Tempban"
    elif action == 3:
        return "Note"
    elif action == 4:
        return "Warn"
    elif action == 5:
        return "Also something"
    elif action == 6:
        return "Mute"
    elif action == 7:
        return "Unmute"
    elif action == 8:
        return "Case Removal"
    else:
        return ""


# Open the input file and load the JSON data
with open('cases_export.json', 'r') as f:
    data = json.load(f)

# Extract the relevant information from the JSON data
records = []
for case in data['cases']:
    created_at = timestamp_to_milliseconds(case['created_at'])
    actionType = action_to_name(case['type'])

    notes = ""

    for note in case['notes']:
        if not notes:
            notes = note['body']
        else:
            notes = notes + "\n**[UPDATE BY " + note['mod_name'] + "]**\n" + note['body']
    notes.replace("'", "\'")

    record = (
        case['case_number'],
        case['user_id'],
        case['user_name'],
        note['mod_id'],
        note['mod_name'],
        actionType,
        created_at,
        notes
    )

    records.append(record)
    print("Case ", case['case_number'], " completed")

# Connect to the database
conn = sqlite3.connect('cases.db')
cursor = conn.cursor()

# Create the cases table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        caseID INTEGER,
        userID TEXT,
        userName TEXT,
        modID TEXT,
        modName TEXT,
        actionType TEXT,
        timeHappened INTEGER,
        actionInfo TEXT
    )
''')

# Insert the records into the cases table
cursor.executemany('''
    INSERT INTO cases (
        caseID,
        userID,
        userName,
        modID,
        modName,
        actionType,
        timeHappened,
        actionInfo
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', records)

# Commit the changes and close the database connection
conn.commit()
conn.close()

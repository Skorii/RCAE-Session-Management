import json
from datetime import datetime, timedelta, time


def main():
    sql_file = 'insert.sql'
    open(sql_file, 'w', encoding='utf-8').close()
    with open('datas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for section in data:
        file_open_write_close(sql_file, format_insert_section(section['code'], section['name'], section['subscription'], section['active']))
        for cycle in section['cycle']:
            slit = cycle['date_start'].split("-")
            date_start = datetime(int(slit[0]), int(slit[1]), int(slit[2]))
            slit = cycle['date_end'].split("-")
            date_end = datetime(int(slit[0]), int(slit[1]), int(slit[2]))
            while date_start <= date_end:
                for session in cycle['session']:
                    if date_start.weekday() == day_str_to_int(session['weekday']):
                        split = session['hour'].split(':')
                        date = datetime(date_start.year, date_start.month, date_start.day, int(split[0]), int(split[1]))
                        duration = time(int(session['duration'].split(':')[0]), int(session['duration'].split(':')[1]))
                        file_open_write_close(sql_file, format_insert_session(date, duration, session['location'], session['max_members'], section['code']))
                date_start = add_one_day(date_start)


# DATA STRUCTURE BEGIN ----------------------------------------------------------------------------------------------------------------------------------
"""
[
   {
      "name": "name",
      "code": "CODE",
      "subscription": "0 OR 1",
      "active": "0 OR 1"
      "cycle":[
         {
            "date_start": "yyyy-mm-dd",
            "date_end": "yyyy-mm-dd",
            "session":[
               {
                  "weekday": "day",
                  "hour": "hh:mm",
                  "duration": "h:mm",
                  "location": "location",
                  "max_members": max_slots
               }, 
               ...
            ]
         }, 
         ...
      ]
   }, 
   ...
]
"""


# DATA STRUCTURE END ----------------------------------------------------------------------------------------------------------------------------------

# FUNCTIONS START ---------------------------------------------------------------------------------------------------------------------------
def add_one_day(date: datetime):
    return date + timedelta(days=1)


def format_insert_session(date: datetime, duration: time, location: str, max_members: int, section_id: str):
    temp = f"INSERT INTO inscription_session (date_time, duration, location, max_members, section_id) VALUES ('{date}', '{duration}', '{ single_to_double_quote(location)}', '{max_members}', '{section_id}');\n"
    return temp


def format_insert_section(code: str, name: str, subscription: str, active):
    temp = f"INSERT INTO inscription_section (code, name, subscription, active) VALUES ('{code}', '{single_to_double_quote(name)}', '{subscription}', '{active}');\n"
    return temp


def file_open_write_close(filename: str, to_write: str):
    f = open(filename, 'a', encoding='utf-8')
    f.write(to_write)
    f.close()


def single_to_double_quote(string: str):
    return string.replace("'", "''")


def day_str_to_int(day: str):
    day = day.lower()
    if day == "monday" or day == "lundi":
        return 0
    elif day == "tuesday" or day == "mardi":
        return 1
    elif day == "wednesday" or day == "mercredi":
        return 2
    elif day == "thursday" or day == "jeudi":
        return 3
    elif day == "friday" or day == "vendredi":
        return 4
    elif day == "saturday" or day == "samedi":
        return 5
    elif day == "sunday" or day == "dimanche":
        return 6
    else:
        return -1


# FUNCTIONS END ---------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

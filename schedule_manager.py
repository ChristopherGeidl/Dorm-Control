import json

SCHEDULE_FILE = "schedule.json"

def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_schedule(schedule):
    with open(SCHEDULE_FILE, 'w') as file:
        json.dump(schedule, file, indent=4)

def save_new_event(event):
    schedule = load_schedule()

    if "schedule"  not in schedule:
        schedule["schedule"] = []

    if len(schedule["schedule"]) == 0:
         schedule["schedule"].append(event)
    else:
        for i in range(len(schedule["schedule"])):
            if event["device"] < schedule["schedule"][i]["device"]:
                schedule["schedule"].insert(i,event)
                break
            elif event["device"] == schedule["schedule"][i]["device"]:
                if event["end_time"] <= schedule["schedule"][i]["start_time"]:
                    schedule["schedule"].insert(i,event)
                    break
            if i == len(schedule["schedule"])-1:
                schedule["schedule"].append(event)

    save_schedule(schedule)

def remove_event(device_name, start_time, end_time):
    schedule = load_schedule().get("schedule",[])

    for i in range(len(schedule)):
        if schedule[i]["device"] == device_name and schedule[i]["start_time"] == start_time and schedule[i]["end_time"] == end_time:
            schedule.pop(i)
            break
    save_schedule({"schedule":schedule})

def get_schedule():
    schedule = load_schedule()
    return schedule.get("schedule",[])

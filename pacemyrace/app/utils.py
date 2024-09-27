
def parse_pace(pace_str):
    try:
        minutes, seconds = pace_str.split(":")
        return int(minutes) + int(seconds) / 60
    except:
        return None

def calculate_missing_field(pace, time, distance):
    if pace and time and not distance:
        # If pace and time are provided, calculate distance
        return time / pace
    elif pace and distance and not time:
        # If pace and distance are provided, calculate time
        return pace * distance
    elif time and distance and not pace:
        # If time and distance are provided, calculate pace
        return time / distance
    return None
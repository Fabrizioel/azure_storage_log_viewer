from datetime import datetime

def is_valid_time(s):
    try:
        datetime.strptime(s, "%H:%M:%S")
        return True
    except ValueError:
        return False
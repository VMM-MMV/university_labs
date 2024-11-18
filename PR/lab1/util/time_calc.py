from datetime import datetime, timedelta

def get_formated_time(format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format)

def is_older_than_x_hours(stored_date_str, hour):
    stored_date = datetime.strptime(stored_date_str, "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()
    time_difference = current_time - stored_date
    return time_difference > timedelta(hours=hour)
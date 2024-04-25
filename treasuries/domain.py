import datetime

def parse_date(date_string):
    if not date_string:
        return None
    try:
        if len(date_string) == 4:
            return datetime.datetime.strptime(date_string, '%Y')
        elif len(date_string) == 6:
            return datetime.datetime.strptime(date_string, '%Y%m')
        elif len(date_string) == 8:
            return datetime.datetime.strptime(date_string, '%Y%m%d')
        elif len(date_string) == 10:
            return datetime.datetime.strptime(date_string, '%Y%m%d%H')
        elif len(date_string) == 12:
            return datetime.datetime.strptime(date_string, '%Y%m%d%H%M')
        elif len(date_string) == 14:
            return datetime.datetime.strptime(date_string, '%Y%m%d%H%M%S')
        else:
            return "Invalid date format"
    except ValueError:
        return "Invalid date format"

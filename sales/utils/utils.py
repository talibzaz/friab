from datetime import date


def get_current_date():
    today = date.today()
    d = today.strftime("%d-%B-%y")
    return d

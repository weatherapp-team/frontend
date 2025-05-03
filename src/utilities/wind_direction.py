def deg_to_direction(deg):
    if 0 <= deg < 78.75:
        return n_dir(deg)
    elif 78.75 <= deg < 168.75:
        return e_dir(deg)
    elif 168.75 <= deg < 258.75:
        return s_dir(deg)
    elif 258.75 <= deg < 348.75:
        return w_dir(deg)
    elif 348.75 <= deg < 360:
        return n_dir(deg)
    else:
        return "N"


def n_dir(deg):
    if 0 <= deg < 11.25:
        return "N"
    elif 11.25 <= deg < 33.75:
        return "NNE"
    elif 33.75 <= deg < 56.25:
        return "NE"
    elif 56.25 <= deg < 78.75:
        return "ENE"
    elif 348.75 <= deg < 360:
        return "N"


def e_dir(deg):
    if 78.75 <= deg < 101.25:
        return "E"
    elif 101.25 <= deg < 123.75:
        return "ESE"
    elif 123.75 <= deg < 146.25:
        return "SE"
    elif 146.25 <= deg < 168.75:
        return "SSE"


def s_dir(deg):
    if 168.75 <= deg < 191.25:
        return "S"
    elif 191.25 <= deg < 213.75:
        return "SSW"
    elif 213.75 <= deg < 236.25:
        return "SW"
    elif 236.25 <= deg < 258.75:
        return "WSW"


def w_dir(deg):
    if 258.75 <= deg < 281.25:
        return "W"
    elif 281.25 <= deg < 303.75:
        return "WNW"
    elif 303.75 <= deg < 326.25:
        return "NW"
    elif 326.25 <= deg < 348.75:
        return "NNW"

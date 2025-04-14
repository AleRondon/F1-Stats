from datetime import timedelta

def convert_time_to_seconds(time_string:str) -> float:
    """
    Convert a time string in format 'h:mm:ss.ss' or 'm:ss.ss' into seconds as a float.
    :param time_string: str - the time string to be converted, e.g., "1:42:06.304" or "1:15.096"
    :return: float - the total number of seconds represented by the input string
    """

    # Try parsing as hours, minutes, and seconds first
    try:
        h, m, s = map(float, time_string.split(':'))
        if h > 0:
            hours = timedelta(hours=h)
            minutes = timedelta(minutes=m)
            seconds = timedelta(seconds=s)

            total_seconds = hours.total_seconds() + minutes.total_seconds() + seconds.total_seconds()
        else:
            raise ValueError("Invalid time string format")
    except ValueError:
        # If parsing as hours, minutes, and seconds fails, try parsing as minutes and seconds
        m, s = map(float, time_string.split(':'))
        if m > 0:
            minutes = timedelta(minutes=m)
            seconds = timedelta(seconds=s)

            total_seconds = minutes.total_seconds() + seconds.total_seconds()
        else:
            raise ValueError("Invalid time string format")

    print(f"Total seconds: {total_seconds}")

    return total_seconds
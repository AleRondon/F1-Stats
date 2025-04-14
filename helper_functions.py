from datetime import timedelta

def convert_time_to_seconds(time_string:str):
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
        # If parsing as hours, minutes, and seconds fails, try parsing as minutes and seconds only
        try:
            m, s = map(float, time_string.split(':', 1))
            if m > 0:
                minutes = timedelta(minutes=m)
                seconds = timedelta(seconds=s)

                total_seconds = minutes.total_seconds() + seconds.total_seconds()
            else:
                raise ValueError("Invalid time string format")
        except ValueError:
            # If parsing as minutes and seconds only fails, try parsing as seconds alone
            try:
                s = float(time_string)
                if s >= 0.0:
                    total_seconds = s
                else:
                    raise ValueError("Invalid time string format")
            except ValueError:
                print(f"Error: Invalid time string '{time_string}'. Please ensure the input is in one of these formats: 'h:mm:ss.sss', 'm:ss.sss', or 'ss.sss'.")
                return None

    return total_seconds
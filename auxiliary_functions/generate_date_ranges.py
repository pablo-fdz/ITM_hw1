import datetime as dt
import calendar

def generate_date_ranges(year, month, num_weeks=3):
    """
    Generate 3 fixed weeks for a given month.
    Week 1: 1st to 8th
    Week 2: 9th to 16th
    Week 3: 17th to 24th
    
    Args:
        year (int): The year of the date ranges.
        month (int): The month of the date ranges.
        num_weeks (int): The number of weeks to generate per month (1, 2, or 3). Default is 3.
    
    Returns:
        list of tuples: A list of (start_date, end_date) pairs in "yyyy-mm-dd" format.
    """

    if num_weeks not in [1, 2, 3]:
        raise ValueError("num_weeks must be 1, 2, or 3.")
    
    # Define the start of the month and the last day of the month
    first_day_of_month = dt.date(year, month, 1)
    last_day_of_month = dt.date(year, month, calendar.monthrange(year, month)[1])

    # Define the 3 fixed week ranges
    week_ranges = [
        (first_day_of_month, min(first_day_of_month + dt.timedelta(days=7), last_day_of_month)),
        (first_day_of_month + dt.timedelta(days=8), min(first_day_of_month + dt.timedelta(days=15), last_day_of_month)),
        (first_day_of_month + dt.timedelta(days=16), min(first_day_of_month + dt.timedelta(days=23), last_day_of_month)),
    ][:num_weeks]  # Slice to include only the specified number of weeks

    # Format the date ranges in "yyyy-mm-dd"
    date_ranges = [(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")) for start_date, end_date in week_ranges]

    return date_ranges
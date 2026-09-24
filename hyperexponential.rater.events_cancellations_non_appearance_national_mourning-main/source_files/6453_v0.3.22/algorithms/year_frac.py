
# v0.3.0
from datetime import date

def from_to(start, end):
    return range(start, end+1)

def diffdays(ldate1, ldate2):
    # Report the TRUE number of days different between ldate1 and ldate2;
    # 0 if ldate1==ldate2, 1 if ldate1+1 == ldated2. Presumes ldate1 <= ldate2.
    return (ldate2 - ldate1).days * 1.0

def days_in_year(year):
    return diffdays(date(year, 1, 1), date(year, 12, 31)) + 1

def is_leap_year(year):
    return (days_in_year(year) == 366)

def feb29_between(date1, date2):
    # Requires date2.year = (date1.year + 1) or date2.year = date1.year.
    # Returns True if "Feb 29" is between the two dates (date1 may be Feb29).
    # Two possibilities: date1.year is a leap year, and date1 <= Feb 29 y1,
    # or date2.year is a leap year, and date2 > Feb 29 y2.
    mar1_date1_year = date(date1.year, 3, 1)
    if ( is_leap_year(date1.year) and (date1 < mar1_date1_year) and 
         (date2 >= mar1_date1_year)):
        return True
    mar1_date2_year = date(date2.year, 3, 1)
    if ( is_leap_year(date2.year) and (date2 >= mar1_date2_year) and
         (date1 < mar1_date2_year)):
        return True
    return False

def diff_appearance_lt_year(date1, date2):
    # Report if date1 and date2 "appear" to be 1 year or less apart.
    # Requires date1 <= date2; returns boolean.
    if date1.year == date2.year:
      return True
    if ( ((date1.year + 1) == date2.year) and
           ((date1.month > date2.month) or
           ((date1.month == date2.month) and (date1.day >= date2.day)))):
      return True
    return False

def basis1(date1,date2):
    # Swap so date1 <= date2 in all cases:
    if date1 > date2:
        date1, date2 = date2, date1
    if date1 == date2:
        return 0.0
    if diff_appearance_lt_year(date1, date2):
      if feb29_between(date1, date2):
        year_length = 366.
      elif (date1.year == date2.year and is_leap_year(date1.year)):
        year_length = 366.
      else:
        year_length = 365.
      return diffdays(date1, date2) / year_length
    else:
      days_in_years = 0.0
      num_years = 0.0
      for year in from_to(date1.year, date2.year):
        days_in_years += days_in_year(year)
        num_years += 1
      average_year_length = days_in_years / num_years
      return diffdays(date1, date2) / average_year_length







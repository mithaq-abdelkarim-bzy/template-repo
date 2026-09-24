import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from rate_utilities import _perform_lookup, look_up, look_up_with_bounds, approx_lookup


# ~~~~~~~~~~~~ 'look_up' example ~~~~~~~~~~~~~~

def example1():
    '''
    The `look_up` function performs an exact match lookup. It returns a specified value if the DataFrame is not valid or if the lookup fails.
    Here is an example of how to use `look_up`:
    '''

    # Sample DataFrame
    data = {'Surname': ['Brooks', 'Taylor', 'Chaplin', 'Gandy'], 'Name': ['Alice', 'Bob', 'Charlie', 'David']}
    df = pd.DataFrame(data)
    print(df)

    # Exact match lookup
    lookup_value = 'Brooks'
    lookup_col = 'Surname'
    return_col = 'Name'
    if_not_found = 'Not Found'

    # Perform the lookup
    result = look_up(lookup_value, lookup_col, return_col, df, if_not_found)
    print(result)

    return result

example1()

# ~~~~~~~~~~~~~~~~~  `look_up_with_bounds` Function ~~~~~~~~~~~~~~~~~~~

def example2():
    '''
    The `look_up_with_bounds` function performs a range-based lookup. 
    It returns a specified value if the DataFrame is not valid or if the lookup fails.

    Here is an example of how to use `look_up_with_bounds`:
    '''

    # Sample DataFrame with ranges
    data = {'LowerBound': [0, 4.5, 10], 'UpperBound': [4.5, 9.5, 14], 'Category': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    print(df)

    # Range-based lookup
    lookup_value = 4.5
    lower_bound_col = 'LowerBound'
    upper_bound_col = 'UpperBound'
    return_col = 'Category'
    if_not_found = 'Not Found'

    # Perform the lookup
    result = look_up_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found)
    print(result) 

    return result

example2()

# ~~~~~~~~~~~~~~~~~  `approx_lookup` Function ~~~~~~~~~~~~~~~~~~~

def example3():
    '''
    The `approx_lookup` function performs an approximate lookup. 
    It returns a specified value if the DataFrame is not valid or if the lookup fails.
    '''
    # Sample DataFrame with ranges
    data = pd.DataFrame({'Bound': [0, 10, 20, 30], 'Category': [1, 2, 3, 4]})
    df = pd.DataFrame(data)
    print(df)

    # Lookup parameters
    lookup_value = 26
    lookup_col = 'Bound'
    return_col = 'Category'
  

    # Perform the lookup
    result = approx_lookup(lookup_value, lookup_col, return_col, df)
    print(result)

    return result

example3()

import hx
from algorithms.windstorm.windstorm_rating_factor import windstorm_rating_factor


def us_windstorm_rating_calc(hxd, df, other_data):
    '''
    Calculates US Windstorm Rating
    '''

    df = windstorm_rating_factor(hxd, df, other_data)

    return df

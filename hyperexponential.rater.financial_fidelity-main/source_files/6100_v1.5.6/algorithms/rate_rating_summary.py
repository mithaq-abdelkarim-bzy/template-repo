import hx


def rate_rating_summary(hxd):
    
    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'
import hx


@hx.rating
def rating_algorithm(hxd):
    # Your rating algorithm goes here
    # For example:
    hxd.c = hxd.a + hxd.b

    hxd.hx_core.charged_premium = 0
    hxd.hx_core.model_premium = 0
    hxd.hx_core.ulr = 0
    hxd.hx_core.premium_currency = 'GBP'
    pass

import hx

def set_valid(hxd, field):
    setattr(getattr(hxd.noncds.validation, field), "valid", True)
    setattr(getattr(hxd.noncds.validation, field), "invalid", False)

def set_invalid(hxd, field, error_msg):
    setattr(getattr(hxd.noncds.validation, field), "valid", False)
    setattr(getattr(hxd.noncds.validation, field), "invalid", True)
    setattr(getattr(hxd.noncds.validation, field), "info_text", error_msg)
    hx.errors.validation(error_msg)

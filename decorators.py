from flask import g, redirect, url_for
from functools import wraps


def sign_in_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'baker'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("baker.baker_sign_in"))
    return wrapper

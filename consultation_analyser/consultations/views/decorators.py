"""
Dummy decorators for authentication-free demo.
Since authentication was removed, these decorators do nothing.
"""


def user_can_see_consultation(view_func):
    """No-op decorator - authentication removed for demo"""
    return view_func


def user_can_see_dashboards(view_func):
    """No-op decorator - authentication removed for demo"""
    return view_func 
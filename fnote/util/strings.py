import re

""" string utility methods """


def format_urlsafe(title):
    """Remove URL-unfriendly characters from string"""
    regexp = r'[^A-Za-z0-9_.~-]'
    return re.sub(regexp, '', title)

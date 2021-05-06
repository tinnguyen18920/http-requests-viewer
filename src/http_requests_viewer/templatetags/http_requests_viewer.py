from urllib.parse import urlparse, urljoin

from django import template

register = template.Library()

@register.filter
def hostname(url):
    """  """
    return urlparse(url).hostname

@register.filter
def path(url):
    """  """
    return urlparse(url).path

@register.filter
def clean_url(url):
    """  """
    return urljoin(url, urlparse(url).path) 
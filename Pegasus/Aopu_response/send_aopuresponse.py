import re

def is_html(response_text):
    return response_text.strip().startswith('<!DOCTYPE html>')

def is_ip(address):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return ip_pattern.match(address) is not None
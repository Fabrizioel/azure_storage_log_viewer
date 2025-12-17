import ipaddress

def is_valid_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False
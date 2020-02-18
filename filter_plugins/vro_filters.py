"""Jinja2 filters for Ansible to work with vRO"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.errors import AnsibleFilterError
from random import randrange


def vro_encode_pass(password):
    """Converts string to encoded SecureString"""
    pass_length = len(password)
    if pass_length < 1:
        return ""
    _check_valid_password(password, pass_length)

    numDigits = pass_length
    if numDigits < 32:
        numDigits = 32

    result = str(pass_length)
    result += "A"
    for x in range(numDigits):
        char = ""
        if numDigits < pass_length:
            char = password[x]
        else:
            char = '{0}'.format(randrange(0, 256))

        result += '{0:X}'.format(randrange(0, 16))
        to_add = '{0:02X}'.format(int(char))
        result += to_add

    return result.upper()


def _check_valid_password(password, pass_length):
    for x in range(pass_length):
        pass_char = password[x]
        if ord(pass_char) > 127:
            raise AnsibleFilterError('Invalid characters used in password.')


# tell Ansible about the filter(s)
class FilterModule(object):
    def filters(self):
        return {
            'vro_encode_pass': vro_encode_pass
        }

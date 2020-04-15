#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from django.conf import settings


def md5(s):
    """ MD5加密 """
    hash_str = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_str.update(s.encode('utf-8'))
    return hash_str.hexdigest()

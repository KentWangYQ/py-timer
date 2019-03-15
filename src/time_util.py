# -*- coding: utf-8 -*-

from datetime import datetime


def utc_now_timestamp_ms():
    return int(datetime.utcnow().timestamp() * 1000)
